import pandas as pd
from pickle import load
from utils.PostgresConnection import PostgresConnection
from uuid import uuid4
import os
import logging


class PredictService:

    def __init__(self, body, model_version):
        self.logger = logging.getLogger(__name__)
        self.logger.info(os.getcwd())
        self.model_version = model_version
        self.model = self.load_model(model_version)
        self.variables_to_predict = body
        self.pg_con = PostgresConnection(os.getenv('POSTGRES_DB'), os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'), os.getenv('POSTGRES_HOST'), '5432')

    @staticmethod
    def load_model(model_version):
        return load(open(f'api/models/{model_version}.pkl', 'rb'))

    def predict(self):

        to_predict = pd.DataFrame([self.variables_to_predict])

        try:
            self.variables_present_in_model()
            to_predict = to_predict[self.model.feature_names_in_]
            prediction = self.model.predict(to_predict)[0]
            unique_id = self.save_into_db(prediction, to_predict)
            return {'id': unique_id, 'prediction': float(prediction)}
        except Exception as e:
            raise ValueError(f"Error in prediction: {str(e)}")

    def save_into_db(self, prediction, to_predict):
        unique_id = str(uuid4())

        prediction = self.mount_prediction(prediction, unique_id)
        self.pg_con.insert_many('predictions', prediction)

        self.save_prediction(to_predict, unique_id)

        return unique_id

    def save_prediction(self, to_predict, unique_id):

        to_df = to_predict.T.reset_index()
        to_df.columns = ['variable_name', 'variable_value']
        to_df['model'] = self.model_version
        to_df['id'] = unique_id

        values = to_df.to_dict(orient='records')

        try:
            self.pg_con.insert_many('prediction_variables', values)
        except Exception as e:
            raise ValueError(f"Error in save prediction variables: {str(e)}")

    @staticmethod
    def mount_prediction(prediction, unique_id):
        return [{
            "id": unique_id,
            "predicted": prediction
        }]

    def variables_present_in_model(self):
        v = [i for i in self.model.feature_names_in_ if i not in self.variables_to_predict]
        if v:
            raise ValueError(f"Variables not present in body but required in model: {v}")
