import unittest

from gencontent import extract_title

class TestGenContent(unittest.TestCase):

    def test_output(self):
        result = extract_title("# The Answer")
        self.assertEqual(result, "The Answer")

    def test_raises_exception(self):
        with self.assertRaises(Exception):
            extract_title("bad input") 


if __name__ == '__main__':
    unittest.main()