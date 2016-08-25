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

class ProteinEcNumberController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='protein_ec_number_v', renderer='scorpio:templates/derived/protein_ec_number/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.ProteinECNumber)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='protein_ec_number_br', renderer='scorpio:templates/derived/protein_ec_number/browse.html')
    def browse(self):
        records = model.meta.DBSession.query(tables.ProteinECNumber)
        records = records.order_by("ec_number")
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}


    @view_config(route_name='protein_ec_number_protein', renderer='scorpio:templates/derived/protein/browse.html')        
    def protein_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.Protein).filter_by(_protein_ec_number_id=id)
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

