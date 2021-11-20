import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

APPOINTMENTS_URL = "https://service.berlin.de/dienstleistungen/"
BOOKABLE_TEXT = "Termin berlinweit suchen"
URL_PATTERN = re.compile(r"^https://service.berlin.de/dienstleistung/\d+/$")

BOOKABLE_CLASS = "buchbar"

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
    response = requests.get(appointment)
    soup = BeautifulSoup(response.text, "html.parser")

    result = []
    for cal_table in soup.find_all(class_="calendar-month-table"):
        for cell in cal_table.find_all("td"):
            if "class" not in cell.attrs:
                continue

            if BOOKABLE_CLASS not in cell.attrs["class"]:
                continue

            result.append(datetime.now())  ## TODO Contruct URL

    return result


@dataclass
class ScrapedAppointment:
    url: str
    label: str
    name: str
    identifier: int


def scrape_appointments() -> List[ScrapedAppointment]:
    response = requests.get(APPOINTMENTS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    azlist = soup.find(class_="azlist")
    anchors = azlist.find_all("a")

    appointments: List[ScrapedAppointment] = []
    for anchor in anchors:
        url = urljoin(APPOINTMENTS_URL, anchor["href"])
        if not URL_PATTERN.match(url):
            logger.debug(f"Skipping {url}")
            continue

        label = anchor.string.strip()
        name = label.lower().replace(" ", "_")
        split = url.rsplit("/")[-2]
        identifier = int(split)
        appointments.append(ScrapedAppointment(url, label, name, identifier))

    logger.info(f"Found {len(appointments)} appointment URls")
    for index, appointment in enumerate(appointments):
        logger.debug(f"Processing: {appointment.url}")
        if not is_appointment_bookable(appointment.url):
            logger.debug(f"Removed: {appointment.url}")

            del appointments[index]

    logger.info(f"Found bookable {len(appointments)} appointment URls")
    return appointments


def is_appointment_bookable(appointment_url: str) -> bool:
    response = requests.get(appointment_url)

    return BOOKABLE_TEXT in response.text
