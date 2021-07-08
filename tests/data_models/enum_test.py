import sys

sys.path.append("..")
import unittest
from src.data_models.enum_tables.degree_type import *
from src.data_models.enum_tables.major import *
from src.data_models.enum_tables.school import *


class DataModelsEnumTest(unittest.TestCase):
    def test_degree_type(self):
        self.assertEqual(from_code_to_degree_type_name(0), "UNKNOWN")
        self.assertEqual(from_code_to_degree_type_name(1000000), "UNKNOWN")
        self.assertEqual(from_code_to_degree_type_name(8), "Professional")

    def test_major(self):
        self.assertEqual(from_code_to_major_name(0), "UNKNOWN")
        self.assertEqual(from_code_to_major_name(50000000), "UNKNOWN")
        self.assertEqual(from_code_to_major_name(6), "Data Science")

    def test_school(self):
        self.assertEqual(from_code_to_school_name(0), "UNKNOWN")
        self.assertEqual(from_code_to_school_name(7958245), "UNKNOWN")
        self.assertEqual(
            from_code_to_school_name(9), "University of California, San Francisco"
        )


if __name__ == "__main__":
    unittest.main()
