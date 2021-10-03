from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here

    class Config:
        extra = "ignore"
        rootpath = "G:/" # 存储智学网文件位置，必须是空文件夹
        version = "0.10b2"
        userId = []
        userPassword = []
        specKey = [] #查询序列号，防止密码泄露
        operationNeedNext = 0 #0 未指定，1 确认，-1 取消
        userLoginStat = {}