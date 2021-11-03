# coding=utf-8
import json


def damage_immunity(entityList):
    damage_immunityList = {}
    text = "damage_immunity = %s"
    for entity in entityList:
        if "伤害免疫" in entity:
            damage_immunityList["mwh_aoa3:" + entity["id"][0]] = entity["伤害免疫"]
        else:
            damage_immunityList["mwh_aoa3:" + entity["id"][0]] = {"近战": False, "弓": False, "枪": False, "爆炸": False,
                                                                  "火焰": False,
                                                                  "魔法": False}

    with open("damage_immunitys.py", "w") as f:
        f.write(text % json.dumps(damage_immunityList, encoding='utf-8', ensure_ascii=False).replace("true",
                                                                                                     "True").replace(
            "false", "False"))
