import csv
import re

from mypy.server.objgraph import Iterable

from checksum import (
    calculate_checksum,
    serialize_result
)


def is_row_valid(row: dict[str, str]):
    processors = {
        "email": "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$",
        "height": "^\\d\\.\\d{2}$",
        "snils": "^\\d{11}$",
        "passport": "^\\d{2} \\d{2} \\d{6}$",
        "occupation": "^[А-Яа-яA-Za-z\\s\\-]+$",
        "longitude": "^-?\\d+(\\.\\d+)?$",
        "hex_color": "^#[0-9a-fA-F]{6}$",
        "issn": "^\\d{4}-\\d{4}$",
        "locale_code": "^[a-z]{2}-[A-Z]{2}$",
        "time": "^\\d{2}:\\d{2}:\\d{2}\\.\\d{6}$"
    }
    for field_name, processor in processors.items():
        if re.fullmatch(processor, row[field_name]) is None:
            return False
    return True