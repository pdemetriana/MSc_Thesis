import logging

from pyramid.response import Response
from pyramid.request import TemplateContext as c
from pyramid.view import view_config

import pyramid.httpexceptions as exc

from scorpio import helpers as h

import scorpio.model as model
import scorpio.model.scorpio_tables as tables
import scorpio.model.meta as meta

import webhelpers.paginate as paginate

log = logging.getLogger(__name__)

class ItcInteractionTypeController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='itc_interaction_type_v', renderer='scorpio:templates/derived/itc_interaction_type/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.ITCInteractionType)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='itc_interaction_type_br', renderer='scorpio:templates/derived/itc_interaction_type/browse.html') 
    def browse(self):
        records = meta.DBSession.query(tables.ITCInteractionType)
        records = records.order_by('interaction_type')
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
        
    @view_config(route_name='itc_interaction_type_itc', renderer='scorpio:templates/derived/itc/browse.html') 
    def itc_data(self, id=None):
        if id is None:
            raise exc.HTTPNotFound()
        records = meta.DBSession.query(tables.ITC).filter_by(_interaction_type_id=id)
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
