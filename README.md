# SkautIS contacts to Google Contacts converter


## Setup

### Prerequisites

- ```python3.11```

Install with your package manager or download from https://www.python.org/downloads/

> [!NOTE]
> The latest version of this app was tested on Python 3.11, but it should generally work with Python 3.8 and later.

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
5. Go back to `Exporty / seznamy`, select your newly created template
6. Remove default data to export, add a new one using `Přidat jednotku` and when it's done, tick `Včetně podřízených`.
> [!NOTE]
> The removal and re-addition needs to be done to allow ticking that box.
7. Click `Export do XLSX`. The export will download.
8. Open terminal. Navigate to folder with this converter and `.venv` folder.
9.  If not in virtual environment already, activate it:
```bash
. .venv/bin/activate
```
10.  Run:
```bash
./convert.py <path_to_downloaded_xlsx_export>.xlsx <where_to_save_the_output>.csv
```

11.  Import that `.csv` file into Google Contacts. Remember to delete old contacts first to avoid duplicates.

> [!NOTE]
> This process is usually done once a year to keep the contact details updated.
