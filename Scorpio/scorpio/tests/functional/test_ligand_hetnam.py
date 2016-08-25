from scorpio.tests import *

class TestLigandHetnamController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='ligand_hetnam_v', id=1))
        # Test response...
        assert 'Ligand HETNAM' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='ligand_hetnam_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='ligand_hetnam_v',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='ligand_hetnam_br'))
        # Test response...
        assert 'Browse ligand HETNAMs' in response


    def test_ligand_data(self):
        response = self.app.get(url(route_name='ligand_hetnam_ligand', id=1))
        # Test response...
        assert 'Browse ligands' in response

    def test_ligand_data_404_no_id(self):
        response = self.app.get(url(route_name='ligand_hetnam_ligand'),
                                status=404)

    def test_ligand_data_404_invalid_id(self):
        response = self.app.get(url(route_name='ligand_hetnam_ligand',
                                    id=100000),
                                status=404)
