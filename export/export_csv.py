import bpy
import csv
import os


# =======================
# EXPORT FUNCTION
# =======================

def export_sphere_centers(filepath):

    depsgraph = (
        bpy.context.evaluated_depsgraph_get()
    )

    with open(filepath, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "x",
            "y",
            "z"
        ])

        for obj in bpy.data.objects:

            if obj.name.startswith("Sphere"):

                eval_obj = obj.evaluated_get(
                    depsgraph
                )

                loc = (
                    eval_obj.matrix_world.translation
                )

                writer.writerow([
                    loc.x,
                    loc.y,
                    loc.z
                ])

    print()
    print(f"CSV exported: {filepath}")
    print()


# =======================
# RUN EXPORT
# =======================

blend_dir = os.path.dirname(
    bpy.data.filepath
)

csv_path = os.path.join(
    blend_dir,
    "sphere_centers.csv"
)

export_sphere_centers(csv_path)