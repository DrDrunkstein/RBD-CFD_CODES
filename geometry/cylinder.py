import bpy
import bmesh


class CylinderFactory:

    def __init__(self):

        self.scene = bpy.context.scene

        self.scene.unit_settings.system = 'METRIC'
        self.scene.unit_settings.scale_length = 1.0

    def create_open_top_cylinder(
        self,
        radius_mm,
        height_mm,
        location=(0, 0, 0),
        name="Cylinder_open_top"
    ):

        radius = radius_mm / 1000.0
        height = height_mm / 1000.0

        cx, cy, base_z = location

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=64,
            radius=radius,
            depth=height,
            end_fill_type='NGON',
            location=(cx, cy, base_z + height / 2.0)
        )

        obj = bpy.context.active_object
        obj.name = name

        # =======================
        # REMOVE ONLY TOP FACE
        # =======================

        me = obj.data

        bm = bmesh.new()
        bm.from_mesh(me)

        top_face = None
        max_z = -999999

        for face in bm.faces:

            face_center_z = face.calc_center_median().z

            if face_center_z > max_z:

                max_z = face_center_z
                top_face = face

        if top_face:

            bm.faces.remove(top_face)

        bm.to_mesh(me)

        me.update()

        bm.free()

        bpy.context.view_layer.update()

        return obj, radius, height