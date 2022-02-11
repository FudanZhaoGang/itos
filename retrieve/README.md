### 运行方法

- 打开本地的 elasticsearch（需要手动安装）
- 运行 search_word.py 新建索引
- 运行 get_similarity.py 测试全部数据集（训练集+验证集+验证集）上的准确率 
- 运行 run.py 建立本地接口

```shell
service elasticsearch start
python search_word.py 
python get_similarity.py 
python run.py
```
