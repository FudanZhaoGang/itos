import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer


class Bert(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.bert = BertModel.from_pretrained(config.pretrained_path)
        self.tokenizer = BertTokenizer.from_pretrained(config.pretrained_path)
        self.linear = nn.Linear(768, config.num_class)
        self.device = config.device

    def forward(self, sentences):
        input = torch.tensor(self.tokenizer(sentences, padding=True)['input_ids']).to(self.device)
        output = self.bert(input)[0][:, 0, :]
        output = self.linear(output)
        return output
