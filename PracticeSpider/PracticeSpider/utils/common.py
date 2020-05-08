# -*- coding: utf-8 -*-
import time

import requests
import hashlib


def get_md5(url):
    """
    :param url: url
    :return: md5加密串
    """
    if isinstance(url, str):
        url = url.encode()
    return hashlib.md5(url).hexdigest()


def x_token():
    """
    拉钩 X_HTTP_TOKEN计算
    :return: str
    """
    t = "f544c02fe4e37448" + str(int(time.time())) + "daf3670c0e4f2219"
    return t[::-1]


def qingting_proxy():
    """
    :return: str 蜻蜓代理 api
    """
    proxyUser = ""
    proxyPass = ""
    proxyHost = ""
    proxyPort = ""
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    return proxyMeta
