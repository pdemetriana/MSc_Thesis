import logging

from pyramid.response import Response
from pyramid.view import view_config

from scorpio import helpers as h
import pyramid.httpexceptions as exc

import scorpio.model as model
import scorpio.model.scorpio_tables as tables
import scorpio.model.meta as meta

import webhelpers.paginate as paginate

log = logging.getLogger(__name__)

class ItcBufferController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='itc_buffer_v', renderer='scorpio:templates/derived/itc_buffer/view.html') 
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.ITCBuffer)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='itc_buffer_br', renderer='scorpio:templates/derived/itc_buffer/browse.html') 
    def browse(self):
        records = model.meta.DBSession.query(tables.ITCBuffer)
        records = records.order_by('description')
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
        
    @view_config(route_name='itc_buffer_itc', renderer='scorpio:templates/derived/itc/browse.html') 
    def itc_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.ITC).filter_by(_buffer_id=id)
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

