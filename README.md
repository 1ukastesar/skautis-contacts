# Převod kontaktů ze skautISu do Google Contacts

## Instalace

### Požadavky

- ```python3.11```

Nainstaluj pomocí správce balíčků nebo stáhni z https://www.python.org/downloads/

> [!NOTE]
> Nejnovější verze této aplikace byla testována na Python 3.11, ale obecně by měla fungovat s Python 3.8 a novějšími.

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

11.  Importuj tento `.csv` soubor do Google Contacts. Nezapomeň nejprve smazat staré kontakty, abys předešel duplicitám.

> [!NOTE]
> Tento proces se obvykle provádí jednou ročně, aby byly kontaktní údaje aktuální.
