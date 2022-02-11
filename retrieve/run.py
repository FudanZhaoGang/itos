from flask import Flask, request
import json
from demo import metric
from get_similarity import load_finetune_model
import copy

app = Flask(__name__)

tokenizer, model = load_finetune_model()


# 只接受get方法访问
@app.route("/getKnowledge", methods=["GET", "POST"])
def check():
    # 默认返回内容
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
    # 判断入参是否为空
    if request.args is None:
        return json.dumps(return_dict, ensure_ascii=False)

    get_data = request.args.to_dict()
    text = get_data.get('text')
    scenes_id = get_data.get('scenes_id')
    target_num = get_data.get("target_num")

    if text == None:
        text = "你刚才说的是什么产品"
    if scenes_id == None:
        scenes_id = "3183157d-69de-11eb-af8b-000c295f8ad5"
    if target_num == None:
        target_num = 2

    return_dict["data"]["text"] = text
    return_dict["data"]["scenes_id"] = scenes_id

    top_info, timing = metric(text, tokenizer, model, topN=int(target_num))

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

    return json.dumps(return_list, ensure_ascii=False)


if __name__ == "__main__":
    app.run()
