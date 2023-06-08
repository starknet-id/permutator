# import bpy
import json

traits = ["head", "fur", "makeup", "makeup_c", "body", "ears", "back"]
trait_amounts = {
    "head": 9,
    "fur": 18,
    "makeup": 6,
    "makeup_c": 7,
    "body": 8,
    "ears": 13,
    "back": 9,
}
path = "C:\\Current projects\\stark net id\\generations\\V3\\img\\"

# Load the JSON data from file.
with open("combinations.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Iterate over each object in the JSON data.
for counter, item in enumerate(data, 1):
    item_id = 0
    acc = 1
    # Set the attributes of the Blender object according to the JSON object.
    for i, trait in enumerate(traits):
        # bpy.context.object[f"{i+1}_{trait}"] = item[trait]+1
        item_id = item_id + acc * item[trait]
        acc *= trait_amounts[trait]

    print(item_id)

    # Render the scene to a file.
    bpy.context.scene.render.filepath = f"{path}{item_id}.png"
    bpy.ops.render.render(write_still=True)
    bpy.data.scenes["Scene"]
