class Config(object):
    data_path = "data.txt"
    dataset_size = 787
    batch_size = 32
    num_class = 7
    pretrained_path = 'chinese-bert'
    epoch = 10
    device = 'cuda'
    save_path = '/remote-home/hxlin/project/IntentionRecognition/bert.pt'
    intentions_path = "/remote-home/hxlin/project/IntentionRecognition/intention.json"
