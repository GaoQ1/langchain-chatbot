'''
Description: 
Author: colin gao
Date: 2022-08-30 11:39:10
LastEditTime: 2023-05-18 18:35:33
'''
import os
from loguru import logger

currentdirPath = os.path.dirname(__file__)
logger_path = os.path.join(currentdirPath, '../logs/file_{time}.log')

logger.add(logger_path, rotation="1 MB", enqueue=True, backtrace=True, diagnose=True, serialize=True)