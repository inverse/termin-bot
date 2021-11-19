import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

APPOINTMENTS_URL = "https://service.berlin.de/dienstleistungen/"
BOOKABLE_TEXT = "Termin berlinweit suchen"


logger = logging.getLogger(__name__)


@dataclass
class AppointmentResult:
    appointment: str
    dates: List[datetime]


def fetch_available_appointments(appointments: List[str]) -> List[AppointmentResult]:
    results = []
    for appointment in appointments:
        free_appointments = scrape(appointment)
        if len(free_appointments) != 0:
            results.append(AppointmentResult(appointment, free_appointments))

    return results


def scrape(appointment: str) -> List[datetime]:
    return []


def scrape_appointments() -> Dict[str, str]:
    response = requests.get(APPOINTMENTS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    azlist = soup.find(class_="azlist")
    anchors = azlist.find_all("a")

    appointments = {}
    for anchor in anchors:
        appointment_url = urljoin(APPOINTMENTS_URL, anchor["href"])
        appointment_label = anchor.string
        appointments[appointment_url] = appointment_label.strip()

    logger.info(f"Found {len(appointments)} appointment URls")
    for appointment_url in list(appointments):
        logger.debug(f"Processing: {appointment_url}")
        if not is_appointment_bookable(appointment_url):
            logger.debug(f"Removed: {appointment_url}")

            del appointments[appointment_url]

    logger.info(f"Found bookable {len(appointments)} appointment URls")
    return appointments


def is_appointment_bookable(appointment_url: str) -> bool:
    response = requests.get(appointment_url)

    return BOOKABLE_TEXT in response.text
