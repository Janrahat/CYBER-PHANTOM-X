# ☠️ CYBER PHANTOM X — 3.0 MEGA EDITION

Colorful defensive Python toolkit for Termux and Kali Linux.

## Features
- Phone-number numbering-plan metadata: region, country-formatting, possible/valid status, type, time zones, carrier if available.
- Public IP information (approximate geolocation).
- DNS A/AAAA/MX/NS/TXT records.
- Website status and common security headers.
- Limited user-specified TCP port checks for authorized systems.
- Local hostname/IP info.
- Secure random password generator.
- SHA-256 file integrity checker.
- Extra tools, reports center, settings/help, and an optional secret menu (choice `99`).
- JSON reports in `reports/`.

**Limitations:** A phone number alone cannot reveal live GPS, a person's identity, or home address. IP geolocation is approximate. Carrier data may be unavailable or outdated. Only scan systems you own or have explicit permission to test.

## Termux
```bash
pkg update -y
pkg install -y python git
# Extract the ZIP, then enter its folder:
bash install-termux.sh
python main.py
```

## Kali Linux
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
# Extract the ZIP, then enter its folder:
bash install-kali.sh
source .venv/bin/activate
python main.py
```

## Secret menu
Choose `99` in the main menu. Default demo code: `CPX-2025`. Change it using `CPX_SECRET_CODE='your-own-code' python main.py`. This is only a menu gate, not strong security. Secret menu includes defensive checks only.
