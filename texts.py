# coding=utf-8
import os

textsItem = """
item.spawn_egg.entity.mwh_aoa3:%s.name=生成 %s
entity.mwh_aoa3:%s.name=%s
"""


def texts(entityList):
    texts = ""
    for entity in entityList:
        texts += textsItem % (entity["id"][0], entity["中文名"],entity["id"][0], entity["中文名"])

    if not os.path.exists("texts"):
        os.makedirs("texts")
    with open("texts/" + "zh_CN.lang", "w") as f:
        f.write(texts)
