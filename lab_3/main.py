import csv
import re

from mypy.server.objgraph import Iterable

from checksum import (
    calculate_checksum,
    serialize_result
)


def is_row_valid(row: dict[str, str]) -> bool:
    """Tests a CSV string against the specified regular expressions."""
    processors = {
        "email": "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$",
        'height': "^[1-2]\\.\\d{2}$",
        "snils": "^\\d{11}$",
        "passport": "^\\d{2} \\d{2} \\d{6}$",
        "occupation": "^[А-Яа-яA-Za-z\\s\\-]+$",
        "longitude": "^(-?(180(\\.0{1,6})?|(1[0-7]\\d|\\d{1,2})(\\.\\d{1,6})?))$",
        "hex_color": "^#[0-9a-fA-F]{6}$",
        "issn": "^\\d{4}-\\d{4}$",
        "locale_code": "^[a-z]{2}(-[a-z]{2}?)?$",
        "time": "^(2[0-3]|[01]\\d):([0-5]\\d):([0-5]\\d)(\\.\\d{1,6})?$"
    }
    for field_name, processor in processors.items():
        if re.fullmatch(processor, row[field_name]) is None:
            return False
    return True


def get_wrong_lines() -> Iterable[int]:
    """Returns the line numbers of the CSV file that were not validated."""
    with open("11.csv", mode="r", encoding="utf16", newline="") as file_to_validate:
        strings_reader = csv.DictReader(file_to_validate, delimiter=';')
        for i, row in enumerate(strings_reader):
            if not is_row_valid(row):
                yield i


def main() -> None:
    """The main function of the program. Calculates line numbers with errors,
    calculates the checksum and stores the results."""
    lines = list(get_wrong_lines())
    variant = 11
    checksum = calculate_checksum(lines)
    serialize_result(variant, checksum)


if __name__ == '__main__':
    main()