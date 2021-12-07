import unittest
from datetime import datetime

from termin_bot import message
from termin_bot.scraper import AppointmentResult


class TestMessage(unittest.TestCase):
    def test_get_notification_message(self):
        result = AppointmentResult(1, "https://example.com/1", [datetime(2021, 1, 1)])

        expected_message = """Appointment found for https://example.com/1 on the following dates:
- 2021-01-01 00:00:00
"""

        self.assertEqual(expected_message, message.get_notification_message(result))
