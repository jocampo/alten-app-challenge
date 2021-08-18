from flask_swagger_ui import get_swaggerui_blueprint

from api.controllers.Routes import Routes

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    Routes.SWAGGER.value,
    Routes.SWAGGER_CONFIG.value,
    config={
        'app_name': "jocampo-alten-app-challenge"
    }
)
