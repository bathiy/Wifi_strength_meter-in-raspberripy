# 📶 Wi-Fi Signal Strength Meter using Raspberry Pi

This is a **personal project** to build a standalone **Wi-Fi Signal Strength Meter** using a **Raspberry Pi**, **SSD1306 OLED display**, and **hardware push buttons**. It allows users to scan available Wi-Fi networks, select one, and monitor its real-time signal strength (RSSI) visually on the display.

## 🛠️ Features

- Scan for available Wi-Fi networks
- Select a network using hardware buttons
- Real-time RSSI (Received Signal Strength Indicator) display
- Visual signal strength bar using `*` characters
- Simple OLED menu interface
- Back and exit functionality
- GPIO button navigation

## 📷 System Overview

This project is built using:

- **Python**
- **RPi.GPIO** – For reading hardware button inputs
- **luma.oled** – To drive the SSD1306 OLED screen
- **Pillow** – For rendering text and graphics
- **subprocess** – To fetch Wi-Fi scan and RSSI data using Linux commands

## 🖥️ Hardware Requirements

| Component             | Description                          |
|----------------------|--------------------------------------|
| Raspberry Pi         | With built-in Wi-Fi or dongle        |
| SSD1306 OLED Display | 128x64 resolution (I2C interface)    |
| Push Buttons         | 3 buttons (Up, Down, Select)         |
| Breadboard & Wires   | Or custom PCB                        |

### 🔌 Pin Configuration

#### OLED I2C Pins:

| OLED Pin | Pi Pin |
|----------|--------|
| VCC      | 3.3V   |
| GND      | GND    |
| SDA      | GPIO 2 (Pin 3)  |
| SCL      | GPIO 3 (Pin 5)  |

#### Button GPIO Pins:

| Function | GPIO | Pin |
|----------|------|-----|
| Up       | 6    | 31  |
| Down     | 13   | 33  |
| Select   | 5    | 29  |

> Buttons are internally pulled down using `GPIO.PUD_DOWN` and must be connected between the GPIO pin and 3.3V.

---

## 📦 Software Requirements

Install the following packages on your Raspberry Pi:

```bash
sudo apt update
sudo apt install python3-pip python3-dev i2c-tools -y
pip3 install RPi.GPIO luma.oled pillow
```

## 🔧 Enable I2C on Raspberry Pi

To use the OLED display, make sure I2C is enabled on your Raspberry Pi:

```bash
sudo raspi-config
# Navigate to: Interfacing Options -> I2C -> Enable
```
## 🚀 How to Run

1. Save the full project code into a file named: `wifi_signal_meter.py`

2. Run the script using:

```bash
sudo python3 wifi_signal_meter.py
```
## 📋 Menu Flow

- `Scan Wi-Fi`: Lists all available networks, scrollable using the Up/Down buttons.
- `Select Network`: Monitors the selected Wi-Fi network.
- `RSSI Display`: Shows real-time RSSI in dBm and a visual `*` bar.
- `--Back--`: Returns to the main menu.
- `Turn Off`: Exits the program safely.

## 🔚 Clean Exit

The program ensures a proper GPIO cleanup (`GPIO.cleanup()`), preventing issues on shutdown or re-run.

---

## 📘 Project Goals & Learnings

- Interface buttons and an OLED screen with a Raspberry Pi using Python
- Monitor and visualize real-time Wi-Fi signal strength
- Build a simple embedded user interface using minimal components
- Practice button input handling with debounce logic

---

## 👨‍💻 Author

**Bathiya Dissanayake**  
Undergraduate – Electronics and Telecommunication Engineering  
University of Moratuwa
