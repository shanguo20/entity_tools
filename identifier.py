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
        if entity["??????????????????"]:
            flyList.append("mwh_aoa3:" + entity["id"][0])
            entityJson = flyJson % (
                entity["id"][0],
                monster if entity["???????????????"] else "",
                entity["???????????????"][0], entity["???????????????"][1],
                entity["??????"],
                entity["??????"],
                entity["id"][0],
                entity["????????????"],
                entity["?????????"],
                range if entity["????????????"] else melee,
                attackPlayer if entity["???????????????"] else "",
                knockback_resistance if "????????????" in entity["????????????"] and entity["????????????"]["????????????"] else "",
                fire_immune if "??????" in entity["????????????"] and entity["????????????"]["??????"] else "",
                entity["??????"]
            )
        else:
            if "???????????????" in entity and entity["???????????????"]:
                entityJson = petJson % (
                    entity["id"][0],
                    entity["???????????????"][0], entity["???????????????"][1],
                    entity["??????"],
                    entity["??????"],
                    entity["????????????"],
                    entity["?????????"]
                )
            elif "??????" in entity and entity["??????"]:
                entityJson = creepJson % (
                    entity["id"][0],
                    entity["?????????"],
                    entity["?????????"],
                    monster if entity["???????????????"] else "",
                    entity["???????????????"][0], entity["???????????????"][1],
                    entity["????????????"],
                    entity["id"][0],
                    entity["??????"],
                    entity["??????"],
                    entity["?????????"],
                    attackPlayer if entity["???????????????"] else "",
                    (knockback_resistance if "????????????" in entity["????????????"] and entity["????????????"]["????????????"] else "") if "????????????" in entity else "",

                    (fire_immune if "??????" in entity["????????????"] and entity["????????????"]["??????"] else "") if "????????????" in entity else "",
                    entity["??????"]
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
        if entity["????????????"]:
            with open("entities/" + entity["id"][0] + "_magic.json", "w") as f:
                f.write(magicEntitiesJson % (entity["id"][0],
                                             entity["?????????"],
                                             entity["?????????"]))

        if "?????????" in entity and entity["?????????"] != []:
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
            for index, loot in enumerate(entity["?????????"]):
                if index == 0:
                    lootText += lootItem % (
                        float(loot["??????"]) / 100,
                        loot["id"],
                        loot["?????????"],
                        loot["??????"],
                        loot["??????"]
                    )
                else:
                    lootText += "," + lootItem % (
                        float(loot["??????"]) / 100,
                        loot["id"],
                        loot["?????????"],
                        loot["??????"],
                        loot["??????"]
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
#         "?????????": "??????1",
#         "???????????????": [???, ???],
#         "??????": 10,
#         "????????????": 0.35,  # ?????????0.35????????????????????????
#         "???????????????": True,  # True ?????? False??????????????????True????????????????????????
#         "?????????": xxx,
#         "??????????????????": False,  # True????????????False????????????
#         "?????????": [  # id???????????????id,????????????????????? "?????????":[]
#             {
#                 "id": "mwh_aoa3:block_creep_grass",
#                 "?????????": 0,
#                 "??????": 1,
#                 "??????": 3,
#                 "??????": 0
#             },
#             {
#                 "id2": "minecraft:dirt",
#                 "?????????": 0,
#
#                 "??????": 3,
#                 "??????": 0
#             }
#         ],
#         "??????": 10,
#         "????????????": True,
#         "??????": True,  # True???????????? False?????????
#         "???????????????": ["#ffffff", "#000000"],  # ??????????????????????????????????????????????????????????????????
#         "????????????": False,
#         "????????????": {"??????": False, "???": True, "???": False, "??????": False, "??????": False, "??????": False},
#
#         "????????????": 0,
#         "??????": "??????",  # ?????? ?????? ????????? ?????? ?????? ??????
#         "????????????": True  # True???????????????????????????False?????????????????????????????????????????????
#     },
# ????????????
# ]
