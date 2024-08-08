from flask import Flask
from api.PredictController import predict_blueprint

class Application:
    def run(self):
        # Initialize the Flask application
        app = Flask(__name__)

        # Register the blueprint from PredictController
        app.register_blueprint(predict_blueprint)

        # Run the app on host 0.0.0.0 and port 8080
        app.run(host="0.0.0.0", port=8080)
