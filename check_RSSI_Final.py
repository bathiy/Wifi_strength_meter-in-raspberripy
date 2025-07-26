import subprocess
import re
import time
import curses
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# GPIO Pin Setup
BTN_UP = 31     # Move up
BTN_DOWN = 33   # Move down
BTN_SELECT = 29 # Select (Enter)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize I2C for OLED (SSD1306 - 128x64)
serial = i2c(port=1, address=0x3C)
oled = ssd1306(serial, width=128, height=64)

# Load font
font = ImageFont.load_default()

def display_text(lines, highlight_index=None):
    """Displays text on the OLED, highlighting the selected index if provided."""
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)

    y_offset = 0
    for i, line in enumerate(lines):
        if highlight_index is not None and i == highlight_index:
            draw.rectangle((0, y_offset, 127, y_offset + 10), outline=255, fill=255)
            draw.text((5, y_offset), line, font=font, fill=0)  # Inverted text
        else:
            draw.text((5, y_offset), line, font=font, fill=255)
        y_offset += 10

    oled.display(image)

def scan_wifi():
    """Scans for available Wi-Fi networks and returns their SSIDs."""
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
        output = result.stdout
        ssid_pattern = re.compile(r'ESSID:"(.*?)"')
        ssids = ssid_pattern.findall(output)
        return ssids if ssids else []
    except Exception as e:
        display_text(["Scan Error!", str(e)[:20]])  # Show first 20 chars of error
        return []

def get_rssi(selected_ssid):
    """Gets the RSSI (signal strength) for a selected SSID."""
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
        output = result.stdout
        network_blocks = output.split('Cell')
        for block in network_blocks:
            if selected_ssid in block:
                signal_pattern = re.search(r'Signal level=(-?\d+) dBm', block)
                if signal_pattern:
                    return int(signal_pattern.group(1))
        return None
    except Exception as e:
        display_text(["RSSI Error!", str(e)[:20]])  # Show first 20 chars of error
        return None

def wait_for_button(button_pin):
    """Waits for a button press and releases it before returning."""
    while GPIO.input(button_pin) == GPIO.LOW:
        time.sleep(0.05)  # Small delay to avoid CPU overload
    while GPIO.input(button_pin) == GPIO.HIGH:
        time.sleep(0.05)  # Wait until button is released

def select_wifi(wifi_networks):
    """Allows user to select a Wi-Fi network using push buttons with scrolling and a Back option."""
    wifi_networks.append("--Back--")  # Add Back option at the end
    current_index = 0  # Start at first SSID
    display_limit = 5  # Number of SSIDs visible on the screen at once
    top_index = 0  # Track the top of the visible list

    while True:
        visible_networks = wifi_networks[top_index:top_index + display_limit]
        display_text(["Select Wi-Fi:"] + visible_networks, highlight_index=(current_index - top_index) + 1)

        if GPIO.input(BTN_UP) == GPIO.HIGH and current_index > 0:
            current_index -= 1
            if current_index < top_index:
                top_index -= 1  # Scroll up
            wait_for_button(BTN_UP)

        if GPIO.input(BTN_DOWN) == GPIO.HIGH and current_index < len(wifi_networks) - 1:
            current_index += 1
            if current_index >= top_index + display_limit:
                top_index += 1  # Scroll down
            wait_for_button(BTN_DOWN)

        if GPIO.input(BTN_SELECT) == GPIO.HIGH:
            wait_for_button(BTN_SELECT)
            if wifi_networks[current_index] == "--Back--":
                return None  # Return to the main menu
            return wifi_networks[current_index]

def main_menu():
    """Displays a main menu where the user can choose to scan Wi-Fi or exit using push buttons."""
    options = ["Scan Wi-Fi", "Turn Off"]
    current_index = 0

    while True:
        display_text(["Welcome!", " "] + options, highlight_index=current_index + 2)

        if GPIO.input(BTN_UP) == GPIO.HIGH and current_index > 0:
            current_index -= 1
            wait_for_button(BTN_UP)

        if GPIO.input(BTN_DOWN) == GPIO.HIGH and current_index < len(options) - 1:
            current_index += 1
            wait_for_button(BTN_DOWN)

        if GPIO.input(BTN_SELECT) == GPIO.HIGH:
            wait_for_button(BTN_SELECT)
            return options[current_index]
            
def get_rssi_status_bar(rssi):
    """Returns a string of '*' symbols proportional to the RSSI value."""
    max_rssi = -10  # Maximum RSSI value (strongest signal)
    min_rssi = -80  # Minimum RSSI value (weakest signal)
    bar_length = 20  # Length of the '*' bar for OLED display (adjust to fit the display)

    # Normalize the RSSI to a value between 0 and 1
    normalized_rssi = (rssi - min_rssi) / (max_rssi - min_rssi)
    normalized_rssi = max(0, min(normalized_rssi, 1))  # Ensure it stays between 0 and 1
    
    # Calculate the number of '*' based on the normalized value
    stars = int(normalized_rssi * bar_length)
    
    # Create the status bar with '*' symbols
    status_bar = '*' * stars + ' ' * (bar_length - stars)
    
    return status_bar
    
def main():
    try:
        while True:
            choice = main_menu()

            if choice == "Turn Off":
                display_text(["Goodbye!"])
                time.sleep(2)
                break
            elif choice == "Scan Wi-Fi":
                wifi_networks = scan_wifi()

                if wifi_networks:
                    selected_ssid = select_wifi(wifi_networks)
                    if selected_ssid is None:
                        continue  # Return to main menu if "--Back--" is selected
                    display_text(["Monitoring:", f"{selected_ssid}"])
                    time.sleep(2)

                    for i in range(20): 
                        rssi = get_rssi(selected_ssid)
                        if rssi is not None:
                            strength = get_rssi_status_bar(rssi)
                            display_text(["SSID:", f"{selected_ssid}", " ", "RSSI:", f"{rssi} dBm", strength])
                        else:
                            display_text([f"{selected_ssid} Not Found"])
                        time.sleep(0.1)
                else:
                    display_text(["No Wi-Fi found!"])
                    time.sleep(2)

    finally:
        GPIO.cleanup()  # Cleanup GPIO when exiting

if __name__ == "__main__":
    main()
