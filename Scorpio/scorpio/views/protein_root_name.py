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

class ProteinRootNameController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='protein_root_name_v', renderer='scorpio:templates/derived/protein_root_name/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.ProteinRootName)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='protein_root_name_br', renderer='scorpio:templates/derived/protein_root_name/browse.html')
    def browse(self):
        records = model.meta.DBSession.query(tables.ProteinRootName)
        records = records.order_by('root_name')
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
      
    @view_config(route_name='protein_root_name_protein', renderer='scorpio:templates/derived/protein/browse.html')  
    def protein_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.Protein).filter_by(_protein_root_name_id=id)
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)    
        return {}

    @view_config(route_name='protein_root_name_itc', renderer='scorpio:templates/derived/itc/browse.html')  
    def itc_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.ITC)
        records = records.join('_protein').filter_by(_protein_root_name_id=id)
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)    
        return {}

    @view_config(route_name='protein_root_name_structure', renderer='scorpio:templates/derived/structure/browse.html')  
    def structure_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.Structure)
        records = records.join('_protein').filter_by(_protein_root_name_id=id)
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)    
        return {}

