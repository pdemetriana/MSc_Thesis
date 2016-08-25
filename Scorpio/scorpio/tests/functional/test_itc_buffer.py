from scorpio.tests import *

class TestItcBufferController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='itc_buffer_v', id=1))
        # Test response...
        assert 'ITC buffer' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='itc_buffer_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='itc_buffer_v',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='itc_buffer_br'))
        # Test response...
        assert 'Browse ITC buffers' in response


    def test_itc_data(self):
        response = self.app.get(url(route_name='itc_buffer_itc', id=1))
        # Test response...
        assert 'Browse citations' in response

    def test_itc_data_404_no_id(self):
        response = self.app.get(url(route_name='itc_buffer_itc'),
                                status=404)

    def test_itc_data_404_invalid_id(self):
        response = self.app.get(url(route_name='itc_buffer_itc',
                                    id=100000))
        # Test response...
        assert 'No ITC data available' in response
