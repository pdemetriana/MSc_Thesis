
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.view import notfound_view_config
from pyramid.renderers import render

@notfound_view_config(renderer='scorpio:templates/derived/error/document.html')
def error(request):
    return {}
