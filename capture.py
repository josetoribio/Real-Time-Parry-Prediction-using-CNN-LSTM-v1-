# scripts/auto_capture_parry.py
import ctypes
import time
from mss import mss
from PIL import Image
import os

# --- Constants for key simulation ---
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

def press_key(scan_code):
    ctypes.windll.user32.keybd_event(0, scan_code, KEYEVENTF_SCANCODE, 0)

def release_key(scan_code):
    ctypes.windll.user32.keybd_event(0, scan_code, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0)

# --- Scancodes ---
SC_DOWN = 46      # C key → down
SC_FORWARD = 47   # V key → forward
SC_PUNCH = 49     # N key → punch
SC_PARRY = 44    # X key → parry

# --- Screen capture region (adjust to your Fightcade window) ---
monitor = {"top": 150, "left": 100, "width": 1600, "height": cvn00}

# --- Output directories ---
os.makedirs("data/parry", exist_ok=True)
os.makedirs("data/no_parry", exist_ok=True)

sct = mss()
frame_count = 0

print("Focus Fightcade window in 5 seconds...")
time.sleep(5)

try:
    while True:
        # --- Hadouken motion ---
        press_key(SC_DOWN)
        time.sleep(0.05)

        press_key(SC_FORWARD)  # Down-Forward
        time.sleep(0.05)

        release_key(SC_DOWN)
        time.sleep(0.05)

        release_key(SC_FORWARD)
        time.sleep(0.05)

        # --- Punch ---
        press_key(SC_PUNCH)
        time.sleep(0.15)
        release_key(SC_PUNCH)

        # --- Capture frame before parry (Hadouken only) ---
        frame = sct.grab(monitor)
        img = Image.frombytes("RGB", frame.size, frame.rgb)
        img.save(f"data/no_parry/frame_{frame_count:05d}.png")
        frame_count += 1

        time.sleep(0.6)

        # --- Parry ---
        press_key(SC_PARRY)
        time.sleep(0.02)
        release_key(SC_PARRY)

        # --- Capture frame after parry ---
        frame = sct.grab(monitor)
        img = Image.frombytes("RGB", frame.size, frame.rgb)
        img.save(f"data/parry/frame_{frame_count:05d}.png")
        frame_count += 1

        # --- Delay before next combo ---
        time.sleep(1)

except KeyboardInterrupt:
    print(f"\nAutomation stopped. Total frames captured: {frame_count}")