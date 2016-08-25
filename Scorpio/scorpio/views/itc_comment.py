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

records = meta.DBSession.query(tables.ITCCommentDefinition).order_by(tables.ITCCommentDefinition.definition)
comment_definition_options = [[r.id, str(r.definition)] for r in records]

class ItcCommentController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='itc_comment_v', renderer='scorpio:templates/derived/itc_comment/view.html') 
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.ITCComment)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='itc_comment_br', renderer='scorpio:templates/derived/itc_comment/browse.html') 
    def browse(self):
        records = model.meta.DBSession.query(tables.ITCComment)
        records = records.order_by('comment')
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

    @view_config(route_name='itc_comment_itc', renderer='scorpio:templates/derived/itc/browse.html') 
    def itc_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        comment = model.meta.DBSession.query(tables.ITCComment).get(id)
        if comment is None:
            raise exc.HTTPNotFound()
        records = meta.DBSession.query(tables.ITC).filter(tables.ITC._comments.contains(comment))
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)
	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
