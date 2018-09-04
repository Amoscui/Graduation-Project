from flask import Blueprint, Flask


webapp = Blueprint('web', __name__)


import web.views, web.forms