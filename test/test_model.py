import unittest
from importlib import reload

from pony.orm import Database, db_session

from termin_bot import model


def setup_test_database(db: Database):
    db.bind(provider="sqlite", filename=":memory:")
    db.generate_mapping(create_tables=True)


class TestModels(unittest.TestCase):

    TEST_TELEGRAM_USERNAME = "iamtelegram"

    TEST_APPOINTMENT_1 = "something-important-1"
    TEST_APPOINTMENT_2 = "something-important-2"

    def setUp(self) -> None:
        reload(model)
        setup_test_database(model.db)
        with db_session:
            user = model.User(telegram_username=self.TEST_TELEGRAM_USERNAME)
            model.Termin(appointment=self.TEST_APPOINTMENT_1, user=user)
            model.Termin(appointment=self.TEST_APPOINTMENT_2, user=user)

    def test_find_user_termins(self):
        result = model.find_user_appointments(self.TEST_TELEGRAM_USERNAME)
        self.assertTrue(len(result) == 2)
        self.assertEqual(self.TEST_APPOINTMENT_1, result[1])
        self.assertEqual(self.TEST_APPOINTMENT_2, result[0])

    def test_remove_user_appointment(self):
        model.remove_user_appointment(
            self.TEST_TELEGRAM_USERNAME, self.TEST_APPOINTMENT_1
        )

        result = model.find_user_appointments(self.TEST_TELEGRAM_USERNAME)
        self.assertTrue(len(result) == 1)
        self.assertEqual(self.TEST_APPOINTMENT_2, result[0])

    def test_delete_user(self):
        model.delete_user(self.TEST_TELEGRAM_USERNAME)
        with self.assertRaises(ValueError):
            model.find_user(self.TEST_TELEGRAM_USERNAME)