#!/bin/bash
set -e

echo "[*] Updating system packages..."
sudo apt update

echo "[*] Installing system dependencies..."
sudo apt install -y libopenal1 libasound2t64 libpulse0 fonts-dejavu

echo "[*] Installing Python dependencies..."
pip install --break-system-packages -r requirements.txt

echo "[✔] Setup complete!"
