from kazoo.client import KazooClient
import os
import time

# zkpath 的格式必须是 / 开头 结尾 /
zkpath = "/"
zk1 = KazooClient(hosts='192.168.0.41:32181')
zk1.start()


class BaseJudge:
    def __init__(self,def_path, jd_path=zkpath):
        self.def_path = def_path
        self.jd_path = jd_path

    def judgeZkPath(self):
        def_zk_children = zk1.get_children(self.def_path)
        if def_zk_children:
            for i in def_zk_children:
                self.def_path = self.def_path + i + '/'
                # 判断产生的新path有没有子目录或者文件 如果有继续叠加 如果没有删除路径的最后一层和新加的一层， 并重新生成path
                try:
                    z_c = zk1.get_children(self.def_path)
                    BaseJudge(self.def_path).judgeZkPath()
                except Exception as e:
                    # 删除路径的最后一层和新加的一层
                    self.def_path = self.def_path[:-1]
                    self.def_path = os.path.split(self.def_path)[0]
                    self.def_path = self.def_path[:-1]
                    self.def_path = os.path.split(self.def_path)[0]
                    self.def_path = self.def_path + '/' + i + '/'
                    BaseJudge(self.def_path).judgeZkPath()

        else:
            # 此处返回的self.def_path为需要写入的文件
            # 生成要创建的文件和目录路径
            zkFilePath = self.def_path[:-1]
            # dirPath = os.path.split(zkFilePath)[0][1:]
            dirPath = os.path.split(zkFilePath)[0].lstrip('/')
            # localFilePath = zkFilePath[1:]
            localFilePath = zkFilePath.lstrip('/')
            if not os.path.exists(dirPath):
                try:
                    os.makedirs(dirPath)
                except FileNotFoundError as fe:
                    os.mknod(localFilePath)
            zk_info = zk1.get(zkFilePath)
            if zk_info[0] == None:
                if not os.path.exists(localFilePath):
                    os.mknod(localFilePath)
                    print("因为zk中文件内容为空，%s文件已创建" % localFilePath)
            else:
                with open(localFilePath, 'w') as f:
                    f.write(zk_info[0].decode('utf-8'))
                    print("%s文件已写入" % localFilePath)

        return 'ok!'
a = BaseJudge(zkpath).judgeZkPath()
print("\033[44;37;1m %s \033[0m" % a)
