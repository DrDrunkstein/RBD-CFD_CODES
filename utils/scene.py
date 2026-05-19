import bpy


def clear_scene():

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    for block_collection in [
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.textures,
        bpy.data.images
    ]:

        for block in block_collection:
            block_collection.remove(block)