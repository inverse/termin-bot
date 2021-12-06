from termin_bot.scraper import AppointmentResult


def get_notification_message(result: AppointmentResult) -> str:
    dates = ""
    for date in result.dates:
        dates += f"- {date}\n"

    notification_message = f"""Appointment found for {result.appointment_url} on the following dates:
{dates}"""

    return notification_message
