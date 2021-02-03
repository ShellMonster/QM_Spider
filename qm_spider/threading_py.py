from qm_spider import *
from qm_spider.top_keyword import *
import threading


threadLock = threading.Lock()

class Top_Keyword_Thread(threading.Thread):
    def __init__(self, threadID, *args):
        threading.Thread.__init__(self)
        self.appid = threadID
        self.name = Get_App_Appinfo(args[0]).get_subname()
        self.args = args

    def run(self):
        print ("===开启 %s 数据获取线程===" %(self.name))
        # 获取锁，用于线程同步
        threadLock.acquire()
        Get_Top_Keyword(self.args[0], self.args[1], self.args[2], self.args[3]).df_to_excel(self.args[4])
        # 释放锁，开启下一个线程
        threadLock.release()

class Top_Multiple_Keyword_Thread:
    def __init__(self, appid_list, keyword_hot_start, start_time, end_time, file_path='./'):
        self.appid_list = appid_list
        self.keyword_hot_start = keyword_hot_start
        self.start_time = start_time
        self.end_time = end_time
        self.file_path = file_path

    def multiple_Thread_run(self):
        threads = []

        for num, appid in enumerate(self.appid_list):
            thread = Top_Keyword_Thread(num+1, *[appid, self.keyword_hot_start, self.start_time, self.end_time, self.file_path])
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()