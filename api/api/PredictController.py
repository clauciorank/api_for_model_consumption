from flask import Blueprint
from werkzeug.exceptions import HTTPException
import json
from flask import request
from flask import abort, Response
from service.PredictService import PredictService

predict_blueprint = Blueprint('predict_test', __name__, url_prefix='/predict_test')


@predict_blueprint.errorhandler(HTTPException)
def handle_exception(error):
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": str(error.description)
    })
    response.content_type = "application/json"

    return response


@predict_blueprint.route('/predict', methods=['POST'])
def predict():
    try:
        if not request.data or request.data == b'' or request.data == b'{}':
            return abort(code=400, description='Body is Required')
        body: list = json.loads(request.data)

        model_version = request.args.get('model_version')

        prediction = PredictService(body, model_version).predict()
        return Response(json.dumps(prediction), status=200, content_type='application/json')
    except Exception as e:
        return abort(code=400, description=str(e))
