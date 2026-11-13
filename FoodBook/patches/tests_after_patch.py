from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import FoodEntry

User = get_user_model()


@override_settings(DEBUG=True)
class SecurityFixTests(TestCase):
    def setUp(self):
        self.client.defaults["REMOTE_ADDR"] = "127.0.0.1"
        self.alex = User.objects.create_user(username="alex_test", password="test-password-123")
        self.sam = User.objects.create_user(username="sam_test", password="test-password-456")
        self.sam_entry = FoodEntry.objects.create(name="Sam", favorite_dish="Sushi", owner=self.sam)

    def test_idor_is_blocked_after_patch(self):
        self.client.force_login(self.alex)
        response = self.client.get(reverse("idor_insecure", args=[self.sam_entry.pk]))
        self.assertEqual(response.status_code, 404)

    def test_search_escapes_untrusted_html_after_patch(self):
        payload = "<script>alert('FoodBook-XSS')</script>"
        response = self.client.get(reverse("home"), {"q": payload})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, payload, html=False)
        self.assertContains(response, "&lt;script&gt;", html=False)
