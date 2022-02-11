from flask import Flask, request, jsonify
import json
import torch
from config import Config
import torch.nn.functional as F

app = Flask(__name__)
# 防止中文乱码
app.config['JSON_AS_ASCII'] = False

# 加载模型，默认设备GPU
device = torch.device("cuda")
model = torch.load(Config.save_path).to(device)

# 加载意图列表
with open(Config.intentions_path, "r", encoding="gbk") as f:
    intentions = json.load(f)


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/getIntent", methods=['GET', 'POST'])
def getIntent():
    text = request.args.get("text")
    scenes_id = request.args.get("scenes_id")

    retcode = 0
    retmsg = "成功"
    text = ("",) if text is None else (text,)
    output = model(text)
    scores = F.softmax(output, dim=1).tolist()[0]
    intents = [{"intent": intentions[i], "score": scores[i]} for i in range(len(intentions))]

    # 判断是否含有中文
    if not is_contain_chinese(text[0]):
        retcode = 1
        retmsg = "无效字符串"

    json_dict = {
        "retcode": retcode,
        "retmsg": retmsg,
        "data": {
            "text": text[0],
            "scenes_id": scenes_id,
            "intents": intents
        }
    }

    return jsonify(json_dict)


if __name__ == "__main__":
    app.run()
