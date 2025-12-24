# Převod kontaktů ze skautISu do Google Contacts

## Webová aplikace (doporučeno)

### Spuštění přes Docker (doporučeno)

#### Požadavky
```bash
docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
git
```

#### Spuštění

```bash
docker compose up -d
```

Aplikace bude dostupná na portu 5000.

#### Zastavení

```bash
docker compose down
```

#### Aktualizace

```bash
docker compose down
git pull
docker compose up -d --build
```

### Spuštění bez Dockeru

#### Požadavky

- ```python3.12```

Nainstaluj pomocí správce balíčků nebo stáhni z https://www.python.org/downloads/

#### Instalace

1. Vytvoř virtuální prostředí:
```bash
python -m venv .venv
```
2. Aktivuj ho:
```bash
. .venv/bin/activate
```
3. Nainstaluj závislosti:
```bash
pip install -r requirements.txt
```

#### Spuštění

```bash
python app.py
```

Aplikace bude dostupná na http://localhost:5000

---

## CLI režim

Skript lze stále používat z příkazové řádky:

```bash
./convert.py <cesta_ke_staženému_xlsx_exportu>.xlsx <kam_uložit_výstup>.csv
```

---

## Příprava exportu ze skautISu

> [!CAUTION]
> Doporučuji nejdříve udělat zálohu a staré kontakty smazat až po úspěšném importu nových, aby se předešlo jakékoli ztrátě dat!

1. Přihlas se do skautISu.
2. Vyber správnou roli. Pro export musí být `Oddíl: vedoucí/admin`
3. Přejdi na `Exporty > Osoby`
4. V sekci `Správa a nastavení exportů` vytvoř novou šablonu a nastav ji podle přiloženého [screenshotu](skautis_export_template_settings.png).
5. Vrať se na `Exporty / seznamy`, vyber nově vytvořenou šablonu.
6. Odstraň výchozí jednotku k exportu, přidej novou pomocí formuláře `Přidat jednotku` a přitom zaškrtni `Včetně podřízených`.
> [!NOTE]
> Odstranění a opětovné přidání je nutné k tomu, aby bylo možné zahrnout podřízené jednotky.
7. Klikni na `Export do XLSX`. Export se stáhne.
8. Nahraj stažený soubor do webové aplikace nebo použij CLI.

## Import do Google Contacts

> [!IMPORTANT]
> Doporučuji vizuální kontrolu vytvořeného CSV, zda se zdá být v pořádku. Mělo by odpovídat [ukázkové šabloně](https://docs.google.com/spreadsheets/u/1/d/1aKXGNF0YMEPRjIuyrl0nUeG4vOiGl6jEj5ikYRc5dl4/copy).

1. Importuj stažený `.csv` soubor do Google Contacts.
2. Nezapomeň poté smazat staré kontakty, abys předešel duplicitám.

> [!NOTE]
> Tento proces se obvykle provádí jednou ročně, aby byly kontaktní údaje aktuální.
