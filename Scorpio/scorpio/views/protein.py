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

records = meta.DBSession.query(tables.ProteinRootName).order_by(tables.ProteinRootName.root_name)
root_name_options = [[r.id, str(r.root_name)] for r in records]
records = meta.DBSession.query(tables.ProteinSource).order_by(tables.ProteinSource.source)
source_options = [[r.id, str(r.source)] for r in records]
records = meta.DBSession.query(tables.ProteinClassification).order_by(tables.ProteinClassification.classification)
classification_options = [[r.id, str(r.classification)] for r in records]
records = meta.DBSession.query(tables.ProteinECNumber).order_by(tables.ProteinECNumber.ec_number)
ec_number_options = [[r.id, str(r.ec_number)] for r in records]

class ProteinController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='protein_v', renderer='scorpio:templates/derived/protein/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.Protein)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='protein_br', renderer='scorpio:templates/derived/protein/browse.html')
    def browse(self):
        records = model.meta.DBSession.query(tables.Protein).order_by('name')

        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
  
    @view_config(route_name='protein_itc', renderer='scorpio:templates/derived/itc/browse.html')      
    def itc_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.ITC).filter_by(_protein_id=id)
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

    @view_config(route_name='protein_structure', renderer='scorpio:templates/derived/structure/browse.html')      
    def structure_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.Structure).filter_by(_protein_id=id)
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

