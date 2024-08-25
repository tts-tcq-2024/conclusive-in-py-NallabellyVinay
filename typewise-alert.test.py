import unittest
import typewise-alert


class TypewiseTest(unittest.TestCase):

    def test_infers_breach_as_too_low(self):
        self.assertEqual(typewise-alert.infer_breach(20, 50, 100), 'TOO_LOW')

    def test_infers_breach_as_too_high(self):
        self.assertEqual(typewise-alert.infer_breach(120, 50, 100), 'TOO_HIGH')

    def test_infers_breach_as_normal(self):
        self.assertEqual(typewise-alert.infer_breach(75, 50, 100), 'NORMAL')

    def test_classify_temperature_breach_for_passive_cooling(self):
        self.assertEqual(typewise-alert.classify_temperature_breach('PASSIVE_COOLING', 30), 'NORMAL')
        self.assertEqual(typewise-alert.classify_temperature_breach('PASSIVE_COOLING', 40), 'TOO_HIGH')
        self.assertEqual(typewise-alert.classify_temperature_breach('PASSIVE_COOLING', -5), 'TOO_LOW')

    def test_classify_temperature_breach_for_hi_active_cooling(self):
        self.assertEqual(typewise-alert.classify_temperature_breach('HI_ACTIVE_COOLING', 30), 'NORMAL')
        self.assertEqual(typewise-alert.classify_temperature_breach('HI_ACTIVE_COOLING', 50), 'TOO_HIGH')

    def test_classify_temperature_breach_for_med_active_cooling(self):
        self.assertEqual(typewise-alert.classify_temperature_breach('MED_ACTIVE_COOLING', 30), 'NORMAL')
        self.assertEqual(typewise-alert.classify_temperature_breach('MED_ACTIVE_COOLING', 45), 'TOO_HIGH')

    def test_check_and_alert_to_controller(self):
        with self.assertLogs() as log:
            typewise-alert.send_to_controller('TOO_HIGH')
            self.assertIn('feed, TOO_HIGH', log.output[0])

    def test_check_and_alert_to_email(self):
        with self.assertLogs() as log:
            typewise-alert.send_to_email('TOO_HIGH')
            self.assertIn('Hi, the temperature is too high', log.output[1])

    def test_invalid_cooling_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            typewise-alert.classify_temperature_breach('INVALID_COOLING', 30)

    def test_invalid_alert_target_raises_value_error(self):
        with self.assertRaises(ValueError):
            typewise-alert.get_alert_method('INVALID_ALERT_TARGET')


if __name__ == '__main__':
    unittest.main()
