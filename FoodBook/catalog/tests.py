from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import FoodEntry

User = get_user_model()


@override_settings(DEBUG=True)
class VulnerabilityTests(TestCase):
    def setUp(self):
        self.client.defaults["REMOTE_ADDR"] = "127.0.0.1"
        self.alex = User.objects.create_user(username="alex_test", password="test-password-123")
        self.sam = User.objects.create_user(username="sam_test", password="test-password-456")
        self.alex_entry = FoodEntry.objects.create(name="Alex", favorite_dish="Pizza", owner=self.alex)
        self.sam_entry = FoodEntry.objects.create(name="Sam", favorite_dish="Sushi", owner=self.sam)

    def test_anonymous_user_is_redirected_from_idor_endpoint(self):
        response = self.client.get(reverse("idor_insecure", args=[self.sam_entry.pk]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_read_another_users_record_idor(self):
        self.client.force_login(self.alex)
        response = self.client.get(reverse("idor_insecure", args=[self.sam_entry.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sushi")

    def test_user_can_read_own_record(self):
        self.client.force_login(self.alex)
        response = self.client.get(reverse("idor_insecure", args=[self.alex_entry.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")

    def test_search_reflects_untrusted_html_without_escaping(self):
        payload = "<script>alert('FoodBook-XSS')</script>"
        response = self.client.get(reverse("home"), {"q": payload})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, payload, html=False)

class AccountAndEntryCreationTests(TestCase):
    def test_user_can_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new_user",
                "password1": "Strong-test-pass-123!",
                "password2": "Strong-test-pass-123!",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_registered_user_can_add_entry_and_becomes_owner(self):
        user = User.objects.create_user(
            username="food_author",
            password="Strong-test-pass-123!",
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse("add_entry"),
            {"name": "Маша", "favorite_dish": "Паста"},
        )
        self.assertRedirects(response, reverse("home"))
        entry = FoodEntry.objects.get(name="Маша")
        self.assertEqual(entry.favorite_dish, "Паста")
        self.assertEqual(entry.owner, user)

    def test_anonymous_user_cannot_add_entry(self):
        response = self.client.get(reverse("add_entry"))
        self.assertEqual(response.status_code, 302)

