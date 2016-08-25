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

class CitationController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='citation_v', renderer='scorpio:templates/derived/citation/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
	if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.Citation)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='citation_br', renderer='scorpio:templates/derived/citation/browse.html')
    def browse(self):
        records = model.meta.DBSession.query(tables.Citation).join('journal')
        records = records.order_by(tables.Journal.abbreviation)
        records = records.order_by(tables.Citation.year)
        records = records.order_by(tables.Citation.volume)
        records = records.order_by(tables.Citation.first_page)
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

    @view_config(route_name='citation_itc', renderer='scorpio:templates/derived/itc/browse.html')
    def itc_data(self, id=None):
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.ITC).filter_by(_citation_id=id)
        if records is None:
            raise exc.HTTPNotFound()
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

    @view_config(route_name='citation_structure', renderer='scorpio:templates/derived/structure/browse.html')
    def structure_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.Structure).filter_by(_citation_id=id)
        if records is None:
            raise exc.HTTPNotFound()
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
