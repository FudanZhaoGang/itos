import torch
from torch.utils.data import Dataset
from transformers import BertTokenizer


class IntentionDataset(Dataset):
    def __init__(self, config, index):
        with open(config.data_path, 'r', encoding='utf-8') as f:
            total = f.readlines()
            self.data = [total[i] for i in index]
            self.config = config

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        line = self.data[index].split()
        intention = int(line[0])
        sentence = line[1]
        return sentence, intention
