import logging

from pyramid.response import Response

from pyramid.view import view_config, view_defaults

log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )



class Home(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='index', renderer="scorpio:templates/derived/home/index.html")
    def index(self):
        return {}
   
    @view_config(route_name='home', renderer="scorpio:templates/derived/home/data_overview.html", match_param="action=data_overview")
    def data_overview(self):
        return {}

    @view_config(route_name='home', renderer="scorpio:templates/derived/home/acknowledgements.html", match_param="action=acknowledgements")
    def acknowledgements(self):
        return {}

    @view_config(route_name='home', renderer="scorpio:templates/derived/home/contact.html", match_param="action=contact")
    def contact(self):
        return {}


