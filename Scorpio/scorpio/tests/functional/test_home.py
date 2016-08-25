from scorpio.tests import *

class TestHomeController(object):


    def __init__(self, request):
        self.request = request

    def test_home(self):
        response = self.app.get(url(route_name='index'))
        # Test response...
        assert 'Welcome to SCORPIO!' in response

    def test_data_overview(self):
        response = self.app.get(url(route_name='home',
                                    match_param="action=data_overview"))
        # Test response...
        assert 'SCORPIO data overview' in response

    def test_acknowledgements(self):
        response = self.app.get(url(route_name='home',
                                    match_param='acknowledgements'))
        # Test response...
        assert '<h2>Acknowledgements</h2>' in response

    def test_contact(self):
        response = self.app.get(url(route_name='home', match_param='contact'))
        # Test response...
        assert 'Contact details' in response
