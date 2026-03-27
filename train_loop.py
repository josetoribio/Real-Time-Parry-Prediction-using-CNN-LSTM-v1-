# scripts/train.py
import os
import sys
import torch
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from dataset_loader import ParryDataset
from model import CNNLSTM

# --- Settings ---
batch_size = 8
seq_len = 2
epochs = 5
lr = 1e-3
data_dir = os.path.join(os.path.dirname(__file__), '../data')
transform = transforms.Compose([transforms.Resize((128,128)), transforms.ToTensor()])

# --- Dataset ---
dataset = ParryDataset(data_dir, sequence_length=seq_len, transform=transform)
if len(dataset) == 0:
    print("No data found! Check your data/no_parry and data/parry folders.")
    exit()

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_ds, val_ds = random_split(dataset, [train_size, val_size])
train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

# --- Model, loss, optimizer ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CNNLSTM().to(device)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

# --- Training loop ---
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for X, y in train_loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        out = model(X)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.4f}")

    # --- Validation ---
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for X, y in val_loader:
            X, y = X.to(device), y.to(device)
            out = model(X)
            preds = out.argmax(dim=1)
            correct += (preds==y).sum().item()
            total += y.size(0)
    print(f"Validation Accuracy: {correct/total:.4f}")
#save model after training
torch.save(model.state_dict(), os.path.join(os.path.dirname(__file__), 'cnn_lstm_parry.pth'))
print("Model saved as cnn_lstm_parry.pth")