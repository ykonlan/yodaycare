from django.test import TestCase, SimpleTestCase
from django.core.exceptions import ValidationError
from wards.validators import validator_for_name

# Create your tests here.
class WardTests(SimpleTestCase):
    def test_ward_name_with_digits_success(self):
        response = validator_for_name("Ama")
        self.assertIsNone(response)

    def test_ward_name_with_digits_fail(self):
        with self.assertRaises(ValidationError):
            response = validator_for_name("Ama123")

        
        

