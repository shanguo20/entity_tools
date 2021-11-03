# coding=utf-8
def hunting_level(entityList):
    text = "hunting_datas = %s"
    hunting_level = {}
    for entity in entityList:
        if "狩猎等级" in entity and entity["狩猎等级"] != 0:
            hunting_level["mwh_aoa3:" + entity["id"][0]] = {"hunting_experience_reward": entity["狩猎经验"],
                                                            "hunting_level": entity["狩猎等级"], "high": entity["碰撞箱大小"][1]}

    with open("hunting_datas.py", "w") as f:
        f.write(text % hunting_level)
