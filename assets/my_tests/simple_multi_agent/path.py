import os
from os import path

DocPath = "CodeDoc"

def get_doc_path()->str:
    real_path = os.getcwd() + '/' + DocPath
    if not path.exists(real_path):
        #如果不存在则创建目录（包含父目录）
        os.makedirs(real_path)
    return real_path

DocName = ''
