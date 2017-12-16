import unittest
import scheduling


class GetForecastDataTest(unittest.TestCase):
    def test_get_forecast_data(self):
        input_api_key = "1fbed46a06fcec66"
        input_location = "CA/San_Francisco"

        actual = scheduling.get_forecast_data(input_api_key, input_location)
        self.assertIsInstance(actual['high_temp'], int)
        self.assertIsInstance(actual['low_temp'], int)
        self.assertIsInstance(actual['average_hum'], int)


class AddMinutesTest(unittest.TestCase):
    def test_add_minutes(self):
        input_time = "0830"
        input_minutes = 30
        expected = "0900"

        actual = scheduling.add_minutes(input_time, input_minutes)
        self.assertEqual(expected, actual)


class AdjustTimeTest(unittest.TestCase):
    def test_adjust_time(self):
        input_schedule = {'conditions': {'high_temp': '20', 'low_temp': '12', 'average_hum': '75'},
                          'schedule': [{'start': '0700', 'end': '0830', 'duration': '90'},
                                       {'start': '2000', 'end': '2100', 'duration': '60'}]}
        input_forecast = {'high_temp': 21, 'low_temp': 18, 'average_hum': 94}
        expected = {'conditions': {'high_temp': '20', 'low_temp': '12', 'average_hum': '75'},
                    'schedule': [{'start': '0700', 'end': '0835', 'duration': '90'},
                                 {'start': '2000', 'end': '2100', 'duration': '60'}]}

        actual = scheduling.adjust_time(input_schedule, input_forecast)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
