# scripts/dataset_loader.py
import os
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms

class ParryDataset(Dataset):
    def __init__(self, root_dir, sequence_length=2, transform=None):
        self.sequence_length = sequence_length
        self.transform = transform or transforms.ToTensor()
        self.data = []
        self.labels = []

        for label, cls in enumerate(['no_parry', 'parry']):
            cls_dir = os.path.join(root_dir, cls)
            if not os.path.exists(cls_dir):
                continue
            frames = sorted(os.listdir(cls_dir))
            print(f"Found {len(frames)} frames for class {cls}")
            for i in range(len(frames) - sequence_length + 1):
                seq = [os.path.join(cls_dir, frames[j]) for j in range(i, i + sequence_length)]
                self.data.append(seq)
                self.labels.append(label)

        print(f"Total sequences: {len(self.data)}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        paths = self.data[idx]
        imgs = [self.transform(Image.open(p).convert('RGB')) for p in paths]
        return torch.stack(imgs), self.labels[idx]