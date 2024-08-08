The folder structure from the api is the following.

```
├── api
│   └── PredictController.py
├── app
│   └── Application.py
├── Dockerfile
├── main.py
├── models
│   └── rf1_0.pkl
├── service
│   └── PredictService.py
└── utils
    └── PostgresConnection.py
```
In summary:

- api/: Handles API routing and request/response handling.
- app/: Contains core application setup and configuration.
- Dockerfile: Defines how to containerize the application.
- main.py: Serves as the entry point to start the API.
- models/: Stores the machine learning model used by the application.
- service/: Contains business logic for handling predictions.
- utils/: Provides utility functions, like database connectivity.
