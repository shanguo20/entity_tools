# coding=utf-8
import os

spawns_on_surface = """ "minecraft:spawns_on_surface": {}, """
spawns_underground = """ "minecraft:spawns_underground": {}, """
difficulty_filter = """
        "minecraft:difficulty_filter": {
          "min": "easy",
          "max": "hard"
        },"""
height_filter = """
        "minecraft:height_filter": {
          "min": 0,
          "max": %s
        },
        """
spawn_ruleJson = """
{
  "format_version": "1.8.0",
  "minecraft:spawn_rules": {
    "description": {
      "identifier": "mwh_aoa3:%s",
      "population_control": "%s"
    },
    "conditions": [
      {
        %s
        %s
        %s
        "minecraft:brightness_filter": {
          "min": %s,
          "max": %s,
          "adjust_for_weather": true
        },
        %s
        "minecraft:weight": {
          "default": 100
        },
        "minecraft:herd": {
          "min_size": 2,
          "max_size": 4
        },
        "minecraft:biome_filter": {
          "test": "has_biome_tag", "operator": "==", "value": "%s"
        }
      }
    ]
  }
}
"""


def spawn_rule(entityList):
    for entity in entityList:
        if entity["自然刷怪"]:
            biome = ""
            if entity["维度"] == "蠕变":
                biome = "dm312345527"

            elif entity["维度"] == "传说":
                biome = "dm542901447"

            elif entity["维度"] == "爵士":
                biome = "dm978585796"

            elif entity["维度"] == "深层":
                biome = "dm273941607"

            elif entity["维度"] == "赫尔维蒂":
                biome = "dm238224186"

            elif entity["维度"] == "主世界":
                biome = "overworld"

            elif entity["维度"] == "下界":
                biome = "nether"

            elif entity["维度"] == "玩具":
                biome = "dm256508992"

            elif entity["维度"] == "黄金":
                biome = "dm260899882"

            elif entity["维度"] == "天堂":
                biome = "dm262997050"

            elif entity["维度"] == "深渊":
                biome = "dm275580023"

            elif entity["维度"] == "秘境":
                biome = "dm260637745"

            elif entity["维度"] == "花园":
                biome = "dm259916881"

            elif entity["维度"] == "未知":
                biome = "dm263586904"

            elif entity["维度"] == "晶体":
                biome = "dm267912298"

            elif entity["维度"] == "糖果":
                biome = "dm265356369"

            elif entity["维度"] == "远古":
                biome = "dm266000000"

            elif entity["维度"] == "月球":
                biome = "dm266000001"


            elif entity["维度"] == "暴风":
                biome = "dm266000002"


            elif entity["维度"] == "不朽之地":
                biome = "dm266000003"


            elif entity["维度"] == "格瑞克":
                biome = "dm266000004"


            elif entity["维度"] == "符境":
                biome = "dm266000005"

            elif entity["维度"] == "异位":
                biome = "dm266000006"
            elif entity["维度"] == "赛尔瑞":
                biome = "dm266000007"

            entityJson = spawn_ruleJson % (
                entity["id"][0],
                "monster" if entity["是否是敌对"] else "animal",
                "" if "地表生成" in entity and entity["地表生成"] is False else spawns_on_surface,
                "" if "地底生成" in entity and entity["地底生成"] is False else spawns_underground,
                height_filter % entity["高度限制"] if "高度限制" in entity is False else "",
                0,
                16,
                difficulty_filter if entity["是否是敌对"] else "",
                biome
            )
            if not os.path.exists("spawn_rules"):
                os.makedirs("spawn_rules")
            with open("spawn_rules/" + entity["id"][0] + ".json", "w") as f:
                f.write(entityJson)
