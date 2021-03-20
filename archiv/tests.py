from django.test import TestCase
from archiv.models import NerSample, NerSource


class ArchivTestCase(TestCase):
    fixtures = ['dump.json']

    def setUp(self):
        # Test definitions as before.
        pass

    def test_001_source(self):
        # A test that uses the fixtures.
        items = NerSource.objects.all()
        self.assertTrue(items.count(), 1)
        self.assertTrue(items[0].__str__(), 'RTA')
        self.assertTrue('description' in items[0].info.keys())

    def test_002_nersample(self):
        items = NerSample.objects.all()
        self.assertTrue(items.count() > 1)
        for x in items:
            self.assertFalse(len(x.__str__()) > 20)
