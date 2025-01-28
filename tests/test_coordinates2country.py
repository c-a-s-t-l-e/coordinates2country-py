import unittest
from coordinates2country.coordinates2country import Coordinates2Country

class TestCoordinates2Country(unittest.TestCase):
    def setUp(self):
        self.c2c = Coordinates2Country()

    def test_germany(self):
        self.assertEqual(self.c2c.country(50, 10), "Germany")

    def test_france(self):
        self.assertEqual(self.c2c.country(-23.7, 39.8), "France")

    def test_invalid_coordinates(self):
        self.assertIsNone(self.c2c.country(-90, 181))
