from unittest import TestCase
from main import Salary


class SalaryTests(TestCase):
    def test_salary_type(self):
        self.assertEqual(type(Salary(10, 20, 'RUR')).__name__, 'Salary')

    def test_salary_from(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_from, 10)

    def test_salary_to(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_to, 20)

    def test_salary_currency(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_currency, 'RUR')

    def test_int_get_salary(self):
        self.assertEqual(Salary(10, 20, 'RUR').get_salary_to_rub(), 15.0)

    def test_float_salary_from_in_get_salary(self):
        self.assertEqual(Salary(10.0, 20, 'RUR').get_salary_to_rub(), 15.0)

    def test_float_salary_to_in_get_salary(self):
        self.assertEqual(Salary(10, 30.0, 'RUR').get_salary_to_rub(), 20.0)

    def test_currency_in_get_salary(self):
        self.assertEqual(Salary(10, 30.0, 'EUR').get_salary_to_rub(), 1198.0)