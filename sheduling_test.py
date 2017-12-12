import unittest
import scheduling


class AddMinutesTest(unittest.TestCase):

    def test_add_minutes(self):
        input_time = "0830"
        input_minutes = 30
        expected = "0900"

        actual = scheduling.add_minutes(input_time, input_minutes)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
