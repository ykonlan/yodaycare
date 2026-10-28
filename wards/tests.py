from django.test import TestCase, SimpleTestCase
from django.core.exceptions import ValidationError
from wards.validators import validator_for_name
from wards.models import Classroom, Ward
from django.contrib.auth.models import User, Group
from users.models import UserProfile
from django.urls import reverse

# Create your tests here.
class WardTests(SimpleTestCase):
    def test_ward_name_with_digits_success(self):
        validator_response = validator_for_name("Ama")
        self.assertIsNone(validator_response)

    def test_ward_name_with_digits_fail(self):
        with self.assertRaises(ValidationError):
            validator_for_name("Ama123")

class ClassroomTests(TestCase):
    def test_classroom_default_population_zero(self):
        classroom = Classroom.objects.create(
            class_name = "Tulips"
        )
        self.assertEqual(classroom.class_population, 0)

    def test_classroom_population_negative_int_fails(self):
        classroom = Classroom(
            class_name = "Marigold",
            class_population = -1
        )
        with self.assertRaises(ValidationError):
            classroom.full_clean()

    



        
        

