import unittest
from unittest.mock import Mock, patch

import responses

from termin_bot import scraper

from .utils import load_fixture


class ScraperTest(unittest.TestCase):
    @patch("termin_bot.scraper.is_appointment_bookable")
    def test_scrape_appointments(self, mock_is_appointment_bookable: Mock):
        responses.add(
            responses.GET,
            scraper.APPOINTMENTS_URL,
            body=load_fixture("dienstleistungen.html"),
        )

        mock_is_appointment_bookable.return_value = True
        scraper.scrape_appointments()

        self.assertTrue(True)

    def test_is_appointment_bookable(self):
        responses.add(
            responses.GET,
            "https://service.berlin.de/dienstleistung/120335/",
            body=load_fixture("bookable_appointment.html"),
        )
        self.assertTrue(
            scraper.is_appointment_bookable(
                "https://service.berlin.de/dienstleistung/120335/"
            )
        )

    def test_scrape(self):
        responses.add(
            responses.GET,
            "https://service.berlin.de/terminvereinbarung/termin/day/",
            body=load_fixture("appointment_termin.html"),
        )

        scraper.scrape("https://service.berlin.de/terminvereinbarung/termin/day/") # TODO: Redirect needs to be handled
