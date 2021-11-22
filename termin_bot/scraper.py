import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from termin_bot.util import month_convert

APPOINTMENTS_URL = "https://service.berlin.de/dienstleistungen/"
BOOKABLE_TEXT = "Termin berlinweit suchen"
URL_PATTERN = re.compile(r"^https://service.berlin.de/dienstleistung/\d+/$")

BOOKABLE_CLASS = "buchbar"

logger = logging.getLogger(__name__)


@dataclass
class AppointmentResult:
    appointment_identifier: int
    dates: List[datetime]


def fetch_available_appointments(appointments: List[int]) -> List[AppointmentResult]:
    results = []
    for appointment in appointments:
        free_appointments = scrape(f"{APPOINTMENTS_URL}{appointment}")
        if len(free_appointments) != 0:
            results.append(AppointmentResult(appointment, free_appointments))

    return results


def scrape(url: str) -> List[datetime]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    result = []
    for cal_table in soup.find_all(class_="calendar-month-table"):
        month_year = month_convert(cal_table.find(class_="month").string.strip())
        next_element = cal_table.find(class_="next")
        if next_element and next_element.find("a"):
            result += scrape(next_element.find("a")["href"])

        for cell in cal_table.find_all("td"):
            if "class" not in cell.attrs:
                continue

            if BOOKABLE_CLASS not in cell.attrs["class"]:
                continue

            date_string = f"{cell.string.strip()} {month_year}"
            result.append(datetime.strptime(date_string, "%d %B %Y"))

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

    total_appointments = len(appointments)
    logger.info(f"Found {total_appointments} appointment URls")
    for index, appointment in enumerate(appointments):
        logger.debug(f"Processing: [{index}/{total_appointments}] {appointment.url}")
        if not is_appointment_bookable(appointment.url):
            logger.debug(f"Removed: {appointment.url}")

            del appointments[index]

    total_appointments = len(appointments)
    logger.info(f"Found bookable {total_appointments} appointment URls")
    return appointments


def is_appointment_bookable(appointment_url: str) -> bool:
    response = requests.get(appointment_url)

    return BOOKABLE_TEXT in response.text
