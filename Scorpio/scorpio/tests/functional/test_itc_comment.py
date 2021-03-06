from scorpio.tests import *

class TestItcCommentController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='itc_comment_v', id=1))
        # Test response...
        assert 'ITC comment' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='itc_comment_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='itc_comment_v',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='itc_comment_br'))
        # Test response...
        assert 'Browse ITC comments' in response


    def test_itc_data(self):
        response = self.app.get(url(route_name='itc_comment_itc', id=1))
        # Test response...
        assert 'Browse ITC data' in response

    def test_itc_data_404_no_id(self):
        response = self.app.get(url(route_name='itc_comment_itc'),
                                status=404)

    def test_itc_data_404_invalid_id(self):
        response = self.app.get(url(controller='itc_comment_itc',
                                    id=100000),
                                status=404)
