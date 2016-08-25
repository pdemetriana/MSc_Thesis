from scorpio.tests import *

class TestProteinClassificationController(object):

    def __init__(self, request):
        self.request = request

    def test_view(self):
        response = self.app.get(url(route_name='protein_classification_v', id=1))
        # Test response...
        assert 'Protein classification' in response 

    def test_view_404_no_id(self):
        response = self.app.get(url(route_name='protein_classification_v'),
                                status=404)

    def test_view_404_invalid_id(self):
        response = self.app.get(url(route_name='protein_classification_v',
                                    id=100000),
                                status=404)

    def test_browse(self):
        response = self.app.get(url(route_name='protein_classification_br'))
        # Test response...
        assert 'Browse protein classifications' in response


    def test_protein_data(self):
        response = self.app.get(url(route_name='protein_classification_protein', id=1))
        # Test response...
        assert 'Browse proteins' in response

    def test_protein_data_404_no_id(self):
        response = self.app.get(url(route_name='protein_classification_protein'),
                                status=404)

    def test_protein_data_404_invalid_id(self):
        response = self.app.get(url(route_name='protein_classification_protein',
                                    id=100000))
        # Test response...
        assert 'No proteins available.' in response
