from dataclasses import dataclass
from datetime import datetime
from typing import List

from termin_bot.model import Appointment


@dataclass
class ScrapedAppointment:
    url: str
    label: str
    name: str
    identifier: int


@dataclass
class AppointmentResult:
    appointment: Appointment
    dates: List[datetime]
