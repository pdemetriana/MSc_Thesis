from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.view import notfound_view_config
from pyramid.renderers import render

from model.meta import (
    DBSession,
    Base,
    )

from pyramid.events import BeforeRender
from scorpio import helpers

def add_renderer_globals(event):
   event['h'] = helpers

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    #config.add_static_view(name='ligand_img', path='scorpio:static/ligand_diagrams/{id}.png')


    config.include('pyramid_mako')
    config.add_mako_renderer('.html')
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.add_route('index', '/')
    config.add_route('home', '/{action}')

    config.add_route('protein_br', '/protein/browse/{page}')
    config.add_route('protein_v', '/protein/id/{id}')
    config.add_route('protein_itc', '/protein/itc_data/{page}/{id}')
    config.add_route('protein_structure', '/protein/structure_data/{page}/{id}')

    config.add_route('protein_classification_br', '/protein_classification/browse/{page}')
    config.add_route('protein_classification_v', '/protein_classification/id/{id}')
    config.add_route('protein_classification_protein', '/protein_classification/protein_data/{page}/{id}')

    config.add_route('protein_source_br', '/protein_source/browse/{page}')
    config.add_route('protein_source_v', '/protein_source/id/{id}')
    config.add_route('protein_source_protein', '/protein_source/protein_data/{page}/{id}')

    config.add_route('protein_ec_number_br', '/protein_ec_number/browse/{page}')
    config.add_route('protein_ec_number_v', '/protein_ec_number/id/{id}')
    config.add_route('protein_ec_number_protein', '/protein_ec_number/protein_data/{page}/{id}')

    config.add_route('protein_root_name_br', '/protein_root_name/browse/{page}')
    config.add_route('protein_root_name_v', '/protein_root_name/id/{id}')
    config.add_route('protein_root_name_protein', '/protein_root_name/protein_data/{page}/{id}')
    config.add_route('protein_root_name_itc', '/protein_root_name/itc_data/{page}/{id}')
    config.add_route('protein_root_name_structure', '/protein_root_name/structure_data/{page}/{id}')

    config.add_route('itc', '/itc/{action}')
    config.add_route('itc_br', '/itc/browse/{page}')
    config.add_route('itc_v', '/itc/id/{id}')
    config.add_route('itc_itc', '/itc/itc_data/{page}/{id}')
    config.add_route('itc_structure', '/itc/structure_data/{page}/{id}')

    config.add_route('structure_br', '/structure/browse/{page}')
    config.add_route('structure_v', '/structure/id/{id}')
    config.add_route('structure_structure', '/structure/structure_data/{page}/{id}')
    config.add_route('structure_itc', '/structure/itc_data/{page}/{id}')

    config.add_route('citation_br', '/citation/browse/{page}')
    config.add_route('citation_v', '/citation/id/{id}')
    config.add_route('citation_itc', '/citation/itc_data/{page}/{id}')
    config.add_route('citation_structure', '/citation/structure_data/{page}/{id}')

    config.add_route('author_v', '/author/id/{id}')
    config.add_route('author_br', '/author/browse/{page}')
    config.add_route('author_citation', '/author/citation_data/{page}/{id}')

    config.add_route('journal_br', '/journal/browse/{page}')
    config.add_route('journal_v', '/journal/id/{id}')
    config.add_route('journal_citation', '/journal/citation_data/{page}/{id}')

    config.add_route('itc_buffer_br', '/itc_buffer/browse/{page}')
    config.add_route('itc_buffer_v', '/itc_buffer/id/{id}')
    config.add_route('itc_buffer_itc', '/itc_buffer/itc_data/{page}/{id}')


    config.add_route('itc_comment_definition_br', '/itc_comment_definition/browse/{page}')
    config.add_route('itc_comment_definition_v', '/itc_comment_definition/id/{id}')
    config.add_route('itc_comment_definition_comment', '/itc_comment_definition/comment_data/{page}/{id}')

    config.add_route('itc_delta_cp_br', '/itc_delta_cp/browse/{page}')
    config.add_route('itc_delta_cp_v', '/itc_delta_cp/id/{id}')
    config.add_route('itc_delta_cp_itc', '/itc_delta_cp/itc_data/{page}/{id}')

    config.add_route('itc_comment_br', '/itc_comment/browse/{page}')
    config.add_route('itc_comment_v', '/itc_comment/id/{id}')
    config.add_route('itc_comment_itc', '/itc_comment/itc_data/{page}/{id}')

    config.add_route('itc_interaction_type_br', '/itc_interaction_type/browse/{page}')
    config.add_route('itc_interaction_type_v', '/itc_interaction_type/id/{id}')
    config.add_route('itc_interaction_type_itc', '/itc_interaction_type/itc_data/{page}/{id}')

    config.add_route('itc_instrument_br', '/itc_instrument/browse/{page}')
    config.add_route('itc_instrument_v', '/itc_instrument/id/{id}')
    config.add_route('itc_instrument_itc', '/itc_instrument/itc_data/{page}/{id}')

    config.add_route('ligand', '/ligand_hetnam//{action}')
    config.add_route('ligand_br', '/ligand/browse/{page}')
    config.add_route('ligand_v', '/ligand/id/{id}')
    config.add_route('ligand_itc', '/ligand/itc_data/{page}/{id}')
    config.add_route('ligand_structure', '/ligand/structure_data/{page}/{id}')

    config.add_route('ligand_hetnam_br', '/ligand_hetnam/browse/{page}')
    config.add_route('ligand_hetnam_v', '/ligand_hetnam/id/{id}')
    config.add_route('ligand_hetnam_ligand', '/ligand_hetnam/ligand_data/{page}/{id}')

    config.add_route('ligand_classification_br', '/ligand_classification/browse/{page}')
    config.add_route('ligand_classification_v', '/ligand_classification/id/{id}')
    config.add_route('ligand_classification_ligand', '/ligand_classification/ligand_data/{page}/{id}')

    config.add_route('ligand_features_v', '/ligand_features/id/{id}')
    config.add_route('ligand_features_br', '/ligand_features/browse/{page}')

    config.add_route('structure_contacts_v', '/structure_contacts/id/{id}')

    #config.add_notfound_view('error', renderer='scorpio:templates/derived/error/document.html')

    config.add_static_view(name='static', path='scorpio:static')

    config.scan('.views')
    return config.make_wsgi_app()

