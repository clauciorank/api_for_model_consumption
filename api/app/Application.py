from flask import Flask
from api.PredictController import predict_blueprint


class Application:

    def run(self):

        app = Flask(__name__)
        app.register_blueprint(predict_blueprint)
        app.run(host="0.0.0.0", port=8080)
