# coding:utf-8
# from lib.common import *
from common import *
import os, platform, sys


# 分析主机上webshell类文件
# 1、提取tomcat的web目录，进行安全扫描
# 2、提取jetty的web目录，进行安全扫描
# 3、提取nginx的web目录，进行安全扫描
# 4、提取apache的web目录，进行安全扫描
# 5、提取jboss的web目录，进行安全扫描
# 6、提取weblogic的web目录，进行安全扫描
# 7、提取resin的web目录，进行安全扫描


class Webshell_Analysis:
    def __init__(self):
        # WEB目录
        self.webroot_list = ['/var/www/', '/usr/share/nginx/html/',
                             '/Users/grayddq/Grayddq/01.mygit/15.GScan/GScan/lib/test']
        # yara的webshell规则
        self.rule = sys.path[0] + '/webshell_rule/'
        # 恶意webshell列表
        self.webshell_list = []

    # 将yara规则编译
    def getRules(self, yara):
        index = 0
        filepath = {}
        for dirpath, dirs, files in os.walk(self.rule):
            for file in files:
                ypath = os.path.join(dirpath, file)
                key = "rule" + str(index)
                filepath[key] = ypath
                index += 1
        yararule = yara.compile(filepaths=filepath)
        return yararule

    def scan_web(self):
        for webroot in self.webroot_list:
            if not os.path.exists(webroot): continue
            for file in gci(webroot):
                if not os.path.exists(file): continue
                if os.path.isdir(file): continue
                if (os.path.getsize(file) == 0) or (
                        round(os.path.getsize(file) / float(1024 * 1024)) > 10): continue
                fp = open(file, 'rb')
                matches = self.yararule.match(data=fp.read())
                if len(matches):
                    self.webshell_list.append(file)
                else: print file

    def run(self):
        DEPENDENT_LIBRARIES_2_6 = "/egg/yara_python-3.5.0-py2.6-linux-2.32-x86_64.egg"
        DEPENDENT_LIBRARIES_3_10 = "/egg/yara_python-3.5.0-py2.7-linux-3.10-x86_64.egg"
        DEPENDENT_LIBRARIES_4_20 = "/egg/yara_python-3.8.1-py2.7-linux-4.20-x86_64.egg"
        DEPENDENT_LIBRARIES_16 = "/egg/yara_python-3.5.0-py2.7-macosx-10.12-x86_64.egg"
        DEPENDENT_LIBRARIES_17 = "/egg/yara_python-3.5.0-py2.7-macosx-10.13-x86_64.egg"
        _kernel = platform.release()
        if _kernel.startswith('2.6'):
            sys.path.append(sys.path[0] + DEPENDENT_LIBRARIES_2_6)
        elif _kernel.startswith('3.') and ("6." in str(platform.dist())):
            sys.path.append(sys.path[0] + DEPENDENT_LIBRARIES_2_6)
        elif _kernel.startswith('3.'):
            sys.path.append(sys.path[0] + DEPENDENT_LIBRARIES_3_10)
        elif _kernel.startswith('4.'):
            sys.path.append(sys.path[0] + DEPENDENT_LIBRARIES_4_20)
        elif _kernel.startswith('16.'):
            sys.path.append(sys.path[0] + DEPENDENT_LIBRARIES_16)
        elif _kernel.startswith('17.'):
            sys.path.append(sys.path[0] + DEPENDENT_LIBRARIES_17)
        else:
            print(u'不支持此内核的Webshell扫描')
            return
        import yara

        # 编译规则
        self.yararule = self.getRules(yara)
        self.scan_web()


if __name__ == '__main__':
    info = Webshell_Analysis()
    info.run()
    print(u"Webshell文件检查异常如下：")
    for info in info.webshell_list:
        print(info)
