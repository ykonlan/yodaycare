from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from users.models import UserProfile


class AllParentsAPITests(TestCase):
    def setUp(self):
        admin_group = Group.objects.create(name="Administrators")
        parent_group = Group.objects.create(name="Parents")
        self.admin = User.objects.create_user(username="admin", password="password")
        self.admin.groups.add(admin_group)
        self.parent = User.objects.create_user(
            username="parent",
            password="password",
            first_name="Casey",
            last_name="Parent",
            email="casey@example.com",
        )
        self.parent.groups.add(parent_group)
        UserProfile.objects.create(
            user=self.parent,
            user_phone_1="555-0101",
            user_phone_2="555-0102",
        )
        self.client.force_login(self.admin)

    def test_unfiltered_request_returns_datatables_rows(self):
        response = self.client.get(reverse("all-parents-api"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["recordsTotal"], 1)
        self.assertEqual(payload["recordsFiltered"], 1)
        self.assertEqual(len(payload["data"]), 1)
        self.assertEqual(payload["data"][0]["email"], "casey@example.com")
        self.assertEqual(payload["data"][0]["user_phone_1"], "555-0101")
        self.assertEqual(payload["data"][0]["user_phone_2"], "555-0102")