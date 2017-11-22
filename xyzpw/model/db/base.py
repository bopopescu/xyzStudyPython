#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2015,掌阅科技
All rights reserved.

摘    要: base.py
创 建 者: tanshuai
创建日期: 2015-06-16
"""
# pylint: disable=unused-argument,protected-access
from datetime import datetime

from conf import log
from conf.settings import DATABASE, DATABASE_MAP
from lib.db.hook import post_delete, pre_save
from lib.db.database import Database

XYZ_DB = Database(DATABASE['xyz'])


def reconnect():
    '''重连数据库
    '''
    for v in DATABASE_MAP.itervalues():
        if v in globals():
            globals()[v].connect()


@post_delete(name='all_model_post_delete')
def post_delete_handler(sender, instance):
    '''所有的model删除后回调函数
    '''
    if Database.current_user is None:
        current_user = 'system'
    else:
        current_user = Database.current_user['account']
    log.info('account=%s,command=delete,table=%s,record_id=%s',
             current_user, instance._meta.db_table, instance.id)


@pre_save(name='all_model_pre_save')
def pre_save_handler(sender, instance, created):
    '''更新和保存前执行该回调
    '''
    if not isinstance(instance, sender):
        return
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fields = instance._meta.fields
    if created:
        # insert操作
        if 'create_time' in fields and not fields.get('create_time'):
            instance.create_time = time_now
        if 'create_user' in fields:
            instance.create_user = Database.current_user['account']
    else:
        # update操作
        if 'update_time' in fields and not fields.get("update_time"):
            instance.update_time = time_now
        if 'update_user' in fields:
            instance.update_user = Database.current_user['account']
