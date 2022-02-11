

# import random
# import torch
# from transformers import GPT2LMHeadModel, BertTokenizer
# from tool import tokenize, sample_sequence
#
#
# seed = 42
# model_checkpoint = 'thu-coai/CDial-GPT_LCCC-large'
# device = "cuda" if torch.cuda.is_available() else "cpu"
# temperature = 0.7
# top_p = 0.9
# top_k = 0
# no_sample = True
# min_length = 1
# max_length = 30
#
#
# random.seed(seed)
# torch.random.manual_seed(seed)
# torch.cuda.manual_seed(seed)
#
# model = GPT2LMHeadModel.from_pretrained(model_checkpoint)
# tokenizer = BertTokenizer.from_pretrained(model_checkpoint, do_lower_case=True)
#
# model.to(device)
# model.eval()
#
#
# def inference(src):
#     raw_text = src
#     raw_text = " ".join(list(raw_text.replace(" ", "")))
#     history = [tokenize(tokenizer, raw_text)]
#     with torch.no_grad():
#         out_ids = sample_sequence(history, tokenizer, model, temperature,
#                                   top_p, top_k, no_sample, min_length, max_length, device)
#         out_text = tokenizer.decode(out_ids, skip_special_tokens=True)
#     return out_text
