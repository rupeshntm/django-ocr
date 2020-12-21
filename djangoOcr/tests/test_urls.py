from django.test import SimpleTestCase
from django.urls import reverse, resolve
from djangoOcr.views import home

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)
