# coding=utf-8
import os

from animation_controllers import animation_controllers
from animations import animations
from damage_immunity import damage_immunity
from entity import entity
from entityList import entityList
from hunting_level import hunting_level
from render_controllers import render_controllers
from spawn_rule import spawn_rule
from texts import texts

flyList = []

sJson = """
{
  "entity_sounds": {
    "entities": {
        %s
    }
  }
}
"""
sitem = """
      "mwh_aoa3:%s": {
        "volume": 1.0,
        "pitch": [
          0.8,
          1.2
        ],
        "events": {
          "ambient": "mob.%s.idle",
          "angry": "mob.%s.angry",
          "attack": "mob.%s.attack",
          "hurt": "mob.%s.hurt",
          "death": "mob.%s.death",
          "step": {
            "sound": "mob.%s.step",
            "volume": 1.0,
            "pitch": 1.0
          }
        }
      },"""

magicEntitiesJson = """
{
  "format_version": "1.13.0",
  "minecraft:entity": {
    "description": {
      "identifier": "mwh_aoa3:%s_magic",
      "is_spawnable": false,
      "is_summonable": false,
      "is_experimental": false
    },
    "components": {
      "netease:custom_entity_type": {
        "value": "projectile_entity"
      },
      "minecraft:collision_box": {
        "width": 0.25,
        "height": 0.25
      },
      "minecraft:projectile": {
        "on_hit": {
          "impact_damage": {
            "damage": [
              %s,
              %s
            ],
            "knockback": true,
            "semi_random_diff_damage": false,
            "destroy_on_hit": true
          },
          "stick_in_ground": {
            "shake_time": 0.35
          },
          "arrow_effect": {
          }
        },
        "power": 1,
        "gravity": 0.05,
        "uncertainty_base": 16,
        "uncertainty_multiplier": 4,
        "anchor": 1,
        "should_bounce": true,
        "offset": [
          0,
          -0.1,
          0
        ]
      },
      "minecraft:physics": {
      },
      "minecraft:pushable": {
        "is_pushable": false,
        "is_pushable_by_piston": true
      }
    }
  }
}"""
monster = """ "monster", """
knockback_resistance = """
        "minecraft:knockback_resistance": {
            "value": 1.0
        },
"""
fire_immune = """"minecraft:fire_immune": true,"""
attackPlayer = """
        "minecraft:behavior.nearest_attackable_target": {
          "priority": 1,
          "entity_types": [
            {
              "filters": {
                "test": "is_family",
                "subject": "other",
                "value": "player"
              },
              "max_dist": 16
            }
          ],
          "must_see": true,
          "must_see_forget_duration": 30
        },
"""
range = """
      "minecraft:behavior.ranged_attack": {
        "priority": 2,
        "speed_multiplier": 1.0,
        "attack_interval_min": 1,
        "attack_interval_max": 1,
        "attack_radius": 10.0
      },
      "minecraft:shooter": {
        "type": "Arrow",
        "def": "mwh_aoa3:%s_magic"
      },
"""
melee = """
      "minecraft:behavior.melee_attack": {
        "priority": 5,
        "target_dist": 1.2,
        "track_target": true,
        "reach_multiplier": 1
      },
"""
creepJson = """
{
  "format_version": "1.13.0",
  "minecraft:entity": {
    "description": {
      "identifier": "mwh_aoa3:%s",
      "is_spawnable": true,
      "is_summonable": true,
      "is_experimental": false
    },
   "component_groups": {
      "minecraft:exploding": {
        "minecraft:explode": {
          "fuse_length": 1.5,
          "fuse_lit": true,
          "power": %s,
          "causes_fire": false,
          "destroy_affected_by_griefing": true
        }
      },
      "minecraft:forced_exploding": {
        "minecraft:target_nearby_sensor": {
        },
        "minecraft:explode": {
          "fuse_length": 1.5,
          "fuse_lit": true,
          "power": %s,
          "causes_fire": false,
          "destroy_affected_by_griefing": true
        },
        "minecraft:on_target_escape": {
        }
      }
    },

    "components": {
      "minecraft:type_family": {
        "family": [ "creeper", %s "mob" ]
      },
      "minecraft:breathable": {
        "total_supply": 15,
        "suffocate_time": 0
      },
      "minecraft:nameable": {
      },
      "minecraft:collision_box": {
        "width": %s,
        "height": %s
      },
      "minecraft:movement": {
        "value": %s
      },
      "minecraft:navigation.walk": {
      "can_path_over_water": true
      },
      "minecraft:movement.basic": {

      },
      "minecraft:jump.static": {
      },
      "minecraft:can_climb": {
      },
      "minecraft:loot": {
        "table": "loot_tables/entity/%s.json"
      },
      "minecraft:health": {
        "value": %s,
        "max": %s
      },
      "minecraft:hurt_on_condition": {
        "damage_conditions": [
          {
            "filters": { "test": "in_lava", "subject": "self", "operator": "==", "value": true },
            "cause": "lava",
            "damage_per_tick": 4
          }
        ]
      },
      "minecraft:attack": {
        "damage": %s
      },
      
      "minecraft:target_nearby_sensor": {
        "inside_range": 2.5,
        "outside_range": 6.0,
        "must_see": true,
        "on_inside_range": {
          "event": "minecraft:start_exploding",
          "target": "self"
        },
        "on_outside_range": {
          "event": "minecraft:stop_exploding",
          "target": "self"
        },
        "on_vision_lost_inside_range": {
            "event": "minecraft:stop_exploding",
            "target": "self"
        }
      },
      "minecraft:interact": {
        "interactions": {
          "on_interact": {
            "filters": {
              "all_of": [
                { "test": "is_family", "subject": "other", "value": "player" },
                { "test": "has_equipment", "domain": "hand", "subject": "other", "value": "flint_and_steel" },
                { "test": "has_component", "operator": "!=", "value": "minecraft:explode" }
              ]
            },
          "event": "minecraft:start_exploding_forced",
          "target": "self"
          },
          "hurt_item": 1,
          "swing": true,
          "play_sounds": "ignite",
          "interact_text": "action.interact.creeper"
        }
      },
      "minecraft:despawn": {
        "despawn_from_distance": {}
      },
      "minecraft:behavior.float": {
        "priority": 0
      },
      "minecraft:behavior.melee_attack": {
        "priority": 3,
        "speed_multiplier": 1.25,
        "track_target": false,
        "reach_multiplier":  0.0
      },
      "minecraft:behavior.random_stroll": {
        "priority": 5,
        "speed_multiplier": 1
      },
      "minecraft:behavior.look_at_player": {
        "priority": 6,
        "look_distance": 8
      },
      "minecraft:behavior.random_look_around": {
        "priority": 6
      },
      %s
      %s
      %s
      
      "minecraft:behavior.hurt_by_target": {
        "priority": 2
      },
      "minecraft:physics": {
      },
      "minecraft:pushable": {
        "is_pushable": true,
        "is_pushable_by_piston": true
      },
      "minecraft:on_target_escape": {
        "event": "minecraft:stop_exploding",
        "target": "self"
      },
      "minecraft:experience_reward": {
        "on_death": "query.last_hit_by_player ? %s : 0"
      }
    },

    "events": {
      "minecraft:start_exploding_forced": {
        "sequence": [
          {
            "filters": {
              "test": "has_component",
              "operator": "!=",
              "value": "minecraft:is_charged"
            },
            "add": {
              "component_groups": [
                "minecraft:forced_exploding"
              ]
            }
          }
        ]
      },
      "minecraft:start_exploding": {
        "sequence": [
          {
            "filters": {
              "test": "has_component",
              "operator": "!=",
              "value": "minecraft:is_charged"
            },
            "add": {
              "component_groups": [
                "minecraft:exploding"
              ]
            }
          }
        ]
      },
      "minecraft:stop_exploding": {
        "remove": {
          "component_groups": [
            "minecraft:exploding"
          ]
        }
      }
    }
  }
}
"""
flyJson = """
{
  "format_version": "1.13.0",
  "minecraft:entity": {
    "description": {
      "identifier": "mwh_aoa3:%s",
      "is_spawnable": true,
      "is_summonable": true,
      "is_experimental": false
    },
    "components": {
	"minecraft:type_family": {
        "family": [  %s "mob" ]
      },
      "minecraft:nameable": {},
      "minecraft:leashable": {
        "soft_distance": 8.0,
        "hard_distance": 12.0,
        "max_distance": 20.0,
        "on_leash": {
          "event": "minecraft:on_leash",
          "target": "self"
        },
        "on_unleash": {
          "event": "minecraft:on_unleash",
          "target": "self"
        }
      },
      "minecraft:breathable": {
        "total_supply": 15,
        "suffocate_time": 0
      },
      "minecraft:collision_box": {
        "width": %s,
        "height": %s
      },
      "minecraft:health": {
        "value": %s,
        "max": %s
      },
      "minecraft:loot": {
        "table": "loot_tables/entity/%s.json"
      },
      "minecraft:hurt_on_condition": {
        "damage_conditions": [
          {
            "filters": {
              "test": "in_lava",
              "subject": "self",
              "operator": "==",
              "value": true
            },
            "cause": "lava",
            "damage_per_tick": 4
          }
        ]
      },
      "minecraft:movement": {
        "value": %s
      },
      "minecraft:attack": {
        "damage": %s
      },
      "minecraft:behavior.float": {
        "priority": 0
      },
      "minecraft:behavior.mount_pathing": {
        "priority": 1,
        "speed_multiplier": 1.25,
        "target_dist": 0,
        "track_target": true
      },
      "minecraft:behavior.leap_at_target": {
        "priority": 4,
        "target_dist": 0.4
      },
      "minecraft:behavior.random_stroll": {
        "priority": 3,
        "speed_multiplier": 1
      },
      "minecraft:behavior.random_look_around": {
        "priority": 7
      },
      "minecraft:behavior.look_at_player": {
        "priority": 6,
        "target_distance": 6,
        "probability": 0.02
      },
      "minecraft:behavior.hurt_by_target": {
	    "alert_same_type":true,
        "priority": 3
      },
      
	  %s
	  %s
	  %s
	  %s
      "minecraft:can_fly": {
        "value": true
      },
	  
      "minecraft:physics": {
        "has_gravity": false
      },
      "minecraft:damage_sensor": {
        "triggers": {
          "cause": "fall",
          "deals_damage": false
        }
      },
    
      "minecraft:behavior.float": {
        "priority": 7
      },
      "minecraft:movement": {
        "value": 0.3
      },
      "minecraft:flying_speed": {
        "value": 0.3
      },
      "minecraft:navigation.hover": {
        "can_path_over_water": true,
        "can_sink": false,
        "can_pass_doors": false,
        "can_path_from_air": true,
        "avoid_water": true,
        "avoid_damage_blocks": true,
        "avoid_sun": false
      },
      "minecraft:movement.hover": {},
      "minecraft:jump.static": {},
      "minecraft:behavior.swoop_attack": {
        "priority": 2,
        "damage_reach": 0.2,
        "speed_multiplier": 1.0,
        "delay_range": [ 1.0, 2.0 ]
      },
      "minecraft:pushable": {
        "is_pushable": true,
        "is_pushable_by_piston": true
      },
      
      "minecraft:experience_reward": {
        "on_death": "query.last_hit_by_player ? %s : 0"
      }
    }
  }
}
"""
terrestrialJson = """
{
  "format_version": "1.13.0",
  "minecraft:entity": {
    "description": {
      "identifier": "mwh_aoa3:%s",
      "is_spawnable": true,
      "is_summonable": true,
      "is_experimental": false
    },
    "components": {
      "minecraft:type_family": {
        "family": [ %s "mob"]
      },
      "minecraft:nameable": {},
      "minecraft:leashable": {
        "soft_distance": 8.0,
        "hard_distance": 12.0,
        "max_distance": 20.0,
        "on_leash": {
          "event": "minecraft:on_leash",
          "target": "self"
        },
        "on_unleash": {
          "event": "minecraft:on_unleash",
          "target": "self"
        }
      },
      "minecraft:breathable": {
        "total_supply": 15,
        "suffocate_time": 0
      },
      "minecraft:collision_box": {
        "width": %s,
        "height": %s
      },
      "minecraft:health": {
        "value": %s,
        "max": %s
      },
      "minecraft:loot": {
        "table": "loot_tables/entity/%s.json"
      },
      "minecraft:hurt_on_condition": {
        "damage_conditions": [
          {
            "filters": {
              "test": "in_lava",
              "subject": "self",
              "operator": "==",
              "value": true
            },
            "cause": "lava",
            "damage_per_tick": 4
          }
        ]
      },
      "minecraft:movement": {
        "value": %s
      },
      "minecraft:navigation.walk": {
        "can_path_over_water": true,
        "avoid_damage_blocks": true
      },
      "minecraft:movement.basic": {},
      "minecraft:jump.static": {},
      "minecraft:can_climb": {},
      "minecraft:attack": {
        "damage": %s
      },
      "minecraft:behavior.float": {
        "priority": 0
      },
      "minecraft:behavior.mount_pathing": {
        "priority": 1,
        "speed_multiplier": 1.25,
        "target_dist": 0,
        "track_target": true
      },
      "minecraft:behavior.leap_at_target": {
        "priority": 4,
        "target_dist": 0.4
      },
      "minecraft:behavior.random_stroll": {
        "priority": 3,
        "speed_multiplier": 1
      },
      "minecraft:behavior.look_at_player": {
        "priority": 6,
        "target_distance": 6,
        "probability": 0.02
      },
      "minecraft:behavior.hurt_by_target": {
        "priority": 3
      },
      
      %s
      %s
      %s
      %s
      
      "minecraft:physics": {},
      "minecraft:pushable": {
        "is_pushable": true,
        "is_pushable_by_piston": true
      },
      "minecraft:experience_reward": {
        "on_death": "query.last_hit_by_player ? %s : 0"
      }
    }
  }
}
"""
petJson = """
{
  "format_version": "1.13.0",
  "minecraft:entity": {
    "description": {
      "identifier": "mwh_aoa3:%s",
      "is_spawnable": true,
      "is_summonable": true,
      "is_experimental": false
    },
    "component_groups": {
        "on_tame": {
            "minecraft:is_tamed": {
            },
            "minecraft:behavior.follow_owner": {
              "priority": 1,
              "speed_multiplier": 1.5,
              "start_distance": 24,
              "stop_distance": 6
            },
            "minecraft:behavior.owner_hurt_by_target": {
              "priority": 2
            },
            "minecraft:behavior.owner_hurt_target": {
              "priority": 2
            },
            "minecraft:behavior.nearest_attackable_target": {
              "priority": 3,
              "entity_types": [
                {
                  "filters": {
                    "test": "is_family",
                    "subject": "other",
                    "value": "monster"
                  },
                  "max_dist": 32
                }
              ],
              "must_see": true
            }
        }
    },
    "components": {
      "minecraft:type_family": {
        "family": [ "pet", "mob"]
      },
      "minecraft:nameable": {},
      
      "minecraft:leashable": {
        "soft_distance": 4.0,
        "hard_distance": 6.0,
        "max_distance": 10.0
      },
      "minecraft:breathable": {
        "total_supply": 15,
        "suffocate_time": 0
      },
      "minecraft:collision_box": {
        "width": %s,
        "height": %s
      },
      "minecraft:health": {
        "value": %s,
        "max": %s
      },
      "minecraft:hurt_on_condition": {
        "damage_conditions": [
          {
            "filters": {
              "test": "in_lava",
              "subject": "self",
              "operator": "==",
              "value": true
            },
            "cause": "lava",
            "damage_per_tick": 4
          }
        ]
      },
      "minecraft:movement": {
        "value": %s
      },
      "minecraft:navigation.walk": {
        "can_path_over_water": true,
        "avoid_damage_blocks": true
      },
      "minecraft:movement.basic": {},
      "minecraft:jump.static": {},
      "minecraft:can_climb": {},
      "minecraft:attack": {
        "damage": %s
      },
      "minecraft:behavior.float": {
        "priority": 0
      },
      "minecraft:behavior.mount_pathing": {
        "priority": 1,
        "speed_multiplier": 1.25,
        "target_dist": 0,
        "track_target": true
      },
      "minecraft:behavior.leap_at_target": {
        "priority": 4,
        "target_dist": 0.4
      },
      "minecraft:behavior.random_stroll": {
        "priority": 3,
        "speed_multiplier": 1
      },
      "minecraft:behavior.look_at_player": {
        "priority": 6,
        "target_distance": 6,
        "probability": 0.02
      },
      "minecraft:behavior.hurt_by_target": {
        "priority": 3
      },
      
      "minecraft:behavior.melee_attack": {
        "priority": 5,
        "target_dist": 1.2,
        "track_target": true,
        "reach_multiplier": 1
      },
      
      "minecraft:physics": {},
      "minecraft:pushable": {
        "is_pushable": true,
        "is_pushable_by_piston": true
      }
    },
    "events": {
        "on_tame":{
            "add": {
                "component_groups": [
                    "on_tame"
                ]
            }
        }
    }
  }
}
"""


def identifier(entityList):
    soundText = ''
    for entity in entityList:
        if " (Elite)" in entity["id"]:
            entity["id"] = "elite_" + str(entity["id"]).replace(" (Elite)", "")
        if " (Strong)" in entity["id"]:
            entity["id"] = "strong_" + str(entity["id"]).replace(" (Strong)", "")
        entity["id"] = str.lower(entity["id"].replace("-", "_").replace(" ", "_")),
        entityJson = None
        if entity["是否可以飞行"]:
            flyList.append("mwh_aoa3:" + entity["id"][0])
            entityJson = flyJson % (
                entity["id"][0],
                monster if entity["是否是敌对"] else "",
                entity["碰撞箱大小"][0], entity["碰撞箱大小"][1],
                entity["血量"],
                entity["血量"],
                entity["id"][0],
                entity["移动速度"],
                entity["攻击力"],
                range if entity["远程攻击"] else melee,
                attackPlayer if entity["是否是敌对"] else "",
                knockback_resistance if "免疫击退" in entity["伤害免疫"] and entity["伤害免疫"]["免疫击退"] else "",
                fire_immune if "火焰" in entity["伤害免疫"] and entity["伤害免疫"]["火焰"] else "",
                entity["经验"]
            )
        else:
            if "是否是宠物" in entity and entity["是否是宠物"]:
                entityJson = petJson % (
                    entity["id"][0],
                    entity["碰撞箱大小"][0], entity["碰撞箱大小"][1],
                    entity["血量"],
                    entity["血量"],
                    entity["移动速度"],
                    entity["攻击力"]
                )
            elif "自爆" in entity and entity["自爆"]:
                entityJson = creepJson % (
                    entity["id"][0],
                    entity["攻击力"],
                    entity["攻击力"],
                    monster if entity["是否是敌对"] else "",
                    entity["碰撞箱大小"][0], entity["碰撞箱大小"][1],
                    entity["移动速度"],
                    entity["id"][0],
                    entity["血量"],
                    entity["血量"],
                    entity["攻击力"],
                    attackPlayer if entity["是否是敌对"] else "",
                    (knockback_resistance if "免疫击退" in entity["伤害免疫"] and entity["伤害免疫"]["免疫击退"] else "") if "伤害免疫" in entity else "",

                    (fire_immune if "火焰" in entity["伤害免疫"] and entity["伤害免疫"]["火焰"] else "") if "伤害免疫" in entity else "",
                    entity["经验"]
                )

        soundText = soundText + sitem % (
            entity["id"][0],
            entity["id"][0],
            entity["id"][0],
            entity["id"][0],
            entity["id"][0],
            entity["id"][0],
            entity["id"][0]
        )

        if not os.path.exists("entities"):
            os.makedirs("entities")
        with open("entities/" + entity["id"][0] + ".json", "w") as f:
            f.write(entityJson)
        if entity["远程攻击"]:
            with open("entities/" + entity["id"][0] + "_magic.json", "w") as f:
                f.write(magicEntitiesJson % (entity["id"][0],
                                             entity["攻击力"],
                                             entity["攻击力"]))

        if "掉落物" in entity and entity["掉落物"] != []:
            lootText = ""
            lootItem = """
        {
            "conditions": [
                {
                    "condition": "killed_by_player"
                },
                {
                    "condition": "random_chance_with_looting",
                    "chance": %s,
                    "looting_multiplier": 0.05
                }
            ],
            "rolls": 1,
            "entries": [
                {
                    "type": "item",
                    "name": "%s",
                    "data": %s,
                    "weight": 1,
                    "functions": [
                        {
                            "function": "set_count",
                            "count": {
                                "min": %s,
                                "max": %s
                            }
                        },
                        {
                            "function": "looting_enchant",
                            "count": {
                                "min": 0,
                                "max": 1
                            }
                        }
                    ]
                }
            ]
        }"""
            lootJson = \
                """
                    {
                        "pools": [
                            %s
                        ]
                    }
                """
            for index, loot in enumerate(entity["掉落物"]):
                if index == 0:
                    lootText += lootItem % (
                        float(loot["概率"]) / 100,
                        loot["id"],
                        loot["特殊值"],
                        loot["最少"],
                        loot["最多"]
                    )
                else:
                    lootText += "," + lootItem % (
                        float(loot["概率"]) / 100,
                        loot["id"],
                        loot["特殊值"],
                        loot["最少"],
                        loot["最多"]
                    )
            if not os.path.exists("loot_tables/entity/"):
                os.makedirs("loot_tables/entity/")
            with open("loot_tables/entity/" + entity["id"][0] + ".json", "w") as f:
                f.write(lootJson % lootText)
        with open("flyList.py", "w") as f:
            f.write("flyList = %s" % flyList)
        with open("sounds.Json", "w") as f:
            f.write(sJson % soundText)


if __name__ == "__main__":
    identifier(entityList)
    hunting_level(entityList)
    entity(entityList)
    animations(entityList)
    animation_controllers(entityList)
    render_controllers(entityList)
    spawn_rule(entityList)
    texts(entityList)
    damage_immunity(entityList)
# [
#     {
#         "id": "xx",
#         "中文名": "生物1",
#         "碰撞箱大小": [宽, 高],
#         "血量": 10,
#         "移动速度": 0.35,  # 僵尸为0.35，以此为基础推测
#         "是否是敌对": True,  # True 为是 False为不是，设为True后生物会攻击玩家
#         "攻击力": xxx,
#         "是否可以飞行": False,  # True为可以，False为不可以
#         "掉落物": [  # id为掉落物品id,没有则不写或写 "掉落物":[]
#             {
#                 "id": "mwh_aoa3:block_creep_grass",
#                 "特殊值": 0,
#                 "概率": 1,
#                 "最多": 3,
#                 "最少": 0
#             },
#             {
#                 "id2": "minecraft:dirt",
#                 "特殊值": 0,
#
#                 "最多": 3,
#                 "最少": 0
#             }
#         ],
#         "经验": 10,
#         "免疫击退": True,
#         "自爆": True,  # True为会自爆 False为不会
#         "刷怪蛋颜色": ["#ffffff", "#000000"],  # 第一个颜色为蛋的底色，第二个为蛋上斑点的颜色
#         "远程攻击": False,
#         "伤害免疫": {"近战": False, "弓": True, "枪": False, "爆炸": False, "火焰": False, "魔法": False},
#
#         "狩猎等级": 0,
#         "维度": "蠕变",  # 蠕变 下界 主世界 爵士 深层 传说
#         "自然刷怪": True  # True为世界会自动刷怪，False为只会在刷怪笼或者其他方式刷怪
#     },
# 。。。。
# ]
