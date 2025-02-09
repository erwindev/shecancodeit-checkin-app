from flask import Blueprint, jsonify, request
from flask_restx import Api, Namespace, Resource, fields
from app.config import Config
from app.attachment.api.attachment import api as attachment_ns

attachment_apiv1 = Blueprint('attachment_api', __name__, url_prefix='/a/v1')

attachment_api = Api(attachment_apiv1, version=Config.CURRENT_VERSION, title='{} Attachment API'.format(Config.SERVICE_NAME),
          description='Attachment End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))

attachment_api.add_namespace(attachment_ns, path="/attachment")

from app.appinfo import api as appinfo_ns
attachment_api.add_namespace(appinfo_ns, path="/app")

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}

attachment_api.authorizations = authorizations
attachment_api.security = 'Bearer Auth'