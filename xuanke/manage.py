import logging.handlers
import os

from config import cur_dir
from xuanke import Xuanke


def logging_config(logging_name='./xuanke.log', stream_log=False, relative_path="."):
    """
    :param logging_name:  log名
    :param stream_log: 是否把log信息输出到屏幕,标准输出
    :param relative_path: 相对路径，log文件相对于logs的位置（父目录，当前目录等）
    :return: None
    """
    log_handles = [logging.handlers.RotatingFileHandler(
        os.path.join(cur_dir, relative_path, os.path.basename(logging_name)),
        maxBytes=20 * 1024 * 1024, backupCount=5, encoding='utf-8')]
    if stream_log:
        log_handles.append(logging.StreamHandler())
    logging.basicConfig(
        handlers=log_handles,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s %(filename)s %(funcName)s %(lineno)s - %(message)s"
    )


logging_config("xuanke.log")

if __name__ == "__main__":
    username = "用户名"
    password = "密码"
    listening_course = ["机器学习", "自然语言处理", "操作系统高级课程"]  # "机器学习", "自然语言处理",
    page_fresh_frequency = 5 * 60  # 选课页面刷新间隔，单位s
    course_fresh_frequency = 1 * 60  # 课程容量刷新间隔，单位s
    wechat_info = False  # 是否启用微信通知
    info_person = False  # 是否通知个人
    auto_select = True  # 有空缺自动选课
    parm = {"username": username, "password": password,
            "listening_course": listening_course,
            "page_fresh_frequency": page_fresh_frequency,
            "course_fresh_frequency": course_fresh_frequency,
            "wechat_info": wechat_info, "info_person": info_person,
            "auto_select": auto_select}
    xuanke = Xuanke(**parm)
    xuanke.run()
