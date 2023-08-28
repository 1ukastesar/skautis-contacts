# -*- coding: utf-8 -*-
# Ah, yeah, the encoding. Just to be sure.

# Information about the script, declared also as variables for later usage...
APP_NAME =  "skautIS to Google Contacts CSV converter"
APP_VERSION = 2.2
AUTHOR = "Lukáš Tesař <lukastesar@skaut.cz>"

# Importing basic Python modules
# These should be always included in default installation
import subprocess
import sys
import os
import argparse

import pandas as pd
import openpyxl as opxl

# CONSTANTS for later use

SKIP_ROWS = 6
USE_COLS = [0, 1, 2, 4, 7, 8, 9, 10, 11]

COL_RENAME_RULES = {
                    "Jméno":            "Given Name",
                    "Příjmení":         "Family Name",
                    "Přezdívka":        "Nickname",
                    "Jednotka":         "Group Membership",
                    "Kategorie":        "Category",
                    "Otec: mail":       "E-mail 1 - Value",
                    "Matka: mail":      "E-mail 2 - Value",
                    "Otec: telefon":    "Phone 1 - Value",
                    "Matka: telefon":   "Phone 2 - Value"
                    }

ADD_COLS =  [
            [0,  "Name",                ""],
            [2,  "Additional Name",     ""],
            [4,  "Yomi Name",           ""],
            [5,  "Given Name Yomi",     ""],
            [6,  "Additional Name Yomi",""],
            [7,  "Family Name Yomi",    ""],
            [8,  "Name Prefix",         ""],
            [9,  "Name Suffix",         ""],
            [10, "Initials",            ""],
            [12, "Short Name",          ""],
            [13, "Maiden Name",         ""],
            [14, "Birthday",            ""],
            [15, "Gender",              ""],
            [16, "Location",            ""],
            [17, "Billing Information", ""],
            [18, "Mileage",             ""],
            [19, "Occupation",          ""],
            [20, "Hobby",               ""],
            [21, "Sensitivity",         ""],
            [22, "Priority",            ""],
            [23, "Subject",             ""],
            [24, "Notes",               ""],
            [25, "Language",            ""],
            [26, "Photo",               ""],
            [28, "E-mail 1 - Type",     "Otec"],
            [30, "E-mail 2 - Type",     "* Matka"],
            [32, "Phone 1 - Type",      "Otec"],
            [34, "Phone 2 - Type",      "* Matka"]
            ]

GRPMEM_SEPARATOR =  " ::: "
GRPMEM_SUFFIX =     "* myContacts"

# FUNCTIONS for later use

# Error handler
def die(error):
    if not quiet: print("\nERROR: " + error)
    sys.exit(1)

# First things first, handle commandline arguments (in case of --help or etc.)
# This process is semi-automatic (for example, displaying the help message is handled fully within the 'argparse' module itself)

# Create the argument parser instance
parser = argparse.ArgumentParser()
# INPUT and OUTPUT file arguments
parser.add_argument("input", help = "input file path, desired data format is Excel spreadsheet (.xlsx)")
parser.add_argument("output", help = "output file path, data will be exported in Google Contacts CSV (.csv) format")
# Other (optional) arguments (for verbosity settings etc.)
parser.add_argument("-q", "--quiet", help = "be quiet; do NOT print ANY information about the whole process, including any errors (not recommended, default FALSE)", 
                    action = "store_true")
# Last but not least, we don't forget to parse the arguments and save them to a variable
args = parser.parse_args()

# Some of the args we'll be using more frequently, so it's a good idea to shorten their variable names (or determine ABSPATH)
quiet = args.quiet
input_path = args.input
output_path = args.output

if not quiet:
    print(APP_NAME + ", v" + str(APP_VERSION))
    print("Made with <3 by " + AUTHOR)
    print()

# Now the actual process itself
if not quiet: print("\nLoading the input file: " + input_path)

# Check if input_path exists
if not os.path.exists(input_path):
    if not os.path.exists(os.path.abspath(input_path)):
        die("INPUT path doesn't exist.")
    else:
        input_path = os.path.abspath(input_path)

# The whole parsing thing is wrapped in try-catch block, if the user tried to give us broken, not valid or incomplete XLSX
try:
    try:
        # First, we (try to) load the input file and parse it into DataFrame (pd)
        input = pd.read_excel(input_path, 
                            skiprows = range(0,SKIP_ROWS), 
                            usecols = USE_COLS,
                            dtype={"Matka: telefon": str, "Otec: telefon": str})
    # If we're not successful, we give up and print the error:
    # - when file not found
    except FileNotFoundError:
        die("Input file not found. \n")
    # - in case of an I/O error - maybe the file is open by another program?
    except IOError:
        die("An I/O error occured when trying to open the input file. Maybe it is already used by another process?\n")
    # - or something other happened - broken format or whatever
    except:
        raise

    if not quiet: print("Processing...")

    # Then we'll make it look like a Google CSV:
    # - some columns we'll rename
    input.rename(columns = COL_RENAME_RULES, inplace = True)

    # - some just need to be added (with no values, in most cases)
    for col in ADD_COLS:
        input.insert(col[0],col[1],col[2])

    # - this one combines values from two other columns instead (Given + Family name = Full name)
    input["Name"] = input["Given Name"] + " " + input["Family Name"]

    # - and some need bigger changes (combining, renaming and adding values)
    input["Group Membership"] = input["Group Membership"].astype(str) \
                            + GRPMEM_SEPARATOR \
                            + input["Category"].astype(str) \
                            + GRPMEM_SEPARATOR \
                            + GRPMEM_SUFFIX

    if not quiet: print("A few more changes to be done...")

    # - add +420 in the beginning of telephone numbers to be recognized correctly
    input["Phone 1 - Value"] = "+420" + input["Phone 1 - Value"].astype(str)
    input["Phone 2 - Value"] = "+420" + input["Phone 2 - Value"].astype(str)

    # - remove "+420nan", whichever cells is it in (this is a result of an empty phone number cell on the input)
    input.replace("+420nan", "", inplace = True)

    # - as a last thing, we drop the columns we no longer need
    input.drop(columns = "Category", inplace = True)

except:
    die("An error occured when trying to open and parse the input file.\n")

# If everything happened correctly (we'll hope so), we can move on to the final step:
# Saving the whole thing

if not quiet: print("Saving the output file: " + output_path)

try:
    # We'll try to export it as csv and write to given path
    input.to_csv(output_path, index = None, header = True)
# If we're not successful, we give up and print the error:
# - in case of an I/O error - maybe the file is open by another program?
except IOError:
    die("An I/O error occured when trying to save the output file. Maybe it is already used by another process?\n")
# - or something other happened
except:
    die("An error occured when trying to save the output file.\n")

# Aaaand done.
if not quiet: print("\nDone.")
