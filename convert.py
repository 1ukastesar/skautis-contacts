#!/usr/bin/env python3

import argparse
import os
import sys

import pandas as pd

APP_NAME = "skautIS to Google Contacts CSV converter"
APP_VERSION = 2.8
AUTHOR = "Lukáš Tesař <lukastesar@skaut.cz>"

SKIP_ROWS = 6
USE_COLS = [0, 1, 2, 4, 7, 8, 9, 10, 11, 12, 13]

COL_RENAME_RULES = {
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

ADD_COLS = [
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

# Error handler
def die(error):
    if not quiet:
        print(f"\033[31;1mERROR:\033[0m {error}", file=sys.stderr)
    sys.exit(1)

# Info print

def iprint(msg: str):
    if not quiet:
        print(msg, file=sys.stderr)

parser = argparse.ArgumentParser()
# INPUT and OUTPUT file arguments
parser.add_argument(
    "input", help="input file path, desired data format is Excel spreadsheet (.xlsx)"
)
parser.add_argument(
    "output",
    help="output file path, data will be exported in Google Contacts CSV (.csv) format",
)

parser.add_argument(
    "-q",
    "--quiet",
    help="be quiet; do NOT print ANY information about the whole process (default False)",
    action="store_true",
)

args = parser.parse_args()

quiet = args.quiet
input_path = args.input
output_path = args.output

iprint(f"{APP_NAME}, v{str(APP_VERSION)}")
iprint(f"Made with <3 by {AUTHOR}\n")

iprint(f"Loading the input file: {input_path}")

# Check if input_path exists
if not os.path.exists(input_path):
    input_path = os.path.abspath(input_path)
    if not os.path.exists(input_path):
        die("Input path doesn't exist.")

try:
    try:
        # First, we (try to) load the input file and parse it into DataFrame (pd)
        input = pd.read_excel(
            input_path,
            skiprows=range(0, SKIP_ROWS),
            usecols=USE_COLS,
            dtype={
                "Matka: telefon": str,
                "Otec: telefon": str,
                "Telefon / mobil (hlavní)": str,
            },
        )
    except FileNotFoundError:
        die("Input file not found.")
    except IOError:
        die(
            "An I/O error occured when trying to open the input file. Maybe it is already used by another process?"
        )

    iprint("Processing...")

    # Then we'll make it look like a Google CSV:
    # - some columns we'll rename
    input.rename(columns=COL_RENAME_RULES, inplace=True)

    # - some just need to be added (with no values, in most cases)
    for col in ADD_COLS:
        input.insert(col[0], col[1], col[2])

    # - this one combines values from two other columns instead (Given + Family name = Full name)
    input["Name"] = input["Given Name"] + " " + input["Family Name"]

    # - replace singular with plural in category
    input["Category"].replace(
        {"Vlče": "Vlčata", "Skaut": "Skauti", "Rover": "Roveři"}, inplace=True
    )

    # - and some need bigger changes (combining, renaming and adding values)
    input["Group Membership"] = input.apply(
        lambda row: f"{row['Group Membership']} ::: {row['Category']} ::: * myContacts",
        axis=1
    )

    iprint("A few more changes to be done...")

    # - add +420 in the beginning of telephone numbers to be recognized correctly
    for i in [1, 2, 3]:
        key = f"Phone {i} - Value"
        input[key] = input[key].apply(lambda num: f"+420{str(num)}" if pd.notna(num) and num else "")

    # - as a last thing, we drop the columns we no longer need
    input.drop(columns="Category", inplace=True)

except Exception as e:
    die(f"An error occured when trying to open and parse the input file: {str(e)}")

# Everything done, save it

iprint(f"Saving the output file: {output_path}")

try:
    # We'll try to export it as csv and write to given path
    input.to_csv(output_path, index=None, header=True)
except IOError:
    die(
        "An I/O error occured when trying to save the output file. Maybe it is already used by another process?"
    )
except BaseException:
    die("An error occured when trying to save the output file.")

iprint("Done.")
