#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from datetime import datetime
from loguru import logger
from nonebot.adapters.cqhttp import MessageSegment, Message
from .config import Config

v = Config.Config.version
def init_data():
    rootdir = Config.Config.rootpath
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            f = open(path)
            data = f.read()
            Config.Config.userId.append(data.split('-')[0])
            logger.info(data.split('-')[0] + "-" + data.split('-')[1] + "-" + data.split('-')[2])
            Config.Config.userPassword.append(data.split('-')[1])
            Config.Config.specKey.append(data.split('-')[2])
            f.close()


logger.info("感谢使用智学查分系统\n版本：" + v + "。Copyright (c) 2021 RisConn Software")
init_data()
logger.success("数据库初始化成功")
