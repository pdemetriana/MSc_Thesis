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

class LigandHetnamController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='ligand_hetnam_v', renderer='scorpio:templates/derived/ligand_hetnam/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.exception_response(400)
        data = model.meta.DBSession.query(tables.LigandHetnam)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.exception_response(400)
        return {}

    @view_config(route_name='ligand_hetnam_br', renderer='scorpio:templates/derived/ligand_hetnam/browse.html')
    def browse(self):
        records = model.meta.DBSession.query(tables.LigandHetnam)
        records = records.order_by('hetnam')
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
        
    @view_config(route_name='ligand_hetnam_ligand', renderer='scorpio:templates/derived/ligand/browse.html')
    def ligand_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.exception_response(400)
        hetnam = meta.DBSession.query(tables.LigandHetnam).get(id)
        if hetnam is None:
            raise exc.exception_response(400)
        records = meta.DBSession.query(tables.Ligand).filter(tables.Ligand._hetnams.contains(hetnam))
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
