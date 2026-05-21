import bpy
import math
import csv
import os
import config


# =======================
# USER PARAMETERS
# =======================

Z_MIN = 0.0

Z_MAX_VALUES = [
    0.01,
    0.02,
    0.03,
    0.04,
    0.05,
    0.06,
    0.07,
    0.08,
    0.09,
    0.10
]


# =======================
# GEOMETRY
# =======================

cylinder_radius = (
    config.CYLINDER_RADIUS_MM / 1000.0
)

sphere_radius = (
    config.SPHERE_DIAMETER_MM / 2.0
) / 1000.0


# =======================
# SPHERE VOLUME
# =======================

sphere_volume = (
    (4.0 / 3.0)
    * math.pi
    * sphere_radius**3
)


# =======================
# OUTPUT FILE
# =======================

blend_dir = os.path.dirname(
    bpy.data.filepath
)

csv_path = os.path.join(
    blend_dir,
    "global_voidage.csv"
)


# =======================
# WRITE CSV
# =======================

with open(csv_path, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "Z_MIN",
        "Z_MAX",
        "sample_height",
        "sphere_count",
        "sample_volume",
        "solid_volume",
        "voidage"
    ])

    # =======================
    # LOOP OVER Z_MAX
    # =======================

    for Z_MAX in Z_MAX_VALUES:

        sample_height = (
            Z_MAX - Z_MIN
        )

        sample_volume = (
            math.pi
            * cylinder_radius**2
            * sample_height
        )

        sphere_count = 0

        for obj in bpy.data.objects:

            if obj.name.startswith("Sphere"):

                z = obj.location.z

                if Z_MIN <= z <= Z_MAX:

                    sphere_count += 1

        solid_volume = (
            sphere_count
            * sphere_volume
        )

        voidage = (
            1.0
            - solid_volume / sample_volume
        )

        writer.writerow([
            Z_MIN,
            Z_MAX,
            sample_height,
            sphere_count,
            sample_volume,
            solid_volume,
            voidage
        ])

        print(
            f"Z_MAX = {Z_MAX:.3f} | "
            f"Voidage = {voidage:.5f}"
        )

print()
print(f"Voidage CSV exported:")
print(csv_path)
print()