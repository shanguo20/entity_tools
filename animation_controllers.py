import os

animation_controllersJson = """
{
  "format_version": "1.10.0",
  "animation_controllers": {
    "controller.animation.%s.move": {
      "initial_state": "default",
      "states": {
        "default": {
          "animations": [
            {
              "move": "query.modified_move_speed || query.ground_speed>0"
            }
          ]
        }
      }
    }
  }
}
"""


def animation_controllers(entityList):
    for entity in entityList:

        if not os.path.exists("animation_controllers"):
            os.makedirs("animation_controllers")
        with open("animation_controllers/" + entity["id"][0] + ".animation_controllers.json", "w") as f:
            f.write(animation_controllersJson % entity["id"])
