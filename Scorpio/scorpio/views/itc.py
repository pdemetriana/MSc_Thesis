import logging

from pyramid.response import Response
from pyramid.view import view_config

import pyramid.httpexceptions as exc

from scorpio import helpers as h

import scorpio.model as model
import scorpio.model.scorpio_tables as tables
import scorpio.model.meta as meta

import webhelpers.paginate as paginate

import matplotlib as mpl
import matplotlib.pyplot# as plt
import matplotlib.lines as mlines

from cStringIO import StringIO

log = logging.getLogger(__name__)

colors = ['g', 'r', 'b']

FIG_DIR = './scorpio/static/figures/'

def mk_figures():
    # dh vs ds plot
    fn = '%sdh_vs_ds.png' % FIG_DIR
    size = (6,6)
    dh_ds_figure(fn, size)
    # dg distribution plot
    fn = '%sdg_dist.png' % FIG_DIR
    size = (6,6)
    dg_dist(fn, size)
    # dh distribution plot
    fn = '%sdh_dist.png' % FIG_DIR
    size = (6,6)
    dh_dist(fn, size)
    # tds distribution plot
    fn = '%stds_dist.png' % FIG_DIR
    size = (6,6)
    tds_dist(fn, size)

def dh_ds_figure(fn, size=None):
    if size:
        figure = matplotlib.pyplot.figure(figsize=(size[0], size[1]))
    ax = matplotlib.pyplot.axes()
    interaction_types = model.meta.DBSession.query(tables.ITCInteractionType)
    for type in interaction_types:
        records = model.meta.DBSession.query(tables.ITC.delta_h,
                                           tables.ITC.delta_s,
                                           tables.ITC._interaction_type_id)
        records = records.filter(tables.ITC._interaction_type_id == type.id)
        records = records.filter(tables.ITC.delta_h != None)
        records = records.filter(tables.ITC.delta_s != None)
        dh = []
        ds = []
        for rec in records:
            dh.append(rec[0])
            ds.append(-rec[1])
        matplotlib.pyplot.scatter(dh, ds,
                    s=40,
                    marker='o',
                    c=colors[type.id-1],
                    label=type.interaction_type)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.axhline(color='black')
    matplotlib.pyplot.axvline(color='black')
    matplotlib.pyplot.xlabel(r'$\Delta$H (kJ/mol)')
    matplotlib.pyplot.ylabel(r'T$\Delta$S (kJ/mol)')
    matplotlib.pyplot.xlim((-125,50))
    matplotlib.pyplot.ylim((-75,100))
    x, y = ([-145, 50], [125, -70])  # dG = -20
    line = mlines.Line2D(x, y, c='black', ls=':')
    ax.add_line(line)
    matplotlib.pyplot.text(-100, 60, r'$\Delta$G = -20', rotation=-45)
    x, y = ([-185, 50], [125, -110])  # dG = -60
    line = mlines.Line2D(x, y, c='black', ls=':')
    ax.add_line(line)
    matplotlib.pyplot.text(-120, 40, r'$\Delta$G = -60', rotation=-45)
    x, y = ([-125, 50], [-125, 50])
    line = mlines.Line2D(x, y, lw=3., alpha=0.4)
    ax.add_line(line)
    matplotlib.pyplot.text(-50, -65, 'Entropy driven')
    matplotlib.pyplot.text(-100, -45, 'Enthalpy driven')
    matplotlib.pyplot.savefig(fn)
    matplotlib.pyplot.close()

def boxplot(fn, size, data, xticks, ylabel):
    if size:
        figure = matplotlib.pyplot.figure(figsize=(size[0], size[1]))
    ax = matplotlib.pyplot.axes()
    bp = matplotlib.pyplot.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    matplotlib.pyplot.setp(bp['boxes'], color='black')
    matplotlib.pyplot.setp(bp['whiskers'], color='black')
    matplotlib.pyplot.setp(bp['fliers'], color='red', marker='+')
    # Now fill the boxes with desired colors
    medians = range(len(data))
    for i, t in enumerate(xticks):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        boxCoords = zip(boxX,boxY)
        boxPolygon = mpl.patches.Polygon(boxCoords,
                                         facecolor=colors[i],
                                         alpha=0.4)
        ax.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            matplotlib.pyplot.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
    xtickNames = matplotlib.pyplot.setp(ax, xticklabels=xticks)
    matplotlib.pyplot.setp(xtickNames, color='black')
    matplotlib.pyplot.ylabel(ylabel)
    matplotlib.pyplot.savefig(fn)
    matplotlib.pyplot.close()

def dg_dist(fn, size):
    interaction_types = model.meta.DBSession.query(tables.ITCInteractionType)
    data = []
    xticks = []
    for type in interaction_types:
        xticks.append(type.interaction_type)
        records = model.meta.DBSession.query(tables.ITC.delta_g,
                                           tables.ITC._interaction_type_id,
                                           tables.ITC.temperature)
        records = records.filter(tables.ITC._interaction_type_id == type.id)
        records = records.filter(tables.ITC.delta_g != None)
        records = records.filter(tables.ITC.temperature != None)
        records = records.filter(tables.ITC.temperature <= 299.15)
        records = records.filter(tables.ITC.temperature >= 297.15)
        dg = []
        for rec in records:
            dg.append(rec[0])
        data.append(dg)
    boxplot(fn, size, data, xticks, ylabel=r'$\Delta$G (kJ/mol)')

def dh_dist(fn, size):
    interaction_types = model.meta.DBSession.query(tables.ITCInteractionType)
    data = []
    xticks = []
    for type in interaction_types:
        xticks.append(type.interaction_type)
        records = model.meta.DBSession.query(tables.ITC.delta_h,
                                           tables.ITC._interaction_type_id,
                                           tables.ITC.temperature)
        records = records.filter(tables.ITC._interaction_type_id == type.id)
        records = records.filter(tables.ITC.delta_h != None)
        records = records.filter(tables.ITC.temperature != None)
        records = records.filter(tables.ITC.temperature <= 299.15)
        records = records.filter(tables.ITC.temperature >= 297.15)
        dh = []
        for rec in records:
            dh.append(rec[0])
        data.append(dh)
    boxplot(fn, size, data, xticks, ylabel=r'$\Delta$H (kJ/mol)')

def tds_dist(fn, size):
    interaction_types = meta.DBSession.query(tables.ITCInteractionType)
    data = []
    xticks = []
    for type in interaction_types:
        xticks.append(type.interaction_type)
        records = meta.DBSession.query(tables.ITC.delta_s,
                                           tables.ITC._interaction_type_id,
                                           tables.ITC.temperature)
        records = records.filter(tables.ITC._interaction_type_id == type.id)
        records = records.filter(tables.ITC.delta_s != None)
        records = records.filter(tables.ITC.temperature != None)
        records = records.filter(tables.ITC.temperature <= 299.15)
        records = records.filter(tables.ITC.temperature >= 297.15)
        ds = []
        for rec in records:
            ds.append(rec[0])
        data.append(ds)
    boxplot(fn, size, data, xticks, ylabel=r'T$\Delta$S (kJ/mol)')


class ItcController(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='itc_v', renderer='scorpio:templates/derived/itc/view.html') 
    def view(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.ITC)
        self.request.tmpl_context.record = data.get(int(id))
        if self.request.tmpl_context.record is None:
            raise exc.HTTPNotFound()
        return {}

    @view_config(route_name='itc_br', renderer='scorpio:templates/derived/itc/browse.html') 
    def browse(self):
        records = model.meta.DBSession.query(tables.ITC)
        records = records.join('_protein')
        records = records.join('_ligand')
        records = records.order_by('Protein.name')
        records = records.order_by('Ligand.name')
 
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}


    @view_config(route_name='itc_structure', renderer='scorpio:templates/derived/structure/browse.html') 
    def structure_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = meta.DBSession.query(tables.ITC)
        rec = data.get(int(id))
        if rec is None:
            raise exc.HTTPNotFound()
        records = meta.DBSession.query(tables.Structure)
        records = records.filter_by(_protein_id=rec.protein.id)
        records = records.filter_by(_ligand_id=rec.ligand.id)
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

    @view_config(route_name='itc_itc', renderer='scorpio:templates/derived/itc/browse.html') 
    def itc_data(self, id=None):
        id = self.request.matchdict["id"]
        if id is None:
            raise exc.HTTPNotFound()
        data = model.meta.DBSession.query(tables.ITC)
        rec = data.get(int(id))
        if rec is None:
            raise exc.HTTPNotFound()
        records = model.meta.DBSession.query(tables.ITC)
        records = records.filter_by(_protein_id=rec.protein.id)
        records = records.filter_by(_ligand_id=rec.ligand.id)
	def page_url(page):
            return h.current_route_path(self.request, page=page, _query=self.request.GET)

	current_page = int(self.request.matchdict["page"])
	self.request.tmpl_context.paginator = paginate.Page(records, current_page, url=page_url)
        return {}

    @view_config(route_name='itc', match_param="action=regenerate_figures") 
    def regenerate_figures(self):
        mk_figures()
        # Issue an HTTP redirect
        response.status_int = 302
        response.headers['location'] = self.request.route_url('home',
                                             action='data_overview')
        return Response("Moved temporarily")
