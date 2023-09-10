# SkautIS contacts to Google Contacts converter


## Setup

### Prerequisites

- ```python3.11```

Install with your package manager or download from https://www.python.org/downloads/

> **Note:** The latest version of this app was tested on Python 3.11, but it should generally work with Python 3.8 and later.

1. Create virtual environment:
```bash
python -m venv .venv
```
2. Activate it:
```bash
. .venv/bin/activate
```
3. Install dependencies:
```bash
pip -r requirements.txt
```

## Usage

1. Log in to skautIS.
2. Select the right role. For the export to work, it must be `Oddíl: vedoucí/admin`
3. Go to `Exporty > Osoby`
4. Under `Správa a nastavení exportů` create new template and set it up like it is shown in the attached [screenshot](skautis_export_template_settings.png).
5. Go back to `Exporty / seznamy`, select your newly created template and click `Export do XLSX`. The export will download.
6. Open terminal. Navigate to folder with this converter and `.venv` folder.
7. If not in virtual environment already, activate it:
```bash
. .venv/bin/activate
```
8. Run:
```bash
./convert.py <path_to_downloaded_xlsx_export>.xlsx <where_to_save_the_output>.csv
```

9. Import that `.csv` file into Google Contacts. Remember to delete old contacts first to avoid duplicates.

> This process is usually done once a year to keep the contact details updated.
