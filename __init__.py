from nonebot import get_driver
from nonebot.adapters.cqhttp.permission import GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_keyword
from .config import Config
from nonebot import on_command
from nonebot.adapters import Bot, Event, MessageSegment, Message
from nonebot.adapters.cqhttp import Bot,Message,GroupMessageEvent, Event
import random
from . import data_source
from zhixuewang import login
import time
import os
import re
from loguru import logger

global_config = get_driver().config
config = Config(**global_config.dict())

scorequest = on_command("查询智学网分数", priority=5, block=True)
scorequestSpecial = on_command("查询智学网考试分数", priority=5, block=True)
about = on_command("关于智学查分系统",priority=5, block=True)
inited = on_command("初始化智学查分",priority=5,permission=GROUP_OWNER | SUPERUSER, block=True)
newQueryKey = on_command("绑定智学网账户",priority=5, block=True)

@about.handle()
async def handle(bot: Bot, event: Event, state: dict):
    msg = '关于 智学分数查询系统 @rs-software/zhixue\n' \
    '查询智学网分数 <学号>#<查询密钥>\n'\
    '绑定智学网账户 <学号>#<密码>(不会保存，请在私聊时使用！)\n' \
    '查询智学网考试分数 <学号>#<查询密钥>#<考试名>\n' \
    '关于智学查分系统 本页面\n' \
    '版本：' + Config.Config.version + '\n' \
    '作者：RisConn Software(consumer@risconn.com)\n' \
    '目前授权的账号：\n'
    for i in range(0,len(Config.Config.userId)):
        msg += '| ' + Config.Config.userId[i]
    Msg = Message(str(msg))
    await about.finish(Msg)

@newQueryKey.handle() # 绑定智学网账户 123#querykey
async def handle(bot: Bot, event: Event, state: dict):
    args = str(event.get_message()).strip()
    if event.dict()["message_type"] != "private":
        Msg = Message(str('您不在私聊环境中，无法执行'))
        await newQueryKey.finish(Msg)
    uid = args.split("#")[0]
    key = args.split("#")[1]
    randN1 = random.randint(10000,32767)
    time.sleep(1)
    randN2 = random.randint(10000,32767)
    keys = str(randN1) + str(randN2)
    Config.Config.userId.append(uid)
    Config.Config.userPassword.append(key)
    Config.Config.specKey.append(keys)
    with open("G:/" + uid + ".secret.txt") as f:
        f.write(uid + "-" + key + "-" + keys)
    msg = '查询密钥:\n' + keys + ",\n请勿向他人透露！"
    Msg = Message(str(msg))
    # await bot.send(event=event, message=Message(MessageSegment.text(msg)))
    await newQueryKey.finish(Msg)

@scorequestSpecial.handle() # 查询智学网分数 123#querykey
async def handle(bot: Bot, event: Event, state: dict):
    args = str(event.get_message()).strip()
    uid = args.split("#")[0]
    key = args.split("#")[1]
    name = args.split('#')[2]
    ind = Config.Config.specKey.index(key)
    pwd = Config.Config.userPassword[ind]
    zxw = login(uid,pwd)
    # msg = '你的分数:\n' + str(zxw.get_self_mark(str(name))) + "\n"
    return await bot.send(event=event, message=Message('你的分数:\n' + str(zxw.get_self_mark(str(name))) + "\n"))
    Msg = Message(str(msg))
    # await bot.send(event=event, message=Message(MessageSegment.text(msg)))
    await scorequestSpecial.finish(Msg)

@scorequest.handle() # 查询智学网分数 123#querykey
async def handle(bot: Bot, event: Event, state: dict):
    args = str(event.get_message()).strip()
    uid = args.split("#")[0]
    key = args.split("#")[1]
    ind = Config.Config.specKey.index(key)
    pwd = Config.Config.userPassword[ind]
    zxw = login(uid,pwd)
    msg = '你的分数:\n' + str(zxw.get_self_mark()) + "\n"
    Msg = Message(str(msg))
    # await bot.send(event=event, message=Message(MessageSegment.text(msg)))
    await scorequest.finish(Msg)

@inited.handle()
async def handle(bot: Bot, event: Event, state: dict):
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
    msg = '初始化智学查分系统完成'
    Msg = Message(msg)
    # await bot.send(event=event, message=Message(MessageSegment.text(msg)))
    await inited.finish(Msg)
