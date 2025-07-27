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

## 🔧 Enable I2C on Raspberry Pi

To use the OLED display, make sure I2C is enabled on your Raspberry Pi:

```bash
sudo raspi-config
# Navigate to: Interfacing Options -> I2C -> Enable
