import pandas as pd
from pickle import load
from utils.PostgresConnection import PostgresConnection
from uuid import uuid4
import os
import logging

class PredictService:

    def __init__(self, body, model_version):
        # Set up logging for the service
        self.logger = logging.getLogger(__name__)
        self.logger.info(os.getcwd())  # Log the current working directory

        # Initialize model version and load the corresponding model
        self.model_version = model_version
        self.model = self.load_model(model_version)

        # Store the variables to predict
        self.variables_to_predict = body

        # Initialize the PostgreSQL connection using environment variables
        self.pg_con = PostgresConnection(
            os.getenv('POSTGRES_DB'), 
            os.getenv('POSTGRES_USER'), 
            os.getenv('POSTGRES_PASSWORD'), 
            os.getenv('POSTGRES_HOST'), 
            '5432'
        )

    @staticmethod
    def load_model(model_version):
        # Load the machine learning model from the specified pickle file
        return load(open(f'api/models/{model_version}.pkl', 'rb'))

    def predict(self):
        # Convert input variables into a DataFrame
        to_predict = pd.DataFrame([self.variables_to_predict])

        try:
            # Ensure all required variables are present
            self.variables_present_in_model()

            # Select only the features used by the model
            to_predict = to_predict[self.model.feature_names_in_]

            # Make the prediction
            prediction = self.model.predict(to_predict)[0]

            # Save prediction and return the result with a unique ID
            unique_id = self.save_into_db(prediction, to_predict)
            return {'id': unique_id, 'prediction': float(prediction)}
        except Exception as e:
            # Handle and raise errors related to prediction
            raise ValueError(f"Error in prediction: {str(e)}")

    def save_into_db(self, prediction, to_predict):
        # Generate a unique ID for the prediction
        unique_id = str(uuid4())

        # Prepare the prediction record and save it to the database
        prediction = self.mount_prediction(prediction, unique_id)
        self.pg_con.insert_many('predictions', prediction)

        # Save the input variables associated with the prediction
        self.save_prediction(to_predict, unique_id)

        return unique_id

    def save_prediction(self, to_predict, unique_id):
        # Transform the input variables DataFrame for saving
        to_df = to_predict.T.reset_index()
        to_df.columns = ['variable_name', 'variable_value']
        to_df['model'] = self.model_version
        to_df['id'] = unique_id

        # Convert DataFrame to a list of dictionaries
        values = to_df.to_dict(orient='records')

        try:
            # Insert the variable values into the database
            self.pg_con.insert_many('prediction_variables', values)
        except Exception as e:
            # Handle and raise errors related to saving variables
            raise ValueError(f"Error in save prediction variables: {str(e)}")

    @staticmethod
    def mount_prediction(prediction, unique_id):
        # Structure the prediction data for database insertion
        return [{
            "id": unique_id,
            "predicted": prediction
        }]

    def variables_present_in_model(self):
        # Check for missing required variables in the input
        v = [i for i in self.model.feature_names_in_ if i not in self.variables_to_predict]
        if v:
            raise ValueError(f"Variables not present in body but required in model: {v}")
