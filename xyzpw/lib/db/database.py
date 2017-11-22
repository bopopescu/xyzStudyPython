#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014,掌阅科技
All rights reserved.

摘    要: database.py
创 建 者: WangLichao
创建日期: 2015-01-26
"""
# pylint: disable=invalid-name
import peewee
from peewee import DoesNotExist
from peewee import OperationalError

from lib.db.hook import Model as _Model
from lib.utils import load_class

TYPE_MAP = {
    'char': 'CharField',
    'varchar': 'CharField',
    'enum': 'CharField',
    'text': 'TextField',
    'longtext': 'TextField',
    'mediumtext': 'TextField',
    'datetime': 'DateTimeField',
    'integer': 'IntegerField',
    'bool': 'BooleanField',
    'boolean': 'BooleanField',
    'int': 'IntegerField',
    'mediumint': 'IntegerField',
    'smallint': 'IntegerField',
    'float': 'FloatField',
    'real': 'FloatField',
    'bigint': 'BigIntegerField',
    'double': 'DoubleField',
    'numeric': 'DecimalField',
    'decimal': 'DecimalField',
    'timestamp': 'DateTimeField',
    'date': 'DateField',
    'time': 'TimeField',
    'tinyint': 'IntegerField',
    'blob': 'BlobField',
    'mediumblob': 'BlobField',
    'longblob': 'BlobField',
}


class DatabaseError(Exception):

    '''数据库类异常信息封装
    '''
    pass

MAX_CONNECTIONS = 10
# 一小时
STALE_TIMEOUT = 3600


class Database(object):

    '''db封装,自动查找数据库
    '''
    engine_map = {
        'mysql': 'peewee.MySQLDatabase',
        'mysqlpool': 'playhouse.pool.PooledMySQLDatabase',
    }
    current_user = None

    def __init__(self, database, engine='mysqlpool', **connect_kwargs):
        self.master = database['master']
        self.slaves = database['slaves']
        self.use_engine = engine
        self.engine = self.engine_map[engine]
        self.connect_kwargs = connect_kwargs
        self.load_database()
        self.Model = self.get_model_class()

    def load_database(self):
        '''加载数据库配置
        '''
        try:
            self.database_class = load_class(self.engine)
            assert issubclass(self.database_class, peewee.Database)
        except ImportError:
            raise DatabaseError('Unable to import: "%s"' % self.engine)
        except AttributeError:
            raise DatabaseError('Database engine not found: "%s"' % self.engine)
        except AssertionError:
            raise DatabaseError('Database engine not a subclass of peewee.Database: "%s"' % self.engine)

        self.master_database = self._connect(self.master, **self.connect_kwargs)
        self.slaves_database = [self._connect(slave, **self.connect_kwargs) for slave in self.slaves]

    def _connect(self, database, **kwargs):
        '''解析配置
        '''
        kwargs.update(self.parse_conf(database))
        if self.use_engine == 'mysqlpool':
            kwargs['max_connections'] = MAX_CONNECTIONS
            kwargs['stale_timeout'] = STALE_TIMEOUT
        return self.database_class(kwargs.pop('db'), **kwargs)

    @staticmethod
    def parse_conf(conf):
        '''将配置转换为字典结构,password中不允许有特殊字符比如:,/,:,@等
        Example:
            mysql://user:password@host:port/database
        '''
        schema = conf.split('://')[1]
        db_conf, db = schema.rsplit('/', 1)
        user_pwd, host_port = db_conf.split('@', 1)
        user, pwd = user_pwd.split(':', 1)
        host, port = host_port.split(':', 1)
        return dict(db=db,
                    host=host,
                    password=pwd,
                    port=int(port),
                    user=user)

    def get_model_class(self):
        '''获取基类model
        '''
        class BaseModel(_Model):

            '''BaseModel的封装
            '''
            current_user = None

            class Meta(object):
                '''元类
                '''
                database = self.master_database
                read_slaves = self.slaves_database

            @classmethod
            def one(cls, *query, **kwargs):
                '''获取单条数据
                Retruns:
                    返回单条数据不存在则返回None
                '''
                try:
                    return cls.get(*query, **kwargs)
                except DoesNotExist:
                    return None

            def __eq__(self, other):
                """提供直接根据==判断方法
                """
                return hasattr(other, "id") and self.id == other.id

            def __hash__(self):
                """提供hash支持
                """
                return hash(self.id)

        return BaseModel

    def connect(self):
        '''主从建立连接,如果连接关闭重试
        '''
        i = 0
        while i < 4:
            try:
                self.master_database.get_conn().ping(True)
                for slave in self.slaves_database:
                    slave.get_conn().ping(True)
                break
            except OperationalError:
                self.close()
                i = i + 1

    def close(self):
        '''关闭连接
        '''
        try:
            self.master_database.close()
            for slave in self.slaves_database:
                slave.close()
        except:
            pass
