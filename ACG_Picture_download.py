# -* - coding: UTF-8 -* -
import urllib.request
import os
import threading
import json
import socket
import time
import re
from  threading import Timer
import enum
import tkinter as tk

# #建立线程池，并启动线程直到结束
def parallel(infos):
    startTime = time.time()
    threads=[]
    counts = range(len(infos))
    for i in counts:
        t=MyThread(downloadImage,(infos[i],downloadFile,),downloadImage.__name__)
        threads.append(t)
    for i in counts:
        threads[i].start()
    for i in counts:
        threads[i].join()
    print('花费时间:%s'%(time.time()-startTime))

# #自定义线程类
class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
        self.res=self.func(*self.args)

# # #单线程测试
# def parallel(infos,downloadFile):
#     counts = range(len(infos))
#     for i in counts:
#         downloadImage(infos[i],downloadFile)
#     print("OK")

#根绝imageUrl下载图片到本地
def downloadImage(info,downloadFile):
    imageUrl = info["url"]
    imagePName = str(info["pname"])
    imageCName = str(info["cname"])

    print(imagePName)

    imagePName = re.sub("[\s+\.\!\/_,$%^*+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "-",imagePName)

    dir = "./"+downloadFile+"/"+imagePName+"/"

    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
            print("创建目录成功 %s"%dir)
    except:
        print("创建目录失败 %s"%dir)
        return

    imageType = imageUrl.split('.')[-1]
    path = dir+imageCName + "."+imageType
    if os.path.exists(path):
        print("文件已存在")
        return
    else:
        print("文件不存在")
        try:
            data = urllib.request.urlopen(imageUrl).read()
        except Exception as e:
            print("下载失败",e)
            return
        try:
            f = open(path,"wb")
            f.write(data)
            f.close()
            print("保存成功"+path)
        except:
            print("保存失败")
            return

#下载整个相册
def downloadAlbum(albumName,albumIndex,downloadUrl):
    reqs =[]
    try:
        res = urllib.request.urlopen(downloadUrl+"/index?index="+albumIndex+"&mode=3")
        resAlbum = json.loads(res.read().decode('utf-8'))
    except:
        print("获取专辑信息失败")
        return
    for Album in resAlbum['info']:
        # print("文件名：" + Album['tags'] + " 文件ID：" + str(Album['id']) + " 下载地址：" + Album['url'])
        a = {}
        a['pname'] = albumName
        a['cname'] = Album['id']
        a['url'] = Album['url']
        reqs.append(a)
    parallel(reqs)

# 获取专辑信息
def downloadIndex(downloadUrl,downloadFile):
    fileFolder="./"+downloadFile+"/"
    if not os.path.exists(fileFolder):
        os.mkdir(fileFolder)
    timeout = 10
    socket.setdefaulttimeout(timeout)

    try:

        print(downloadUrl+"/index?index=mainindex&mode=3")

        res = urllib.request.Request()
        res = urllib.request.urlopen(downloadUrl+"/index?index=mainindex&mode=3")
        resAlbum = json.loads(res.read().decode('utf-8'))
        print(resAlbum)
    except Exception as e:
        print("获取索引失败",e)
        return
    for Album in resAlbum['indexes']:
        print("开始下载专辑" + Album['des'] + " 索引是：" + Album['index'])
        # 下载专辑封面信息
        pic = {}
        pic['pname'] = '封面'
        pic['cname'] = Album['des']
        pic['url'] = Album['url']
        downloadImage(pic,downloadFile)
        # 下载专辑
        downloadAlbum(Album['des'], Album['index'],downloadUrl)
    print("结束任务")



# 主程序
if __name__ == "__main__":

    #下载地址
    downloadUrl = "http://acgstay.mavericks.lol:8888"
    #下载文件夹
    downloadFile= "ACG"

    # #下载地址
    # downloadUrl = "http://cosplay.mavericks.lol:8887"
    # #下载文件夹
    # downloadFile= "COS"

    timer_interval=240
    t=Timer(timer_interval,downloadIndex(downloadUrl,downloadFile))
    t.start()
    while True:
        pass
    print("结束")
