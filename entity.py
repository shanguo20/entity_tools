# coding=utf-8
import os

entityJson = """
{
  "format_version": "1.8.0",
  "minecraft:client_entity": {
    "description": {
      "identifier": "mwh_aoa3:%s",
      "textures": {
        "default": "textures/entity/nether/%s"
      },
      "geometry": {
        "default": "geometry.%s"
      },
      "spawn_egg": {
        "base_color": "%s",
        "overlay_color": "%s"
      },
      "materials": {
        "default": "entity_alphatest"
      },
      "animations": {
        "look_at_target_default": "animation.humanoid.look_at_target.default",
        "look_at_target_gliding": "animation.humanoid.look_at_target.gliding",
        "look_at_target_swimming": "animation.humanoid.look_at_target.swimming",
        "move": "animation.%s.move"
      },
      "animation_controllers": [
        { 
            "move": "controller.animation.%s.move"
        },
        
        {
            "look_at_target": "controller.animation.humanoid.look_at_target"
        }
      ],
      "render_controllers": [
        "controller.render.%s"
      ]
    }
  }
}
"""

magicEntityJson = """
{
  "format_version": "1.10.0",
  "minecraft:client_entity": {
    "description": {
      "identifier": "mwh_aoa3:%s_magic",
      "materials": {
        "default": "entity_alphatest"
      },
      "textures": {
        "default": "textures/entity/holly_arrow"
      },
      "geometry": {
        "default": "geometry.magic"
      },
      "animations": {
        "move": "animation.holly_arrow.move"
      },
      "scripts": {
        "pre_animation": [
          "variable.shake = query.shake_time - query.frame_alpha;",
          "variable.shake_power = variable.shake > 0.0 ? -Math.sin(variable.shake * 200.0) * variable.shake : 0.0;"
        ],
        "animate": [
          "move"
        ]
      },
      "render_controllers": [ "controller.render.holly_arrow" ]
    }
  }
}
"""


def entity(entityList):
    for entity in entityList:
        if not os.path.exists("entity"):
            os.makedirs("entity")
        with open("entity/" + entity["id"][0] + ".entity.json", "w") as f:
            f.write(entityJson % (
                entity["id"][0],
                entity["id"][0],
                entity["id"][0],
                entity["刷怪蛋颜色"][0],
                entity["刷怪蛋颜色"][1],
                entity["id"][0],
                entity["id"][0],
                entity["id"][0]
            ))

        if entity["远程攻击"]:
            with open("entity/" + entity["id"][0] + "_magic.json", "w") as f:
                f.write(magicEntityJson % (entity["id"][0]))
