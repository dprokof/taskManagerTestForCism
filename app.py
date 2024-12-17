from flask import Flask
from flask_restful import Api
from resources import TaskResource, TaskListResource
from flask_swagger_ui import get_swaggerui_blueprint
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Task processing started.")


app = Flask(__name__)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL,
                                               API_URL,
                                               config={'app_name': "Task Service"})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

api.add_resource(TaskResource, '/tasks/<int:id>')
api.add_resource(TaskListResource, '/tasks')

if __name__ == '__main__':
    app.run(debug=True)
