#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2015,掌阅科技
All rights reserved.

摘    要: test_api_auth
创 建 者: ZhangXu
创建日期: 2016/3/23 14:32
"""
import os
import sys
import json
import unittest

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from apiauth import APIAuthFactory
from model.db.api_auth import ApiAuth

GLOBAL_BOOK_LIST = []
GLOBAL_CHAPTER_DICT = {}


class TestApiAuth(unittest.TestCase):
    """
    测试接口模块
    """

    def setUp(self):
        client_id = 2
        self.req_info = {
            "req_method": "",
            "client_name": "",
            "client_id": client_id,
            "book_id": "",
            "chapter_id": "",
            "res_type": "json",
        }
        self.auth_info = ApiAuth.one(id=client_id)

    def tearDown(self):
        del self.req_info
        del self.auth_info

    def testBookList(self):
        """
        测试书籍列表
        Returns:

        """
        self.req_info["req_method"] = "bookList"
        test_field = ("name", "bookId")
        generate_response = APIAuthFactory.create(self.req_info, self.auth_info).generate_response()
        generate_response = json.loads(generate_response)

        self.assertIsInstance(generate_response, list)
        for book in generate_response:
            self.assertIsInstance(book, dict)
            for field in test_field:
                self.assertIn(field, book)
                self.assertIn(field, book)
        globals()["GLOBAL_BOOK_LIST"] = [str(val["bookId"]) for val in generate_response]

    def testBookInfo(self):
        """
        测试书籍信息
        Returns:

        """
        self.req_info["req_method"] = "bookInfo"
        test_field = ("author", "bookId", "brief", "category", "categoryId",
                           "completeStatus", "cover", "createTime", "displayName",
                           "keywords", "name", "wordCount")
        for book_id in globals()["GLOBAL_BOOK_LIST"]:
            self.req_info["book_id"] = book_id
            generate_response = APIAuthFactory.create(self.req_info, self.auth_info).generate_response()
            generate_response = json.loads(generate_response)
            self.assertIsInstance(generate_response, dict)
            for field in test_field:
                self.assertIn(field, generate_response)

    def testChapterList(self):
        """
        测试章节列表
        Returns:

        """
        self.req_info["req_method"] = "chapterList"
        test_field = ("chapterId", "chapterOrder", "title", "createTime")
        for book_id in globals()["GLOBAL_BOOK_LIST"]:
            self.req_info["book_id"] = book_id
            generate_response = APIAuthFactory.create(self.req_info, self.auth_info).generate_response()
            generate_response = json.loads(generate_response)
            self.assertIsInstance(generate_response, list)
            for chapter in generate_response:
                self.assertIsInstance(chapter, dict)
                for field in test_field:
                    self.assertIn(field, chapter)
            globals()["GLOBAL_CHAPTER_DICT"][book_id] = [str(val["chapterId"]) for val in generate_response]

    def testChapterInfo(self):
        """
        测试章节信息
        Returns:

        """
        self.req_info["req_method"] = "chapterInfo"
        test_field = ("title", "chapterId", "chapterOrder", "content",
                           "createTime", "bookId")
        for book_id in globals()["GLOBAL_BOOK_LIST"]:
            self.req_info["book_id"] = book_id
            for chapter_id in globals()["GLOBAL_CHAPTER_DICT"][book_id]:
                self.req_info["chapter_id"] = chapter_id
                generate_response = APIAuthFactory.create(self.req_info, self.auth_info).generate_response()
                generate_response = json.loads(generate_response)
                self.assertIsInstance(generate_response, dict)
                for field in test_field:
                    self.assertIn(field, generate_response)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestApiAuth("testBookList"))
    suite.addTest(TestApiAuth("testBookInfo"))
    suite.addTest(TestApiAuth("testChapterList"))
    suite.addTest(TestApiAuth("testChapterInfo"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
