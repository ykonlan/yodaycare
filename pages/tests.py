from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.
class HomepageTests(SimpleTestCase):
    def test_page_exists_at_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_page_by_name_exists_at_url(self):
            response = self.client.get(reverse("login"))
            self.assertEqual(response.status_code, 200)

    def test_check_template_used(self):
         response = self.client.get(reverse("login"))
         self.assertTemplateUsed(response, "pages/index.html")

