import unittest
from importlib import reload

from pony.orm import Database, db_session

from termin_bot import model
from termin_bot.exceptions import MaxTerminException


def setup_test_database(db: Database):
    db.bind(provider="sqlite", filename=":memory:")
    db.generate_mapping(create_tables=True)


@db_session
class TestModels(unittest.TestCase):

    TEST_TELEGRAM_ID = 123456789

    TEST_APPOINTMENT_1 = "something-important-1"
    TEST_APPOINTMENT_1_IDENTIFIER = 123
    TEST_APPOINTMENT_2 = "something-important-2"
    TEST_APPOINTMENT_2_IDENTIFIER = 124
    TEST_APPOINTMENT_3 = "something-important-3"
    TEST_APPOINTMENT_3_IDENTIFIER = 125

    def setUp(self) -> None:
        reload(model)
        setup_test_database(model.db)
        user = model.User(telegram_id=self.TEST_TELEGRAM_ID)
        appointment_1 = model.Appointment(
            name=self.TEST_APPOINTMENT_1,
            label="Something Important 1",
            identifier=self.TEST_APPOINTMENT_1_IDENTIFIER,
        )
        appointment_2 = model.Appointment(
            name=self.TEST_APPOINTMENT_2,
            label="Something Important 2",
            identifier=self.TEST_APPOINTMENT_2_IDENTIFIER,
        )
        model.Appointment(
            name=self.TEST_APPOINTMENT_3,
            label="Something Important 3",
            identifier=self.TEST_APPOINTMENT_3_IDENTIFIER,
        )
        model.Termin(appointment=appointment_1, user=user)
        model.Termin(appointment=appointment_2, user=user)

    def test_find_user_termins(self):
        result = model.find_user_subscriptions(self.TEST_TELEGRAM_ID)
        self.assertEqual(2, len(result))
        self.assertTrue(self.TEST_APPOINTMENT_1 in [r.label for r in result])
        self.assertTrue(self.TEST_APPOINTMENT_2 in [r.label for r in result])

    def test_remove_user_appointment(self):
        model.remove_user_appointment(self.TEST_TELEGRAM_ID, self.TEST_APPOINTMENT_1)

        result = model.find_user_subscriptions(self.TEST_TELEGRAM_ID)
        self.assertEqual(1, len(result))
        self.assertEqual(self.TEST_APPOINTMENT_2, result[0].label)

    def test_delete_user(self):
        model.delete_user(self.TEST_TELEGRAM_ID)
        self.assertIsNone(model.find_user(self.TEST_TELEGRAM_ID))

    def test_find_appointments(self):
        result = model.find_appointments()
        self.assertEqual(2, len(result))

    def test_find_users_for_appointment(self):
        result = model.find_users_for_appointment(self.TEST_APPOINTMENT_1_IDENTIFIER)
        self.assertEqual(1, len(result))
        self.assertEqual(self.TEST_TELEGRAM_ID, result[0].telegram_id)

    def test_add_user_appointment(self):
        model.add_user_appointment(self.TEST_TELEGRAM_ID, self.TEST_APPOINTMENT_3)
        result = model.find_user_subscriptions(self.TEST_TELEGRAM_ID)
        self.assertEqual(3, len(result))

        with self.assertRaises(MaxTerminException):
            model.add_user_appointment(self.TEST_TELEGRAM_ID, self.TEST_APPOINTMENT_3)


class TestAppointments(unittest.TestCase):
    def test_get_appointments_empty(self):
        appointments = model.Appointments([{}])
        self.assertEqual([], appointments.get_appointment_names())

    def test_get_paginated_appointments_empty(self):
        appointments = model.Appointments([{}])
        self.assertEqual([{}], appointments.get_paginated_appointments(0))

    def test_get_paginated_appointments_paged(self):
        appointments = model.Appointments(
            [
                {"a": "label-a"},
                {"b": "label-b"},
                {"c": "label-c"},
            ]
        )
        self.assertEqual(
            [{"a": "label-a"}], appointments.get_paginated_appointments(0, 1)
        )
        self.assertEqual(
            [{"b": "label-b"}], appointments.get_paginated_appointments(1, 1)
        )
        self.assertEqual(
            [{"c": "label-c"}], appointments.get_paginated_appointments(2, 1)
        )

    def test_get_paginated_appointments_under(self):
        appointments = model.Appointments(
            [
                {"a": "label-a"},
                {"b": "label-b"},
                {"c": "label-c"},
            ]
        )
        self.assertEqual([], appointments.get_paginated_appointments(-1, 1))

    def test_get_paginated_appointments_over(self):
        appointments = model.Appointments(
            [
                {"a": "label-a"},
                {"b": "label-b"},
                {"c": "label-c"},
            ]
        )
        self.assertEqual([], appointments.get_paginated_appointments(3, 1))
