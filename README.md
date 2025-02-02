# Převod kontaktů ze skautISu do Google Contacts

## Instalace

### Požadavky

- ```python3.12```

Nainstaluj pomocí správce balíčků nebo stáhni z https://www.python.org/downloads/

> [!TIP]
> Nejnovější verze skriptu byla testována na Python 3.12.3, ale obecně by měla fungovat s Python 3.8 a novějším.

## Závislosti

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
pip -r requirements.txt
```

## Použití

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
8. Otevři terminál. Přejdi do složky s tímto skriptem a složkou `.venv`.
9. Pokud nejsi již ve virtuálním prostředí, aktivuj ho:
```bash
. .venv/bin/activate
```
10.  Spusť:
```bash
./convert.py <cesta_ke_staženému_xlsx_exportu>.xlsx <kam_uložit_výstup>.csv
```

> [!IMPORTANT]
> Zde doporučuji vizuální kontrolu vytvořeného CSV, zda se zdá být v pořádku. Mělo by odpovídat [ukázkové šabloně](https://docs.google.com/spreadsheets/u/1/d/1aKXGNF0YMEPRjIuyrl0nUeG4vOiGl6jEj5ikYRc5dl4/copy).

11.  Importuj tento `.csv` soubor do Google Contacts. Nezapomeň poté smazat staré kontakty, abys předešel duplicitám.

> [!NOTE]
> Tento proces se obvykle provádí jednou ročně, aby byly kontaktní údaje aktuální.
