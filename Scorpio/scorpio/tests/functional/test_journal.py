from scorpio.tests import *

class TestJournalController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='journal_v', id=1))
        # Test response...
        assert 'Journal' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='journal_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='journal_v',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='journal_br'))
        # Test response...
        assert 'Browse journals' in response


    def test_citation_data(self):
        response = self.app.get(url(route_name='journal_citation', id=1))
        # Test response...
        assert 'Browse citations' in response

    def test_citation_data_404_no_id(self):
        response = self.app.get(url(route_name='journal_citation'),
                                status=404)

    def test_citation_data_404_invalid_id(self):
        response = self.app.get(url(route_name='journal_citation',
                                    id=100000))
        # Test response...
        assert 'No citations available' in response
