from scorpio.tests import *

class TestProteinController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='protein_v', id=1))
        # Test response...
        assert 'Protein' in response

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='protein_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='protein',
                                    action='view',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='protein_br'))
        # Test response...
        assert 'Browse proteins' in response



    def test_itc_data(self):
        response = self.app.get(url(route_name='protein_itc', id=1))
        # Test response...
        assert 'Browse ITC data' in response

    def test_itc_data_404_no_id(self):
        response = self.app.get(url(route_name='protein_itc'),
                                status=404)

    def test_itc_data_invalid_id(self):
        response = self.app.get(url(route_name='protein_itc',
                                    id=100000))
        assert 'No ITC data available' in response

    def test_structure_data(self):
        response = self.app.get(url(route_name='protein_structure', id=1))
        # Test response...
        assert 'Browse structures' in response

    def test_structure_data_404_no_id(self):
        response = self.app.get(url(route_name='protein_structure'),
                                status=404)

    def test_structure_data_invalid_id(self):
        response = self.app.get(url(route_name='protein_structure',
                                    id=100000))
        assert 'No structural data available' in response
