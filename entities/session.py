import requests
import os
from loguru import logger
# 创建会话对象
session = requests.Session()
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

session.params = {"_sid": ''}

if os.path.exists(root_dir+ os.path.sep +'._sid'):
    with open(root_dir+os.path.sep +'._sid', 'r') as f:
        session.params = {"_sid": f.readline()}
        logger.info(f"load sid from file = {session.params}")

