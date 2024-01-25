import os
from pathlib import Path
from enum import Enum
import inspect

class Const():
    FileName = 'FileName' #策划文件名称
    FilePath = "FilePath"  # 策划文件路径
    DesignDoc = 'DESIGN_DOC' #策划文档内容
    Document: str = "Document.md" #技术文档
    ArchitectureDiagram = "ArchitectureDiagram.jar" #架构图



class BlackBoard():
    task = 'test'
    blackboard = "blackboard.txt"

    def save_task(self,task):
        self.task = task

    def save_to_blackboard(self, msg: dict):
        """在黑板中保存信息"""
        with open(self.get_blackboard_path(), 'a', encoding='utf-8') as f:
            for k, v in msg.items():
                f.write(f'{k}={v}\n')

    def get_blackboard_path(self):
        """获取黑板文件路径"""
        file_path = f'{self.get_workspace_path()}/{self.task}_{self.blackboard}'
        return file_path

    def read_blackboard(self,key: str) -> str:
        """从黑板中读取信息"""
        with open(self.get_blackboard_path(), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                datas = line.split('=')
                if datas[0] == key:
                    return datas[1]

        return ''

    def get_workspace_path(self):
        path = Path(__file__).parent.parent.joinpath(f'workspace/{self.task}')
        # 如果文件夹不存在，则创建文件夹
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def save_doc(self,file_name,content):
        with open(f'{self.get_workspace_path()}/{file_name}', mode='w', encoding='utf-8') as f:
            f.write(content)

    def get_doc(self,file_name):
        with open(f'{self.get_workspace_path()}/{file_name}', mode='r', encoding='utf-8') as f:
            return f.read()

def get_script_path():
  # 获取当前帧的调用者
  caller_frame = inspect.currentframe().f_back
  try:
      # 获取调用者的代码对象
      code_obj = caller_frame.f_code
      # 获取调用者的文件名
      filename = code_obj.co_filename
      # 返回调用者的父文件夹路径
      return os.path.dirname(os.path.abspath(filename))
      #return os.path.abspath(filename)
  finally:
      # 释放当前帧
      del caller_frame

def get_prompt(prompt_name: str = 'prompt') -> str:
    """从文件中读取提示"""
    caller_frame = inspect.currentframe().f_back
    try:
        # 获取调用者的代码对象
        code_obj = caller_frame.f_code
        # 获取调用者的文件名
        filename = code_obj.co_filename
        # 返回调用者的父文件夹路径
        dir_path = os.path.dirname(os.path.abspath(filename))
        prompt_path = os.path.join(dir_path, f'{prompt_name}.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    finally:
        # 释放当前帧
        del caller_frame


#共享黑板
ShareBlackBoard = BlackBoard()


