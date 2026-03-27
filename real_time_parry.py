# scripts/real_time_parry.py
import time
import ctypes
from PIL import ImageGrab
from PIL import Image
import torch
from torchvision import transforms
import os
from model import CNNLSTM

# --- Monitor capture area ---
monitor = {
    "top": 100,
    "left": 100,
    "width": 1600,  # change to your game resolution width
    "height": 600   # change to your game resolution height
}

# --- Key press setup ---
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

SC_DOWN = 46       # C key → down
SC_FORWARD = 47    # V key → forward
SC_PUNCH = 48      # B key → punch
SC_PARRY = 44      # X key → parry

def press_key(scan_code):
    ctypes.windll.user32.keybd_event(0, scan_code, KEYEVENTF_SCANCODE, 0)

def release_key(scan_code):
    ctypes.windll.user32.keybd_event(0, scan_code, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0)

def tap_key(scan_code, hold=0.1):
    press_key(scan_code)
    time.sleep(hold)
    release_key(scan_code)

# --- Model setup ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CNNLSTM().to(device)

model_path = os.path.join(os.path.dirname(__file__), "cnn_lstm_parry.pth")
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# --- Sequence & transform ---
sequence_length = 5
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))
])

seq_buffer = []

# --- Rolling prediction tracking ---
rolling_preds = []
rolling_confs = []
rolling_window = 7  # number of frames to track rolling predictions

# --- Parry cooldown ---
confidence_threshold = 0.75
cooldown = 0.25  # seconds between parries
last_parry_time = 0

print("Starting real-time parry detection. Focus your game window...")
time.sleep(3)

try:
    while True:
        # --- Grab frame ---
        img = ImageGrab.grab(bbox=(monitor["left"], monitor["top"],
                                    monitor["left"] + monitor["width"],
                                    monitor["top"] + monitor["height"]))
        img = img.convert("RGB")
        img_tensor = transform(img).unsqueeze(0)  # (1, C, H, W)
        seq_buffer.append(img_tensor)

        if len(seq_buffer) < sequence_length:
            continue  # wait until buffer fills

        # --- Prepare sequence for model ---
        input_seq = torch.stack(seq_buffer[-sequence_length:], dim=0)  # (seq_len, 1, C, H, W)
        input_seq = input_seq.permute(1, 0, 2, 3, 4).to(device)         # (1, seq_len, C, H, W)

        # --- Predict ---
        with torch.no_grad():
            output = model(input_seq)
            probs = torch.softmax(output, dim=1)
            conf, pred = torch.max(probs, dim=1)

       # --- Rolling prediction + confidence tracking ---
        rolling_preds.append(pred.item())
        rolling_confs.append(conf.item())

        if len(rolling_preds) > rolling_window:
            rolling_preds.pop(0)
            rolling_confs.pop(0)

        parry_votes = rolling_preds.count(1)
        no_parry_votes = rolling_preds.count(0)
        avg_conf = sum(rolling_confs) / len(rolling_confs)

        print(
        f"[Window {rolling_window}] "
        f"Votes -> Parry: {parry_votes}, No: {no_parry_votes} | "
        f"AvgConf: {avg_conf:.2f} | CurrConf: {conf.item():.2f}"
            )


          # --- Execute parry if conditions met ---
            # --- Decision logic (NEW) ---
        recent_preds = rolling_preds[-rolling_window:]
        parry_votes = recent_preds.count(1)

        current_time = time.time()

        if (
                len(recent_preds) == rolling_window and
                parry_votes >= 5 and  # majority vote (5 out of 7)
                conf.item() > confidence_threshold and
                (current_time - last_parry_time) > cooldown
         ):
                print(f"Parry! votes={parry_votes}/{rolling_window} conf={conf.item():.2f}")
                
                #time.sleep(0.02)  # slight delay to fix early timing
                tap_key(SC_PARRY, hold=0.03)  # shorter tap = less movement bugs
                
                last_parry_time = current_time
        else:
                print(f"No parry | votes={parry_votes}/{rolling_window} conf={conf.item():.2f}")
                    

except KeyboardInterrupt:
    print("Real-time parry detection stopped.")