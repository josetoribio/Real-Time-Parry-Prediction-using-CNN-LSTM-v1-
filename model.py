# scripts/model.py
import torch
import torch.nn as nn

class CNNLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.lstm = nn.LSTM(32*32*32, 64, batch_first=True)
        self.fc = nn.Linear(64, 2)  # 2 classes: no_parry, parry

    def forward(self, x):
        batch_size, seq_len, C, H, W = x.size()
        c_in = x.view(batch_size*seq_len, C, H, W)
        c_out = self.cnn(c_in)
        c_out = c_out.view(batch_size, seq_len, -1)
        lstm_out, _ = self.lstm(c_out)
        out = self.fc(lstm_out[:,-1,:])
        return out