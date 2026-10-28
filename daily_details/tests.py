from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, User
from users.models import UserProfile, StaffProfile
from wards.models import Classroom, Ward

# Create your tests here.
class DailyDetailsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.parent_group_obj = Group.objects.get(name="Parents")
        # Sample classroom for ward
        cls.classroom1 = Classroom.objects.create(
                            class_name = "Marigold"
                        )

        cls.classroom2 = Classroom.objects.create(
                                    class_name = "Hibiscus"
                                )
        # Parent 1, Yoeman
        cls.p1 = User(
            username = "yoeman"
        )
        cls.p1.set_password("yyyisgood")

        # Parent 1 UserProfile
        cls.p1_profile = UserProfile(
            user_phone_1 = "055399013412",
            user_phone_2 = "055399013312"
        )

        # Assign Yoeman to UserProfile and save
        cls.p1_profile.user = cls.p1
        cls.p1.save()
        cls.p1.groups.add(cls.parent_group_obj)
        cls.p1_profile.save()

        # Parent 2, Evame
        cls.p2 = User(
            username = "evame",
        )
        cls.p2.set_password("yyyisgood")

        # Parent 2 UserProfile
        cls.p2_profile = UserProfile(
            user_phone_1 = "055399018934",
            user_phone_2 = "055399019834"
        )

        # Assign Evame to UserProfile and save
        cls.p2_profile.user = cls.p2
        cls.p2.save()
        cls.p2.groups.add(cls.parent_group_obj)
        cls.p2_profile.save()

        # Sample Ward, Tiana, belonging to Parent 1, Yoeman
        cls.ward1 = Ward.objects.create(
            ward_name = "Tiana Konlan",
            ward_parent = cls.p1_profile,
            ward_class = cls.classroom1
        )

        cls.ward2 = Ward.objects.create(
                    ward_name = "Tiana Cobblah",
                    ward_parent = cls.p2_profile,
                    ward_class = cls.classroom2
                )

        cls.staff_group = Group.objects.get(name="Staff")
        # Sample Staff1
        cls.s1 = User(
             username = "ibino"
        )
        cls.s1.set_password("yyyisgood")
        cls.s1.save()
        cls.s1.groups.add(cls.staff_group)

        cls.staff_user_profile = UserProfile(
            user_phone_1 = "055399013456",
            user_phone_2 = "055399013356"
        )
        cls.staff_user_profile.user = cls.s1
        cls.staff_user_profile.save()

        cls.staff_profile = StaffProfile.objects.create(
            staff = cls.s1,
            staff_classroom = cls.classroom1
        )
    
    def test_parent_cannot_view_another_parents_ward(self):
        # Login as Parent 2, Evame
        self.assertTrue(
            self.client.login(
                username = "evame",
                password = "yyyisgood"
            )
        )

        response = self.client.get(reverse("view-daily-report", kwargs={"pk":self.ward1.id}))
        self.assertEqual(response.status_code, 403)

    def test_parent_can_view_their_own_ward(self):
        # Login as Parent 1, Yoeman
        self.assertTrue(
            self.client.login(
                username = "yoeman",
                password = "yyyisgood"
            )
        )

        response = self.client.get(reverse("view-daily-report", kwargs={"pk":self.ward1.id}))
        self.assertEqual(response.status_code, 200)

    def test_staff_cannot_view_ward_from_other_class(self):
        self.assertTrue(
            self.client.login(
                username = "ibino",
                password = "yyyisgood"
            )
        )

        response = self.client.get(reverse("view-daily-report", kwargs={"pk": self.ward2.id}))
        self.assertEqual(response.status_code, 403)


    def test_staff_can_view_ward_from_their_class(self):
            self.assertTrue(
                self.client.login(
                    username = "ibino",
                    password = "yyyisgood"
                )
            )
    
            response = self.client.get(reverse("view-daily-report", kwargs={"pk": self.ward1.id}))
            self.assertEqual(response.status_code, 200)






