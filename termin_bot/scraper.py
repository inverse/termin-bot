from dataclasses import dataclass
from datetime import datetime
from typing import List


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
