This repository stores an example to use docker-compose to up an API capable of return predictions and save the used parameters and the prediction inside a postgres database.

THE .ENV CONTAINS SENSITIVE INFORMATION IT'S ONLY MAINTAINED HERE FOR DIDATIC PURPOSES

The following examples make a request to consume a Random Forest Model trained in the Iris dataset

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

To use another SKLearn model it's only necessary to upload it inside the models folder and change model_version parameter to match the .pkl file name and of course change the body values to match the column names of the trained model (It is important to train the model with a dataframe and not with a np.array)
