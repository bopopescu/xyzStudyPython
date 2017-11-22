__author__ = 'root'

import chardet


def to_unicode(input_str):
    """

    :param input_str:
    :return:
    """
    pass


def join_and_wash(split, data_list):
    """
    join and wash
    :param split:
    :param data_list:
    :return:
    """
    return split.join(data_list).replace("\r", "").replace("\t", "").replace("\n", "").strip()


def remove_none_item(item):
    """
    remove none item
    :param dic:
    :return:
    """
    dic = dict(item)
    dic_keys = [k for k in dic.iterkeys()]
    for k in dic_keys:
        if dic[k] in ("", None):
            del dic[k]
    return dic

if __name__ == "__main__":
    dic = {"a": None, "b": "sdf", "c": ""}
    print dic
    print remove_none_item(dic)