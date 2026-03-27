# scripts/train.py
import os
import sys
sys.path.append(os.path.dirname(__file__))  # ensure scripts/ is in path

import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from dataset_loader import ParryDataset
from model import CNNLSTM

# --- Settings ---
batch_size = 2
seq_len = 2
data_dir = os.path.join(os.path.dirname(__file__), '../data')
transform = transforms.Compose([transforms.Resize((128,128)), transforms.ToTensor()])

# --- Dataset ---
dataset = ParryDataset(data_dir, sequence_length=seq_len, transform=transform)
if len(dataset) == 0:
    print("No data found! Check your data/no_parry and data/parry folders.")
    exit()

loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# --- Model ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CNNLSTM().to(device)
model.eval()

# --- Test forward ---
for X, y in loader:
    X = X.to(device)
    out = model(X)
    print(f"Input shape: {X.shape}, Output shape: {out.shape}, Labels: {y}")
    break