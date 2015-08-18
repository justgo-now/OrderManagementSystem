# coding: utf-8

""" 时间处理函数库

    定义了相关的时间处理函数

"""

import datetime


def todayfstr(format_str='%Y-%m-%d %H:%M:%S'):
    """ 获取今天的时间字符串
    比如 "2013-09-09 09:09:23"
    :para format_str: 一个有效的描述时间的格式
    """

    return datetime.datetime.now().strftime(format_str)


def get_date_time_str():
    now_time = todayfstr()  # 当前时间
    str_time = str(now_time)[:10]  # 截取当前时间。去掉时分秒
    args_time = '%' + str_time + '%'
    return args_time