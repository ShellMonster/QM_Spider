import random,os
from multiprocessing.pool import Pool
from qm_spider.top_keyword import *
from qm_spider.threading_py import *


# class top_keyword_multiprocessing(top_multiple_keyword_Thread):
#     def main_process(self):
#         # 创建多个进程，表示可以同时执行的进程数量。默认大小是CPU的核心数
#         self.p = Pool(len(self.appid_list))
#         for appid in self.appid_list:
#             # 创建进程，放入进程池统一管理
#             self.p.apply_async(self.multiprocessing_run, args=(appid, self.keyword_hot_start, self.start_time, self.end_time, self.file_path, ))
#         # 如果我们用的是进程池，在调用join()之前必须要先close()，并且在close()之后不能再继续往进程池添加新的进程
#         self.p.close()
#         # 进程池对象调用join，会等待进程吃中所有的子进程结束完毕再去结束父进程
#         self.p.join()
#
#     def multiprocessing_run(self, appid):
#         self.appname = get_app_appinfo(appid).get_subname()
#         print("【%s】子进程开始，进程ID：%d" % (self.appname, os.getpid()))
#         start = time.time()
#         get_top_keyword(appid, self.keyword_hot_start, self.start_time, self.end_time, self.file_path).df_to_excel()
#         end = time.time()
#         print("%s子进程结束，进程ID：%d。耗时0.2%f" % (self.appname, os.getpid(), end - start))

@qm_auth_check  # 登录检查；
def top_keyword_multiprocessing(appid_list, keyword_hot_start, start_time, end_time, file_path='./'):
    # 创建多个进程，表示可以同时执行的进程数量。默认大小是CPU的核心数
    p = Pool(len(appid_list))
    for appid in appid_list:
        # 创建进程，放入进程池统一管理；
        p.apply_async(multiprocessing_run, args=(appid, keyword_hot_start, start_time, end_time, file_path, ))
    # 如果我们用的是进程池，在调用join()之前必须要先close()，并且在close()之后不能再继续往进程池添加新的进程
    p.close()
    # 进程池对象调用join，会等待进程吃中所有的子进程结束完毕再去结束父进程
    p.join()

def multiprocessing_run(appid, keyword_hot_start, start_time, end_time, file_path):
    time.sleep(random.random() * 3)
    app_name = Get_App_Appinfo(appid).get_subname().replace(' ', '')
    print("【%s】子进程开始，进程ID：%d" % (app_name, os.getpid()))
    old_seconds = datetime.datetime.now()
    Get_Top_Keyword(appid, keyword_hot_start, start_time, end_time, app_name).df_to_excel(file_path)
    now_seconds = datetime.datetime.now()
    interval_seconds =round((now_seconds - old_seconds).seconds/60, 2)
    print("【%s】子进程结束，进程ID：%d；当前 %s ，耗时%s分钟" % (app_name, os.getpid(), str(now_seconds)[:19], interval_seconds))
