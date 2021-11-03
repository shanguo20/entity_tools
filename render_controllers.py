import os

render_controllersJson = """
{
  "format_version": "1.8.0",
  "render_controllers": {
    "controller.render.%s": {
      "geometry": "Geometry.default",
      "materials": [ { "*": "Material.default" } ],
      "textures": [ "Texture.default" ]
    }
  }
}
"""


def render_controllers(entityList):
    for entity in entityList:

        if not os.path.exists("render_controllers"):
            os.makedirs("render_controllers")
        with open("render_controllers/" + entity["id"][0] + ".render_controllers.json", "w") as f:
            f.write(render_controllersJson % entity["id"])
