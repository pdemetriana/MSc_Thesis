from scorpio.tests import *

class TestItcController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='itc_v', id=1))
        # Test response...
        assert 'ITC datum' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='itc_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='itc_v',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='itc_br'))
        # Test response...
        assert 'Browse ITC data' in response

    
    def test_structure_data(self):
        response = self.app.get(url(route_name='itc_structure', id=1))
        # Test response...
        assert 'Browse structures' in response 

    def test_structure_data_404_no_id(self):
        response = self.app.get(url(route_name='itc_structure'),
                                status=404)

    def test_structure_data_404_invalid_id(self):
        response = self.app.get(url(route_name='itc_structure',
                                    id=100000),
                                status=404)

    def test_itc_data(self):
        response = self.app.get(url(route_name='itc_itc', id=1))
        # Test response...
        assert 'Browse ITC data' in response 

    def test_itc_data_404_no_id(self):
        response = self.app.get(url(route_name='itc_itc'),
                                status=404)

    def test_itc_data_404_invalid_id(self):
        response = self.app.get(url(route_name='itc_itc',
                                    id=100000),
                                status=404)

    def test_regenerate_figures(self):
        response = self.app.get(url(route_name='itc',
                                     match_param='regenerate_figures'),
                                status=302)
        # Test response...
        assert 'Moved temporarily' in response 
