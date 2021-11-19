"""Check that data can be extracted from structured data files.

The `load_neos` function should load a collection of `NearEarthObject`s from a
CSV file, and the `load_approaches` function should load a collection of
`CloseApproach` objects from a JSON file.

To run these tests from the project root, run:

    $ python3 -m unittest --verbose tests.test_extract

These tests should pass when Task 2 is complete.
"""
import collections.abc
import datetime
import pathlib
import math
import unittest

from extract import load_neos, load_approaches
from models import NearEarthObject, CloseApproach


TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_NEO_FILE = TESTS_ROOT / 'test-neos-2020.csv'
TEST_CAD_FILE = TESTS_ROOT / 'test-cad-2020.json'


class TestLoadNEOs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.neos = load_neos(TEST_NEO_FILE)
        cls.neos_by_designation = {neo.designation: neo for neo in cls.neos}

    @classmethod
    def get_first_neo_or_none(cls):
        try:
            # Don't use __getitem__ in case the object is a set or a stream.
            return next(iter(cls.neos))
        except StopIteration:
            return None

    def test_neos_are_collection(self):
        self.assertIsInstance(self.neos, collections.abc.Collection)

    def test_neos_contain_near_earth_objects(self):
        neo = self.get_first_neo_or_none()
        self.assertIsNotNone(neo)
        self.assertIsInstance(neo, NearEarthObject)

    def test_neos_contain_all_elements(self):
        self.assertEqual(len(self.neos), 4226)

    def test_neos_contain_2019_SC8_no_name_no_diameter(self):
        self._extracted_from_test_asclepius_has_name_no_diameter_2(
            '2019 SC8', None, False
        )

    def test_asclepius_has_name_no_diameter(self):
        self._extracted_from_test_asclepius_has_name_no_diameter_2(
            '4581', 'Asclepius', True
        )

    def _extracted_from_test_asclepius_has_name_no_diameter_2(self, arg0, arg1, arg2):
        neo = self._extracted_from_test_adonis_is_potentially_hazardous_2(arg0, arg1)
        self.assertTrue(math.isnan(neo.diameter))
        self.assertEqual(neo.hazardous, arg2)

    # TODO Rename this here and in `test_neos_contain_2019_SC8_no_name_no_diameter`, `test_asclepius_has_name_no_diameter` and `test_adonis_is_potentially_hazardous`
    def test_adonis_is_potentially_hazardous(self):
        neo = self._extracted_from_test_adonis_is_potentially_hazardous_2(
            '2101', 'Adonis'
        )

        self.assertEqual(neo.diameter, 0.6)
        self.assertEqual(neo.hazardous, True)

    # TODO Rename this here and in `test_neos_contain_2019_SC8_no_name_no_diameter`, `test_asclepius_has_name_no_diameter` and `test_adonis_is_potentially_hazardous`
    def _extracted_from_test_adonis_is_potentially_hazardous_2(self, arg0, arg1):
        self.assertIn(arg0, self.neos_by_designation)
        result = self.neos_by_designation[arg0]
        self.assertEqual(result.designation, arg0)
        self.assertEqual(result.name, arg1)
        return result


class TestLoadApproaches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.approaches = load_approaches(TEST_CAD_FILE)

    @classmethod
    def get_first_approach_or_none(cls):
        try:
            # Don't __getitem__, in case it's a set or a stream.
            return next(iter(cls.approaches))
        except StopIteration:
            return None

    def test_approaches_are_collection(self):
        self.assertIsInstance(self.approaches, collections.abc.Collection)

    def test_approaches_contain_close_approaches(self):
        approach = self.get_first_approach_or_none()
        self.assertIsNotNone(approach)
        self.assertIsInstance(approach, CloseApproach)

    def test_approaches_contain_all_elements(self):
        self.assertEqual(len(self.approaches), 4700)

    def test_approach_time_is_datetime(self):
        approach = self.get_first_approach_or_none()
        self.assertIsNotNone(approach)
        self.assertIsInstance(approach.time, datetime.datetime)

    def test_approach_distance_is_float(self):
        approach = self.get_first_approach_or_none()
        self.assertIsNotNone(approach)
        self.assertIsInstance(approach.distance, float)

    def test_approach_velocity_is_float(self):
        approach = self.get_first_approach_or_none()
        self.assertIsNotNone(approach)
        self.assertIsInstance(approach.velocity, float)


if __name__ == '__main__':
    unittest.main()
