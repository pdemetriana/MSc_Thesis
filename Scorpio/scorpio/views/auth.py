import logging

from pyramid.response import Response

from pyramid.view import view_config

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )


#from pylons.controllers.util import abort, redirect
#from scorpio.lib.base import BaseController, render
#from authkit.authorize.pylons_adaptors import authorize
#from authkit.permissions import UserIn

log = logging.getLogger(__name__)

class AuthController(object):

    def __init__(self, request):
        self.request = request
'''
    #@view_config(route_name='auth', renderer='scorpio:templates/derived/home/index.html', match_param="action=signin")
   # @authorize(UserIn(["admin"]))
    def signin(self):
        return {}

    @view_config(route_name='auth', renderer='scorpio:templates/derived/home/index.html', match_param="action=signout")
    def signout(self):
        return {}
'''
