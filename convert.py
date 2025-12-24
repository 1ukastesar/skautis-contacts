#!/usr/bin/env python3
"""
SkautIS Contacts Converter

Converts SkautIS Excel export to Google Contacts CSV format.

Author: Lukas Tesar <lukastesar03@gmail.com>
"""

import argparse
import os
import sys

import pandas as pd


class ConversionError(Exception):
    """Exception raised when conversion fails."""

    pass


# Error handler for CLI mode
def die(error):
    """Print error message and exit."""
    print(f"\033[31;1mERROR:\033[0m {error}", file=sys.stderr)
    sys.exit(1)


def convert(input_path: str, output_path: str) -> None:
    """
    Convert SkautIS Excel export to Google Contacts CSV format.

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
        # First, we (try to) load the input file and parse it into DataFrame (pd)
        skip_rows = 6
        use_cols = [0, 1, 2, 4, 7, 8, 9, 10, 11, 12, 13]
        df = pd.read_excel(
            input_path,
            skiprows=range(0, skip_rows),
            usecols=use_cols,
            dtype={
                "Matka: telefon": str,
                "Otec: telefon": str,
                "Telefon / mobil (hlavní)": str,
            },
        )

        # Then we'll make it look like a Google CSV:
        # - some columns we'll rename
        rename_rules = {
            "Jméno": "Given Name",
            "Příjmení": "Family Name",
            "Přezdívka": "Nickname",
            "Jednotka": "Group Membership",
            "Kategorie": "Category",
            "E-mail (hlavní)": "E-mail 1 - Value",
            "Otec: mail": "E-mail 2 - Value",
            "Matka: mail": "E-mail 3 - Value",
            "Telefon / mobil (hlavní)": "Phone 1 - Value",
            "Otec: telefon": "Phone 2 - Value",
            "Matka: telefon": "Phone 3 - Value",
        }
        df.rename(columns=rename_rules, inplace=True)

        # - some just need to be added (with no values, in most cases)
        add_cols = [
            [0, "Name", ""],
            [2, "Additional Name", ""],
            [4, "Yomi Name", ""],
            [5, "Given Name Yomi", ""],
            [6, "Additional Name Yomi", ""],
            [7, "Family Name Yomi", ""],
            [8, "Name Prefix", ""],
            [9, "Name Suffix", ""],
            [10, "Initials", ""],
            [12, "Short Name", ""],
            [13, "Maiden Name", ""],
            [14, "Birthday", ""],
            [15, "Gender", ""],
            [16, "Location", ""],
            [17, "Billing Information", ""],
            [18, "Mileage", ""],
            [19, "Occupation", ""],
            [20, "Hobby", ""],
            [21, "Sensitivity", ""],
            [22, "Priority", ""],
            [23, "Subject", ""],
            [24, "Notes", ""],
            [25, "Language", ""],
            [26, "Photo", ""],
            [28, "E-mail 1  - Type", "Dítě"],
            [29, "Phone 1 - Type", "Dítě"],
            [30, "E-mail 2 - Type", "Otec"],
            [31, "Phone 2 - Type", "Otec"],
            [32, "E-mail 3 - Type", "* Matka"],
            [33, "Phone 3 - Type", "* Matka"],
        ]
        for col in add_cols:
            df.insert(col[0], col[1], col[2])

        # - this one combines values from two other columns instead (Given + Family name = Full name)
        df["Name"] = df["Given Name"] + " " + df["Family Name"]

        # - replace singular with plural in category
        # Avoid inplace on a Series (pandas will warn about chained assignment).
        # Assign the replaced Series back to the DataFrame to ensure we operate
        # on the original object (compatible with pandas 3.0 behavior).
        df["Category"] = df["Category"].replace(
            {"Vlče": "Vlčata", "Skaut": "Skauti", "Rover": "Roveři"}
        )

        # - and some need bigger changes (combining, renaming and adding values)
        df["Group Membership"] = df.apply(
            lambda row: f"{row['Group Membership']} ::: {row['Category']} ::: * myContacts",
            axis=1,
        )

        # - add +420 in the beginning of telephone numbers to be recognized correctly
        for i in [1, 2, 3]:
            key = f"Phone {i} - Value"
            df[key] = df[key].apply(
                lambda num: f"+420{str(num)}" if pd.notna(num) and num else ""
            )

        # - as a last thing, we drop the columns we no longer need
        df.drop(columns="Category", inplace=True)

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
        # We'll try to export it as csv and write to given path
        df.to_csv(output_path, index=None, header=True)
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
