import logging

from pyramid.response import Response

from pyramid.view import view_config

import pyramid.httpexceptions as exc

from scorpio import helpers as h

import scorpio.model as model
import scorpio.model.scorpio_tables as tables
import scorpio.model.meta as meta

import webhelpers.paginate as paginate

log = logging.getLogger(__name__)

class ContactsController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='structure_contacts_v', renderer='scorpio:templates/derived/structure_contacts/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.Contacts)
        data = data.join('_structure')
        self.request.tmpl_context.record = data.filter(tables.Structure.id==int(id)).first()
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

