from scorpio.tests import *

class TestLigandClassificationController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='ligand_classification_v', id=1))
        # Test response...
        assert 'Ligand classification' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='ligand_classification_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='ligand_classification',
                                    action='view',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='ligand_classification_br'))
        # Test response...
        assert 'Browse ligand classifications' in response



    def test_ligand_data(self):
        response = self.app.get(url(route_name='ligand_classification_ligand', id=1))
        # Test response...
        assert 'Browse ligands' in response

    def test_ligand_data_404_no_id(self):
        response = self.app.get(url(route_name='ligand_classification_ligand'),
                                status=404)

    def test_ligand_data_404_invalid_id(self):
        response = self.app.get(url(route_name='ligand_classification_ligand',
                                    id=100000))
        # Test response...
        assert 'No ligands available' in response
