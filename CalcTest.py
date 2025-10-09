import unittest
from Calc import Calculator  # The class we are going to implement

class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Calculator()
        result = calc.add(2, 3)
        self.assertEqual(result, 5)  # Expect 2 + 3 = 5

    def test_subtract(self):
        calc = Calculator()
        result = calc.subtract(5, 3)
        self.assertEqual(result, 2) # Expect 5 - 3 = 2

    def test_multiply(self):
        calc = Calculator()
        result = calc.multiply(2, 5)
        self.assertEqual(result, 10)    # Expect 2 * 5 = 10
    
    def test_divide(self):
        calc = Calculator()
        result = calc.divide(10, 2)
        self.assertEqual(result, 5.0)   # Expect 10 / 2 = 5.0(float)

    def test_divide_by_zero(self):  # Expect divide 0 to raise exception
        calc = Calculator()
        with self.assertRaises(ZeroDivisionError):
            calc.divide(5, 0)

if __name__ == "__main__":
    unittest.main()