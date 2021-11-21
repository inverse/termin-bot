def month_convert(month_str: str) -> str:
    mapper = {
        "Januar": "January",
        "Februar": "February",
        "März": "March",
        "April": "April",
        "Mai": "May",
        "Juni": "June",
        "Juli": "July",
        "August": "August",
        "September": "September",
        "Oktober": "October",
        "November": "November",
        "Dezember": "December",
    }

    for month, replace in mapper.items():
        if month in month_str:
            month_str = month_str.replace(month, replace)

    return month_str
