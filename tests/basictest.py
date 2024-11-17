import unittest

class BasicTest(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(4+4, 8)

    

if __name__ == '__main__':
    unittest.main()