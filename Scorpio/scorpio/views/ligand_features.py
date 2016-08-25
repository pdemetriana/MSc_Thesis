import logging

from pyramid.response import Response

from pyramid.view import view_config

import pyramid.httpexceptions as exc

from scorpio import helpers as h

import scorpio.model as model
import scorpio.model.scorpio_tables as tables
import scorpio.model.meta as meta

import webhelpers.paginate as paginate

import os
import pybel

log = logging.getLogger(__name__)

class LigandFeaturesController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='ligand_features_v', renderer='scorpio:templates/derived/ligand_characteristics/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
	if id is None:
            raise exc.HTTPNotFound()
        data = meta.DBSession.query(tables.Ligand_Features)
        data=data.join('_ligand')
        self.request.tmpl_context.record = data.filter(tables.Ligand.id==id).first()
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='ligand_features_br', renderer='scorpio:templates/derived/ligand_characteristics/browse.html')
    def browse(self):
        records = meta.DBSession.query(tables.Ligand_Features)
        records = records.order_by('name')
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

