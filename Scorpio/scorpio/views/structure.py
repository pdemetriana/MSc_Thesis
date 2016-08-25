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
'''
records = meta.DBSession.query(tables.Protein).order_by(tables.Protein.name)
protein_options = [[r.id, str(r.name)] for r in records]
records = meta.DBSession.query(tables.Ligand).order_by(tables.Ligand.name)
ligand_options = [[r.id, str(r.name)] for r in records]
records = meta.DBSession.query(tables.Citation).join('journal')
records = records.order_by(tables.Journal.abbreviation)
records = records.order_by(tables.Citation.year)
records = records.order_by(tables.Citation.volume)
records = records.order_by(tables.Citation.first_page)
citation_options = [[r.id, str(r)] for r in records]
'''
class StructureController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='structure_v', renderer='scorpio:templates/derived/structure/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.Structure)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='structure_br', renderer='scorpio:templates/derived/structure/browse.html')
    def browse(self):
        records = model.meta.DBSession.query(tables.Structure)
        records = records.join('_protein')
        records = records.join('_ligand')
        records = records.order_by('Protein.name')
        records = records.order_by('Ligand.name')

	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

        
    @view_config(route_name='structure_structure', renderer='scorpio:templates/derived/structure/browse.html')
    def structure_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.Structure)
        rec = data.get(int(id))
        
        if rec is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.Structure)
        records = records.filter_by(_protein_id=rec.protein.id)
        if rec.ligand:
            records = records.filter_by(_ligand_id=rec.ligand.id)
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

    @view_config(route_name='structure_itc', renderer='scorpio:templates/derived/itc/browse.html')
    def itc_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.Structure)
        rec = data.get(int(id))
        if rec is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.ITC)
        records = records.filter_by(_protein_id=rec.protein.id)
        if rec.ligand:
            records = records.filter_by(_ligand_id=rec.ligand.id)
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
