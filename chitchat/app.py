from flask import Flask, request
import json
# from api import inference
from tool import inference


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/get_chat', methods=['GET'])
def chat():
    return_dict = {
        'retcode': '0',
        'retmsg': '成功',
        'data': {
            'question': None,
            'delay': '',
            'chatAnswers': [],
        }
    }
    if len(request.args) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    get_data = request.args.to_dict()
    text = get_data.get('text')
    response, ppl, delay = inference(text)
    return_dict['data']['question'] = text
    return_dict['data']['ppl'] = round(ppl, 4)
    return_dict['data']['chatAnswers'].append(response)
    return_dict['data']['delay'] = str(round(delay, 4)) + 'ms'
    return json.dumps(return_dict, ensure_ascii=False)


if __name__ == '__main__':
    # 10.192.9.83:20009
    # 10.192.9.83:20034
    # app.run('10.192.9.83', 20034)
    # app.run('0.0.0.0', 8000)
    app.run()
