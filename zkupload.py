#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kazoo.client import KazooClient
import pickle
import os
import time

zk1 = KazooClient(hosts='192.168.0.41:32181')
zk1.start()
# path 的格式必须是 / 开头 结尾没有 /
# 指定zk的第一级目录 下面还可以有两层 例如：导入本机当前目录 configs/msdbConf/lang/stopwords_nl.txt文件到zk /configs/msdbConf/lang/stopwords_nl.txt
# 可以直接写 path = '/configs'
path = '/overseer_elect'


def UpLoad(up_path):
    print(up_path, 'upppppppppppppppppppppp')
    zk1.ensure_path(up_path)
    with open(up_path[1:]) as f:
        try:
            zk1.create(up_path, b" ")
            zk1.set(up_path, f.read().encode('utf-8'))
        except:
            zk1.set(up_path, f.read().encode('utf-8'))


# 第一次获取目录下的文件列表
f_list = os.listdir(path[1:])
for i1 in f_list:
    i1_path = path[1:] + os.sep + i1
    # 目录下面如果是目录 则产生新的路径
    if os.path.isdir(i1_path):
        print(i1_path)
        # 第二次获取目录下的文件列表
        list2 = os.listdir(i1_path)
        for i2 in list2:
            i2_path = i1_path + os.sep + i2
            # 第二次判断 目录下面如果是目录 则产生新的路径
            if os.path.isdir(i2_path):
                list3 = os.listdir(i2_path)
                for i3 in list3:
                    print(os.sep + i2_path + os.sep + i3)
                    UpLoad(up_path=os.sep + i2_path + os.sep + i3)
            elif os.path.isfile(i2_path):
                UpLoad(up_path=os.sep + i2_path)
    elif os.path.isfile(i1_path):
        UpLoad(up_path=os.sep + i1_path)

zk1.stop()

