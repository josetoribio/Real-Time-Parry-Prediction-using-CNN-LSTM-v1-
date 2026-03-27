import ctypes
import time

# --- Constants ---
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002


# --- Scancodes ---
SC_DOWN = 46      # C key → down
SC_FORWARD = 47   # V key → forward
SC_PUNCH = 49     # N key → punch
SC_PARRY = 44    # X key → parry
print("Focus Fightcade window in 5 seconds...")
time.sleep(5)

try:
    while True:
        # Step 1: Press Down
        press_key(SC_DOWN)
        time.sleep(0.05)

        # Step 2: Press Forward while still holding Down (Down-Forward)
        press_key(SC_FORWARD)
        time.sleep(0.05)

        # Step 3: Release Down (Forward still held)
        release_key(SC_DOWN)
        time.sleep(0.05)

        # Step 4: Release Forward (optional delay)
        release_key(SC_FORWARD)
        time.sleep(0.05)

        # Step 5: Punch
        press_key(SC_PUNCH)
        time.sleep(0.15)  # hold punch a bit longer
        release_key(SC_PUNCH)

        # Step 6: Small delay before next Hadouken
        time.sleep(.6)

        # Step 7: Parry
     #   press_key(SC_PARRY)
     #   time.sleep(0.02)  # hold punch a bit longer
      #  release_key(SC_PARRY)
                    
        # Step 8: Delay before next projectle
        time.sleep(4)

except KeyboardInterrupt:
    print("\nHadouken automation stopped by user.")