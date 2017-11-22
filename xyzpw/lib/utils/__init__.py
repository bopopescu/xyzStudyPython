#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014,掌阅科技
All rights reserved.

摘    要: 部分工具方法
创 建 者: WangLichao
创建日期: 2014-12-3
"""

import re
import sys
import string
import time
import hashlib
import inspect
import urlparse
import urllib
import urllib2
import datetime
from random import choice
from collections import Counter
from decimal import Decimal

from conf import log
from conf.settings import REQ_TIMEOUT


def toint(value, default=0):
    """转成 int 类别，避免异常
    """
    if not value:
        return default
    return int(value)


def tofloat(value, default=0.0):
    """转成 float 类别，避免异常
    """
    if not value:
        return default
    return float(value)


def tolen(value, default=0):
    """求长度,避免异常
    """
    if not value:
        return default
    return len(value)


def md5(input_str):
    """计算字符串的md5值
    Args:
        input_str: 输入字符串
    """
    return hashlib.md5(input_str).hexdigest()


def md5hex(word):
    """ MD5加密算法，返回32位小写16进制符号
    """
    if isinstance(word, unicode):
        word = word.encode("utf-8")
    elif not isinstance(word, str):
        word = str(word)
    m = hashlib.md5()
    m.update(word)
    return m.hexdigest()


def decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv


def decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        rv[key] = value
    return rv


def page_range(record_number, page_size, current_page):
    """计算分页时元索的区间以偏移量start 和 stop
    Args:
        record_number: 记录数
        page_size: 每页记录数
        current_page: 当前页
    Returns:
        分页的开始位置与结束位置
    """
    if current_page < 1:
        current_page = 1
    start = 0 if current_page == 1 else (current_page - 1) * page_size
    end = current_page * page_size - 1
    end = end if end < record_number else record_number - 1
    return (start, end)


def page_compute(record_number, page_size, current_page):
    """计算总页数和有效的当前页
    Args:
        record_number: 记录数
        page_size: 每页记录数
        current_page: 当前页
    """
    current_page = max(current_page, 1)
    page_total = (record_number + page_size - 1) / page_size
    current_page = min(current_page, page_total)
    return (current_page, page_total)


def update_dict_key(dict_value, key_map):
    """将字典中的key进行修改
    Args:
        dict_value:原始字典
        key_map: key映射dict类型
    Returns:
        返回修改后的字典
    举例：
        dict_value = {'a':1,'b':2}
        key_map = {'a':'c'}
        返回值new_val = {'c':1, 'b':2}
    """
    new_val = dict_value.copy()
    for k, v in key_map.items():
        if k not in new_val or v in new_val:
            continue
        new_val[v] = new_val.pop(k)
    return new_val


def merge_sort(sort_list):
    """对列表进行排序操作,如果有重复的需要排在最前面,
    如果没有重复的需要按顺序进行排序
    Args:
        sort_list: list类型
    """
    if len(sort_list) <= 1:
        return sort_list
    temp_counter = Counter(sort_list)
    return sorted(temp_counter, key=temp_counter.get, reverse=True)


def filter_dict_keys(orig, filter_keys):
    """将指定的字典的key过滤出来
    Args:
        orig: 待过滤的字典数据
        filter_keys: dict 需要过滤的字典的key
    Returns:
        返回过滤后的字典数据
    Examples:
        >>> orig = {'x_1': 1, 'y_1': 'xx', 'x_2': 2, 'z': 34}
        >>> filter_keys = {('x_1', 'x'): '', 'x_4':'', 'z': 1}
        >>> dest = filter_dict_keys(orig, filter_keys)
        >>> dest
        ... {'x':1, 'x_4': '', 'z': 34}
    """
    dest_dict = {}
    for k, v in filter_keys.iteritems():
        if isinstance(k, tuple):
            dest_dict[k[1]] = orig.get(k[0], v)
        else:
            dest_dict[k] = orig.get(k, v)
    return dest_dict


def camel_to_underline(camel_format):
    '''
        驼峰命名格式转下划线命名格式
    '''
    underline_format = ''
    if isinstance(camel_format, str) or isinstance(camel_format, unicode):
        for _s_ in camel_format:
            underline_format += _s_ if not _s_.isupper() else '_' + _s_.lower()
    return underline_format


def log_format(instance, func_name=None, params=None, error_info=None):
    """格式化log信息
    Args:
        instance: 类实例,当前业务环境下针对Handler类
        func_name: 类中调用返回为空的方法
        params: str 需要在log中说明的参数
        error_info: error级log的错误信息
    """
    if inspect.isclass(type(instance)):
        module_name = instance.__module__
        class_name = instance.__class__.__name__
        if not params:
            params = instance.request.uri
        end_time = time.time()
        spend_time = round((end_time - instance._start_time) * 1000, 2)
        if error_info:
            log.error('%s.%s faild spend_time:%sms params:(%s) error info:%s',
                      module_name,
                      class_name,
                      spend_time,
                      params,
                      error_info)
            return
        if func_name:
            log.warning('%s.%s call %s faild spend_time:%sms params:(%s)',
                        module_name,
                        class_name,
                        func_name,
                        spend_time,
                        params)
        else:
            log.warning('%s.%s faild spend_time:%sms params:(%s)',
                        module_name,
                        class_name,
                        spend_time,
                        params)


def sublist(lst, slice_size):
    """列表切片
    """
    if not slice_size:
        return lst
    sub = []
    result = []
    for i in lst:
        sub += [i]
        if len(sub) == slice_size:
            result += [sub]
            sub = []
    if sub:
        result += [sub]
    return result


def create_token(length=16):
    '''生成字母和数字的随机组合
    '''
    chars = list(string.letters + string.digits)
    salt = ''.join([choice(chars) for i in range(length)])
    return salt


def load_class(s):
    '''获取文件模块中的类对象
    '''
    path, klass = s.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, klass)


def setting_from_object(obj):
    '''从对象中获取配置项,全为大写的为配置
    '''
    settings = dict()
    for key in dir(obj):
        if key.isupper():
            settings[key.lower()] = getattr(obj, key)
    return settings


class ObjectDict(dict):
    '''对象字典，使用属性操作
    '''

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


def find_subclasses(klass, include_self=False):
    '''查找一个类的子类
    Args:
        include_self: 是否包含本身
    '''
    accum = []
    for child in klass.__subclasses__():
        accum.extend(find_subclasses(child, True))
    if include_self:
        accum.append(klass)
    return accum


def url_add_params(url, escape=True, **params):
    """
    add new params to given url
    """
    pr = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(pr.query))
    query.update(params)
    prlist = list(pr)
    if escape:
        prlist[4] = urllib.urlencode(query)
    else:
        prlist[4] = '&'.join(['%s=%s' % (k, v) for k, v in query.items()])
    return urlparse.ParseResult(*prlist).geturl()


def get_module_from_uri(uri, method='index'):
    '''根据uri获取module
    Args:
        uri: 请求地址
    Returns:
        module: 模块名称
    Examples:
        uri = '/auth/user/index'
        解析后
        module = '/auth/user'
    '''
    if not uri.endswith(method):
        return uri
    path_list = uri.split('/')
    module = '/'.join(path_list[0: -1])
    return module


def date_diff(date, days):
    """获取某个日期的差

    @days, int, 天数
    """
    date += datetime.timedelta(days=days)
    return date


def timestamp2date(timestamp, fmt="%Y-%m-%d"):
    """时间戳转日期

    @timestamp, float, 时间戳
    @fmt, str, 模板
    """
    return time.strftime(fmt, time.localtime(timestamp))


def date2timestamp(date, fmt="%Y-%m-%d"):
    """日期时间戳

    @date, str, 时间
    @fmt, str, 模板
    """
    return time.mktime(
        datetime.datetime.strptime(date, fmt).timetuple())


def get_local_ip():
    """获取本地IP
    """
    import commands
    return commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]


def sync_fetch(url, method="POST", data=None, timeout=REQ_TIMEOUT):
    """同步请求

    @method, str, 请求方式
    @data, dict, 请求数据
    """

    if data:
        if method == "GET":
            url += '?' + urllib.urlencode(data)
            data = None
        else:
            data = urllib.urlencode(data)
    content = None
    for _ in range(3):
        try:
            content = urllib2.urlopen(url, data, timeout=timeout)
            break
        except Exception:
            continue
    if not content:
        log.error("url:%s failed to fetch!" % url)
    return content


def force_unicode(data):
    """数据转换为unicode

    @data, 待转换的数据
    """
    if isinstance(data, str):
        return data.decode('utf-8')
    elif isinstance(data, list):
        for idx, i in enumerate(data):
            data[idx] = force_unicode(i)
    elif isinstance(data, dict):
        for i in data:
            data[i] = force_unicode(data[i])
    return data


def force_utf8(data):
    """数据转换为utf8

    @data: 待转换的数据
    """
    if isinstance(data, unicode):
        return data.encode('utf-8')
    elif isinstance(data, list):
        for idx, i in enumerate(data):
            data[idx] = force_utf8(i)
    elif isinstance(data, dict):
        for i in data:
            data[i] = force_utf8(data[i])
    return data


REGX = u'[\u4e00-\u9fa5a-zA-Z0-9]'


def intercept(data, regx=REGX):
    """过滤指定正则的数据

    @content, 内容
    @regx, unicode, 正则
    """
    if isinstance(data, basestring):
        content = force_unicode(data)
        res = re.findall(regx, content)
        return ''.join(res).encode("utf8")
    elif isinstance(data, list):
        for idx, i in enumerate(data):
            data[idx] = intercept(i)
    elif isinstance(data, dict):
        for i in data:
            data[i] = intercept(data[i])
    return data


def match_contain(arga, argb, ignore_symbol=True):
    """包含相似比较

    @arga, str, 字符串A
    @argb, str, 字符串B
    @ignore_symbol, bool, 是否忽略符号
    """
    if not arga or not argb:
        return False
    arga = force_unicode(arga)
    argb = force_unicode(argb)
    # 忽略符号
    if ignore_symbol:
        arga = intercept(arga)
        argb = intercept(argb)
    if len(arga) < len(argb):
        arga, argb = argb, arga
    return argb in arga


def match_similar(arga, argb, ratio=0.7):
    """相似度比较

    @arga, str, 字符串A
    @argb, str, 字符串B
    @ratio, float, 相似度比例
    """
    if not arga or not argb:
        return False

    arga = force_unicode(arga)
    argb = force_unicode(argb)

    count = 0  # 匹配数
    start = 0  # 匹配起始索引值

    if len(arga) < len(argb):
        arga, argb = argb, arga
    for s in argb:
        # 依次匹配
        pos = arga.find(s, start)
        if pos >= 0:
            start = pos + 1
            count += 1
    return float(count) / float(len(arga)) >= ratio


def diff_string(arga, argb, need_similar=False, ratio=0.7):
    """字符串比较

    @arga, str, 字符串A
    @argb, str, 字符串B
    @need_similar, bool, 是否比较相似度
    @ratio, float, 相似度比例
    """
    # 包含比较
    contain_flag = match_contain(arga, argb)
    if not contain_flag and need_similar:
        return match_similar(arga, argb, ratio)
    return contain_flag


def round_num(num, sep=2, out_type=float):
    """
    四舍五入
    :param sep: 保留小数点位数
    :return:
    """
    if not isinstance(num, Decimal):
        num = Decimal(str(num))
    return out_type(("{:.%sf}" % sep).format(num))


def to_str(strs):
    """
    数据转utf8
    """
    if isinstance(strs, unicode):
        return strs.encode("utf-8")
    return strs
