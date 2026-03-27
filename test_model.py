import os
import torch
from dataset_loader import ParryDataset
from model import CNNLSTM
from torchvision import transforms
from torch.utils.data import DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# --- Load trained model ---
model = CNNLSTM().to(device)
model.load_state_dict(torch.load(os.path.join(os.path.dirname(__file__), 'cnn_lstm_parry.pth'), map_location=device))
model.eval()

# --- Load dataset for testing ---
transform = transforms.Compose([transforms.Resize((128,128)), transforms.ToTensor()])
dataset = ParryDataset(os.path.join(os.path.dirname(__file__), '../data'), sequence_length=2, transform=transform)
loader = DataLoader(dataset, batch_size=1, shuffle=False)

# --- Run predictions ---
correct = 0
total = 0
for X, y in loader:
    X, y = X.to(device), y.to(device)
    with torch.no_grad():
        out = model(X)
        pred = out.argmax(dim=1).item()
    print(f"True: {y.item()}, Predicted: {pred}")
    correct += int(pred == y.item())
    total += 1

print(f"\nTest Accuracy: {correct/total:.4f}")