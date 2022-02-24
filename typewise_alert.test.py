import unittest
import typewise_alert as ta

from typewise_alert import TypewiseAlert
from CoolingType import passive, med_active, hi_active
from BreachAlert import normal, too_low, too_high


class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        alert = TypewiseAlert()
        self.assertTrue(alert.infer_breach(20, 50, 100) == 'TOO_LOW')
        self.assertTrue(alert.infer_breach(55, 50, 100) == 'NORMAL')
        self.assertTrue(alert.infer_breach(105, 50, 100) == 'TOO_HIGH')

    def test_get_cooling_type_object(self):
        alert = TypewiseAlert()
        self.assertEqual(alert.get_cooling_type_object('PASSIVE_COOLING'), passive)
        self.assertEqual(alert.get_cooling_type_object('HI_ACTIVE_COOLING'), hi_active)
        self.assertEqual(alert.get_cooling_type_object('MED_ACTIVE_COOLING'), med_active)
        self.assertEqual(alert.get_cooling_type_object('Something'), None)

    def test_classify_temperature_breach(self):
        alert = TypewiseAlert()
        self.assertEqual(alert.classify_temperature_breach('PASSIVE_COOLING', 36), 'TOO_HIGH')
        self.assertEqual(alert.classify_temperature_breach('PASSIVE_COOLING', -1), 'TOO_LOW')
        self.assertEqual(alert.classify_temperature_breach('PASSIVE_COOLING', 30), 'NORMAL')

        self.assertEqual(alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46), 'TOO_HIGH')
        self.assertEqual(alert.classify_temperature_breach('HI_ACTIVE_COOLING', -1), 'TOO_LOW')
        self.assertEqual(alert.classify_temperature_breach('HI_ACTIVE_COOLING', 45), 'NORMAL')

        self.assertEqual(alert.classify_temperature_breach('MED_ACTIVE_COOLING', 41), 'TOO_HIGH')
        self.assertEqual(alert.classify_temperature_breach('MED_ACTIVE_COOLING', -1), 'TOO_LOW')
        self.assertEqual(alert.classify_temperature_breach('MED_ACTIVE_COOLING', 40), 'NORMAL')

        with self.assertRaises(SystemExit) as context_manager:
            alert.classify_temperature_breach('Something', 40)
        self.assertEqual(context_manager.exception.code, 0)

    def test_get_alert_object(self):
        alert = TypewiseAlert()
        self.assertEqual(alert.get_alert_object('TOO_LOW'), too_low)
        self.assertEqual(alert.get_alert_object('TOO_HIGH'), too_high)
        self.assertEqual(alert.get_alert_object('NORMAL'), normal)
        self.assertEqual(alert.get_alert_object('HIGH'), None)

    def test_check_and_alert(self):
        alert = TypewiseAlert()

        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'PASSIVE_COOLING'}, -1))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'PASSIVE_COOLING'}, 36))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'PASSIVE_COOLING'}, 35))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'PASSIVE_COOLING'}, 0))

        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'PASSIVE_COOLING'}, -1))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'PASSIVE_COOLING'}, 36))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'PASSIVE_COOLING'}, 35))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'PASSIVE_COOLING'}, 0))

        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'HI_ACTIVE_COOLING'}, -1))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'HI_ACTIVE_COOLING'}, 46))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'HI_ACTIVE_COOLING'}, 45))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'HI_ACTIVE_COOLING'}, 0))

        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'HI_ACTIVE_COOLING'}, -1))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'HI_ACTIVE_COOLING'}, 46))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'HI_ACTIVE_COOLING'}, 45))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'HI_ACTIVE_COOLING'}, 0))

        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'MED_ACTIVE_COOLING'}, -1))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'MED_ACTIVE_COOLING'}, 41))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'MED_ACTIVE_COOLING'}, 40))
        self.assertTrue(alert.check_and_alert('TO_EMAIL', {'cooling_type': 'MED_ACTIVE_COOLING'}, 0))

        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'MED_ACTIVE_COOLING'}, -1))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'MED_ACTIVE_COOLING'}, 41))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'MED_ACTIVE_COOLING'}, 40))
        self.assertTrue(alert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'MED_ACTIVE_COOLING'}, 0))

    def test_mail_server_status_stub(self):
        self.assertEqual(ta.mail_server_status_stub(50), 200)
        self.assertEqual(ta.mail_server_status_stub(51), 500)

        self.assertEqual(ta.mail_server_status_stub(0), 200)
        self.assertEqual(ta.mail_server_status_stub(-6), 500)

    def test_controller_status_stub(self):
        self.assertEqual(ta.controller_status_stub(50), 'OK')
        self.assertEqual(ta.controller_status_stub(51), 'Not OK')

        self.assertEqual(ta.controller_status_stub(0), 'OK')
        self.assertEqual(ta.controller_status_stub(-6), 'Not OK')

    def test_send_to_controller(self):
        self.assertTrue(normal, 40)
        self.assertTrue(too_low, -1)
        self.assertTrue(too_high, 46)

    def test_send_alert_to_email(self):
        alert = TypewiseAlert()
        self.assertTrue(alert.send_alert_to_email(ta.mail_server_status_stub, 50, too_high))
        self.assertFalse(alert.send_alert_to_email(ta.mail_server_status_stub, 51, too_high))
        self.assertTrue(alert.send_alert_to_email(ta.mail_server_status_stub, 0, too_low))
        self.assertFalse(alert.send_alert_to_email(ta.mail_server_status_stub, -6, too_low))

    def test_send_alert_to_controller(self):
        alert = TypewiseAlert()
        self.assertTrue(alert.send_alert_to_controller(ta.controller_status_stub, 50, too_high))
        self.assertFalse(alert.send_alert_to_controller(ta.controller_status_stub, 51, too_high))
        self.assertTrue(alert.send_alert_to_controller(ta.controller_status_stub, 0, too_low))
        self.assertFalse(alert.send_alert_to_controller(ta.controller_status_stub, -6, too_low))


if __name__ == '__main__':
    unittest.main()
