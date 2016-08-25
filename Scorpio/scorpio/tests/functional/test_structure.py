from scorpio.tests import *

class TestStructureController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='structure_v', id=1))
        # Test response...
        assert 'Structure' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='structure_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='structure_v',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='structure_br'))
        # Test response...
        assert 'Browse structures' in response

    
    def test_structure_data(self):
        response = self.app.get(url(route_name='structure_structure', id=1))
        # Test response...
        assert 'Browse structures' in response 

    def test_structure_data_404_no_id(self):
        response = self.app.get(url(route_name='structure_structure'),
                                status=404)

    def test_structure_data_404_invalid_id(self):
        response = self.app.get(url(route_name='structure_structure',
                                    id=100000),
                                status=404)

    def test_itc_data(self):
        response = self.app.get(url(route_name='structure_itc', id=1))
        # Test response...
        assert 'Browse ITC data' in response 

    def test_itc_data_404_no_id(self):
        response = self.app.get(url(route_name='structure_itc'),
                                status=404)

    def test_itc_data_404_invalid_id(self):
        response = self.app.get(url(route_name='structure_itc',
                                    id=100000),
                                status=404)

