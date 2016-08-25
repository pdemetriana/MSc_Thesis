from scorpio.tests import *

class TestItcCommentDefinitionController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='itc_comment_definition_v', id=1))
        # Test response...
        assert 'ITC comment definition' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='itc_comment_definition_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='itc_comment_definition_v',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='itc_comment_definition_br'))
        # Test response...
        assert 'Browse ITC comment definitions' in response


    def test_comment_data(self):
        response = self.app.get(url(route_name='itc_comment_definition_comment', id=1))
        # Test response...
        assert 'Browse ITC comments' in response

    def test_comment_data_404_no_id(self):
        response = self.app.get(url(route_name='itc_comment_definition_comment'),
                                status=404)

    def test_comment_data_404_invalid_id(self):
        response = self.app.get(url(route_name='itc_comment_definition_comment',
                                    id=100000))
        # Test response...
        assert 'No ITC comments available.' in response
