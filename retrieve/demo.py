from retrival_bert_server import Cross_Encoder
from transformers import BertTokenizer, BertModel
from get_similarity import load_intent, load_pretrained_model, load_finetune_model
from get_similarity import score_query_and_intent_pretrained, filter
from utils import load_answer
from search_word import keywordSearch
import time
import torch
import copy


def normalization(x, top=10, bottom=-10):
    if x >= top:
        return 1

    if x <= bottom:
        return 0

    return (x - 10) / 20 + 1


def metric(query, tokenizer, model, topN=2):
    my_index = "word2vec_index"
    my_doc = "my_doc"

    result, t = keywordSearch(keywords1=query, my_index=my_index, my_doc=my_doc)
    re_label = [item[0] for item in result]
    start_time = time.time()

    topN_score, topN_index, topN_intent = filter(query, re_label, tokenizer, model, topN=topN)

    end_time = time.time()

    answer_dict = load_answer()
    topN_answer = [answer_dict[str(index)] for index in topN_index]

    return [(normalization(score), answer) for score, answer in zip(topN_score, topN_answer)], end_time - start_time


if __name__ == "__main__":
    return_dict = {
        "retcode": "0",
        "retmsg": "成功",
        "data": {
            "text": "客服电话多少",
            "scenes_id": "3183157d-69de-11eb-af8b-000c295f8ad5",
            "queryKnowledge": [
                {
                    "answer": "我们丰收银行的客服电话是二五五八零",
                    "score": "0.873",
                    "rank": 1
                }
            ]
        }
    }

    query = "你刚才说的是什么产品"
    tokenizer, model = load_finetune_model()
    top_info, timing = metric(query, tokenizer, model, topN=3)

    for i, info in enumerate(top_info):
        print("Top{}_score = {}".format(i + 1, info[0]))
        print("Top{}_score = {}".format(i + 1, info[1]))
        print("\n")
    print("Time used = {}s".format(timing))

    return_list = []
    for i, info in enumerate(top_info):
        targt = copy.deepcopy(return_dict)
        targt["data"]["queryKnowledge"][0]["answer"] = info[1]
        targt["data"]["queryKnowledge"][0]["score"] = info[0]
        targt["data"]["queryKnowledge"][0]["rank"] = i + 1
        return_list.append(targt)

    print(return_list)
