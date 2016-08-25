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

import formencode
from formencode import htmlfill

from pyramid_simpleform import Form

log = logging.getLogger(__name__)

class AuthorController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='author_v', renderer='scorpio:templates/derived/author/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
	if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.Author)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='author_br', renderer='scorpio:templates/derived/author/browse.html')
    def browse(self):
        records = model.meta.DBSession.query(tables.Author)
        records = records.order_by('first_name').order_by('last_name')
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

    @view_config(route_name='author_citation', renderer='scorpio:templates/derived/citation/browse.html')   
    def citation_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        author = model.meta.DBSession.query(tables.Author).get(id)
        if author is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.Citation).filter(tables.Citation._authors.contains(author))
        if records is None:
            raise exc.HTTPNotFound()
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
