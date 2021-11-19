"""Check that an `NEODatabase` can be constructed and responds to inspect queries.

The `NEODatabase` constructor should cross-link NEOs and their close approaches,
as well as prepare any additional metadata needed to support the `get_neo_by_*`
methods.

To run these tests from the project root, run:

    $ python3 -m unittest --verbose tests.test_database

These tests should pass when Task 2 is complete.
"""
import pathlib
import math
import unittest


from extract import load_neos, load_approaches
from database import NEODatabase


# Paths to the test data files.
TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_NEO_FILE = TESTS_ROOT / 'test-neos-2020.csv'
TEST_CAD_FILE = TESTS_ROOT / 'test-cad-2020.json'


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.neos = load_neos(TEST_NEO_FILE)
        cls.approaches = load_approaches(TEST_CAD_FILE)
        cls.db = NEODatabase(cls.neos, cls.approaches)

    def test_database_construction_links_approaches_to_neos(self):
        for approach in self.approaches:
            self.assertIsNotNone(approach.neo)

    def test_database_construction_ensures_each_neo_has_an_approaches_attribute(self):
        for neo in self.neos:
            self.assertTrue(hasattr(neo, 'approaches'))

    def test_database_construction_ensures_neos_collectively_exhaust_approaches(self):
        approaches = set()
        for neo in self.neos:
            approaches.update(neo.approaches)
        self.assertEqual(approaches, set(self.approaches))

    def test_database_construction_ensures_neos_mutually_exclude_approaches(self):
        seen = set()
        for neo in self.neos:
            for approach in neo.approaches:
                if approach in seen:
                    self.fail(f"{approach} appears in the approaches of multiple NEOs.")
                seen.add(approach)

    def test_get_neo_by_designation(self):
        self._extracted_from_test_get_neo_by_designation_2(
            '1865', 'Cerberus', 1.2, False
        )

        self._extracted_from_test_get_neo_by_designation_2(
            '2101', 'Adonis', 0.60, True
        )

        self._extracted_from_test_get_neo_by_designation_2(
            '2102', 'Tantalus', 1.649, True
        )

    def _extracted_from_test_get_neo_by_designation_2(self, arg0, arg1, arg2, arg3):
        cerberus = self.db.get_neo_by_designation(arg0)
        self._extracted_from_test_get_neo_by_name_3(cerberus, arg0, arg1)
        self.assertEqual(cerberus.diameter, arg2)
        self.assertEqual(cerberus.hazardous, arg3)

    def test_get_neo_by_designation_missing(self):
        nonexistent = self.db.get_neo_by_designation('not-real-designation')
        self.assertIsNone(nonexistent)

    def test_get_neo_by_designation_neos_with_year(self):
        bs_2020 = self.db.get_neo_by_designation('2020 BS')
        self._extracted_from_test_get_neo_by_name_3_(bs_2020, '2020 BS', None, False)
        py1_2020 = self.db.get_neo_by_designation('2020 PY1')
        self._extracted_from_test_get_neo_by_name_3_(py1_2020, '2020 PY1', None, False)

    # TODO Rename this here and in `test_get_neo_by_designation`, `test_get_neo_by_designation_neos_with_year` and `test_get_neo_by_name`
    def test_get_neo_by_name(self):
        lemmon = self.db.get_neo_by_name('Lemmon')
        self._extracted_from_test_get_neo_by_name_3_(
            lemmon, '2013 TL117', 'Lemmon', False
        )

        jormungandr = self.db.get_neo_by_name('Jormungandr')
        self._extracted_from_test_get_neo_by_name_3_(
            jormungandr, '471926', 'Jormungandr', True
        )

    # TODO Rename this here and in `test_get_neo_by_designation`, `test_get_neo_by_designation_neos_with_year` and `test_get_neo_by_name`
    def _extracted_from_test_get_neo_by_name_3_(self, arg0, arg1, arg2, arg3):
        self._extracted_from_test_get_neo_by_name_3(arg0, arg1, arg2)
        self.assertTrue(math.isnan(arg0.diameter))
        self.assertEqual(arg0.hazardous, arg3)

    # TODO Rename this here and in `test_get_neo_by_designation`, `test_get_neo_by_designation_neos_with_year` and `test_get_neo_by_name`
    def _extracted_from_test_get_neo_by_name_3(self, arg0, arg1, arg2):
        self.assertIsNotNone(arg0)
        self.assertEqual(arg0.designation, arg1)
        self.assertEqual(arg0.name, arg2)

    def test_get_neo_by_name_missing(self):
        nonexistent = self.db.get_neo_by_name('not-real-name')
        self.assertIsNone(nonexistent)


if __name__ == '__main__':
    unittest.main()
