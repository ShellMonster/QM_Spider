# QM_Spider
QM_Spider

## 安装
* 首次安装
```
pip3 install qm_spider
```
* 升级
```
pip3 install --upgrade qm_spider
```


## 文件说明：
### init.py
  * 根文件，主要存储抓取qimai.cn的方法；
  * 其中也存储了一些其他的方法：
    * 例如DingDing_Push类，封装了常用的text、markdown格式的钉钉推送，使用对应的文字或markdown格式代入调用即可；
    ```python
    # 举例调用示例：正常运行成功后，推送状态;
    DingDing_Push(push_title='推送消息的标题', push_status='状态，字符串，默认成功提示', push_url='推送的钉钉token').status_push()
    ```
    * 例如Qimai_Outside_Tool类，封装了常用的一些转换方法，例如时间戳转日期、转标准日期、字符匹配、星期几计算、json转df、list转df等方法；
### email_py
  * 邮件发送文件，主要存储了发送邮件的方法，封装zmail的常用发送函数；

  
