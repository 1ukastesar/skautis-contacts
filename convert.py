#!/usr/bin/env python3
"""
SkautIS Contacts Converter

Converts SkautIS Excel export to Google Contacts CSV format.

Author: Lukas Tesar <lukastesar03@gmail.com>
"""

import argparse
import os
import re
import sys

import openpyxl
import pandas as pd


class ConversionError(Exception):
    """Exception raised when conversion fails."""

    pass


# Error handler for CLI mode
def die(error):
    """Print error message and exit."""
    print(f"\033[31;1mERROR:\033[0m {error}", file=sys.stderr)
    sys.exit(1)


GOOGLE_CONTACTS_COLUMNS = [
    "Name",
    "Given Name",
    "Additional Name",
    "Family Name",
    "Yomi Name",
    "Given Name Yomi",
    "Additional Name Yomi",
    "Family Name Yomi",
    "Name Prefix",
    "Name Suffix",
    "Initials",
    "Nickname",
    "Short Name",
    "Maiden Name",
    "Birthday",
    "Gender",
    "Location",
    "Billing Information",
    "Mileage",
    "Occupation",
    "Hobby",
    "Sensitivity",
    "Priority",
    "Subject",
    "Notes",
    "Language",
    "Photo",
    "Group Membership",
    "E-mail 1 - Type",
    "E-mail 1 - Value",
    "Phone 1 - Type",
    "Phone 1 - Value",
]

CATEGORY_PLURAL_MAP = {
    "Benjamínek": "Benjamínci",
    "Vlče": "Vlčata",
    "Světluška": "Světlušky",
    "Skaut": "Skauti",
    "Skautka": "Skautky",
    "Rover": "Roveři",
    "Ranger": "Rangeři",
}


def clean_str(val: object) -> str:
    """Clean and strip string value, treating NaN / None as empty."""
    if pd.isna(val):
        return ""
    s = str(val).strip()
    return "" if s.lower() == "nan" else s


def format_phone(val: object) -> str:
    """Format phone number with country code."""
    s = clean_str(val)
    if not s:
        return ""
    if s.endswith(".0"):
        s = s[:-2]
    # Remove whitespace, hyphens, and dots
    s = re.sub(r"[\s\-\.]+", "", s)
    if not s:
        return ""
    if s.startswith("+"):
        return s
    if s.startswith("00"):
        return f"+{s[2:]}"
    return f"+420{s}"


def clean_email(val: object) -> str:
    """Clean and strip email address."""
    return clean_str(val)


def detect_header_row(file_path: str) -> int:
    """
    Find the 0-indexed row containing table headers ('Jméno' and 'Příjmení').
    Returns 6 (row 7 in Excel) as fallback.
    """
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        ws = wb.active
        for idx, row in enumerate(ws.iter_rows(values_only=True)):
            if row and "Jméno" in row and "Příjmení" in row:
                wb.close()
                return idx
        wb.close()
    except Exception:
        pass
    return 6


def convert(input_path: str, output_path: str) -> None:
    """
    Convert SkautIS Excel export to Google Contacts CSV format.

    Each child's contacts (child, father, mother) are split into individual entries
    formatted as 'Jméno dítěte - Matka/Otec/Dítě'.

    Args:
        input_path: Path to input Excel file (.xlsx)
        output_path: Path for output CSV file

    Raises:
        ConversionError: If conversion fails
        FileNotFoundError: If input file not found
        IOError: If I/O error occurs
    """
    # Check if input_path exists
    if not os.path.exists(input_path):
        abs_path = os.path.abspath(input_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Input path doesn't exist: {input_path}")
        input_path = abs_path

    try:
        header_row = detect_header_row(input_path)
        df_raw = pd.read_excel(
            input_path,
            skiprows=range(0, header_row),
            dtype=str,
        )

        output_rows = []

        if not df_raw.empty and "Jméno" in df_raw.columns:
            for _, row in df_raw.iterrows():
                given_name = clean_str(row.get("Jméno"))
                family_name = clean_str(row.get("Příjmení"))
                child_name = f"{given_name} {family_name}".strip()
                nickname = clean_str(row.get("Přezdívka"))
                jednotka = clean_str(row.get("Jednotka"))
                category = clean_str(row.get("Kategorie"))
                category_plural = CATEGORY_PLURAL_MAP.get(category, category)

                group_parts = []
                if jednotka:
                    group_parts.append(jednotka)
                if category_plural:
                    group_parts.append(category_plural)
                group_parts.append("* myContacts")
                group_membership = " ::: ".join(group_parts)

                contacts = [
                    (
                        "Dítě",
                        format_phone(row.get("Telefon / mobil (hlavní)")),
                        clean_email(row.get("E-mail (hlavní)")),
                    ),
                    (
                        "Otec",
                        format_phone(row.get("Otec: telefon")),
                        clean_email(row.get("Otec: mail")),
                    ),
                    (
                        "Matka",
                        format_phone(row.get("Matka: telefon")),
                        clean_email(row.get("Matka: mail")),
                    ),
                ]

                for role, phone, email in contacts:
                    if phone or email:
                        contact_name = f"{child_name} - {role}" if child_name else role
                        contact_family = f"{family_name} - {role}".strip() if family_name else role
                        row_dict = {
                            "Name": contact_name,
                            "Given Name": given_name,
                            "Additional Name": "",
                            "Family Name": contact_family,
                            "Yomi Name": "",
                            "Given Name Yomi": "",
                            "Additional Name Yomi": "",
                            "Family Name Yomi": "",
                            "Name Prefix": "",
                            "Name Suffix": "",
                            "Initials": "",
                            "Nickname": nickname,
                            "Short Name": "",
                            "Maiden Name": "",
                            "Birthday": "",
                            "Gender": "",
                            "Location": "",
                            "Billing Information": "",
                            "Mileage": "",
                            "Occupation": "",
                            "Hobby": "",
                            "Sensitivity": "",
                            "Priority": "",
                            "Subject": "",
                            "Notes": "",
                            "Language": "",
                            "Photo": "",
                            "Group Membership": group_membership,
                            "E-mail 1 - Type": "Home" if email else "",
                            "E-mail 1 - Value": email,
                            "Phone 1 - Type": "Mobile" if phone else "",
                            "Phone 1 - Value": phone,
                        }
                        output_rows.append(row_dict)

        df_out = pd.DataFrame(output_rows, columns=GOOGLE_CONTACTS_COLUMNS)

    except FileNotFoundError:
        raise FileNotFoundError("Input file not found.")
    except IOError:
        raise IOError(
            "An I/O error occurred when trying to open the input file. Maybe it is already used by another process?"
        )
    except Exception as e:
        raise ConversionError(
            f"An error occurred when trying to open and parse the input file: {str(e)}"
        )

    # Everything done, save it
    try:
        output_dir = os.path.dirname(os.path.abspath(output_path))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        df_out.to_csv(output_path, index=False, header=True)
    except IOError:
        raise IOError(
            "An I/O error occurred when trying to save the output file. Maybe it is already used by another process?"
        )
    except Exception as e:
        raise ConversionError(f"An error occurred when trying to save the output file: {str(e)}")


def main():
    """CLI entry point for the converter."""
    parser = argparse.ArgumentParser(
        description="Convert SkautIS Excel export to Google Contacts CSV format."
    )
    parser.add_argument(
        "input",
        help="input file path, desired data format is Excel spreadsheet (.xlsx)",
    )
    parser.add_argument(
        "output",
        help="output file path, data will be exported in Google Contacts CSV (.csv) format",
    )

    args = parser.parse_args()

    try:
        convert(args.input, args.output)
        print(f"Successfully converted {args.input} to {args.output}")
    except (FileNotFoundError, IOError, ConversionError) as e:
        die(str(e))


if __name__ == "__main__":
    main()
