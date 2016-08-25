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

def number_of_cycles(values):
    return int(values['number_of_cycles'])


class LigandController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='ligand_v', renderer='scorpio:templates/derived/ligand/view.html')
    def view(self, id=None):
        id = self.request.matchdict["id"]
	if id is None:
            raise exc.HTTPNotFound()
        data = meta.DBSession.query(tables.Ligand)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='ligand_br', renderer='scorpio:templates/derived/ligand/browse.html')
    def browse(self):
        records = meta.DBSession.query(tables.Ligand)
        records = records.order_by('name')
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}
    '''
    @view_config(route_name='ligand', match_param="action=process_diagram")
    def process_diagram(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
       # data = meta.DBSession.query(tables.Ligand)
       # record = data.filter_by(id=id).first()
       # if record is None:
      #      raise exc.HTTPNotFound()
      #  action = request.params.getone('action')
      #  values = dict(request.params)
        # Don't use the values filed for repopulation
     #   del values['action']
     #   if action == 'Try again':
     #       self.request.tmpl_context.record = record
      #      return render_diagram_form(
       #         values=values,
        #        number_of_cycles=number_of_cycles(values)+1,
        #        id=id
        #    )
       # elif action == 'Save':
            # Issue an HTTP redirect
        #    response.status_int = 302
        #    response.headers['location'] = h.url(controller='ligand',
          #                                       action='view',
          #                                       id=record.id)
            return Response("Moved temporarily")
       # else:
         #   raise Exception('Invalid action%s'%action)
    '''
    @view_config(route_name='ligand_itc', renderer='scorpio:templates/derived/itc/browse.html')
    def itc_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.ITC).filter_by(_ligand_id=id)
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

        return render('/derived/itc/browse.html')

    @view_config(route_name='ligand_structure', renderer='scorpio:templates/derived/structure/browse.html')
    def structure_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.Structure).filter_by(_ligand_id=id)
        def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}


