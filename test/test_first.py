import unittest

def addition(a, b):
    return a + b

class TestAddition(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(addition(2, 3), 5)
        self.assertEqual(addition(-1, 1), 0)
        self.assertEqual(addition(0, 0), 0)

if __name__ == '__main__':
    unittest.main()
