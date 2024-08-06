This repository contains an example of using Docker Compose to deploy an API capable of returning predictions and saving the used parameters and predictions inside a PostgreSQL database.

Note: The .env file contains sensitive information and is included here for didactic purposes only.

For more details:

- [MODEL TRAINING](docs/model_training_doc.md)
- [API](docs/api_doc.md)
- [DOCKER FILES](docs/docker_doc.md)
- [POSTGRES SETUP](docs/postgres_doc.md)

The following examples demonstrate how to make a request to consume a Random Forest model trained on the Iris dataset:


## CURL
```
curl --location '{ip_address}/predict_test/predict?model_version=rf1_0' \
--header 'Content-Type: application/json' \
--data '{
        "petal length (cm)": 1,
        "petal width (cm)": 1,
        "sepal length (cm)":1,
        "sepal width (cm)": 1
}'
```

## Python Requests
```
import requests
import json

url = "{ip_address}/predict_test/predict?model_version=rf1_0"

payload = json.dumps({
  "petal length (cm)": 1,
  "petal width (cm)": 1,
  "sepal length (cm)": 1,
  "sepal width (cm)": 1
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

To use another SKLearn model, simply upload it to the models folder and change the model_version parameter to match the .pkl file name. Additionally, update the body values to match the column names of the trained model. (It is important to train the model with a DataFrame and not with an np.array.)
