import bpy
import sys
import os
import importlib

# =======================
# PROJECT PATH
# =======================

project_dir = os.path.dirname(
    bpy.context.space_data.text.filepath
)

if project_dir not in sys.path:
    sys.path.append(project_dir)

# =======================
# IMPORT MODULES
# =======================

import config

import utils.scene
import geometry.cylinder
import physics.rigidbody
import particles.emitter
import export.export_csv

# =======================
# RELOAD MODULES
# =======================

importlib.reload(config)

importlib.reload(utils.scene)
importlib.reload(geometry.cylinder)
importlib.reload(physics.rigidbody)
importlib.reload(particles.emitter)
importlib.reload(export.export_csv)

# =======================
# IMPORT CLASSES/FUNCTIONS
# =======================

from utils.scene import clear_scene

from geometry.cylinder import CylinderFactory

from physics.rigidbody import (
    setup_rigidbody,
    setup_rigidbody_world
)

from particles.emitter import SphereEmitter

from export.export_csv import export_sphere_centers



import config

from utils.scene import clear_scene
from geometry.cylinder import CylinderFactory
from physics.rigidbody import (
    setup_rigidbody,
    setup_rigidbody_world
)
from particles.emitter import SphereEmitter
from export.export_csv import export_sphere_centers


# =======================
# INITIAL SETUP
# =======================

# Clear scene
clear_scene()

# Clear rigid body cache
if bpy.context.scene.rigidbody_world:

    bpy.ops.ptcache.free_bake_all()

factory = CylinderFactory()

# =======================
# CREATE CYLINDER
# =======================

(
    cylinder_obj,
    cylinder_radius_m,
    cylinder_height_m

) = factory.create_open_top_cylinder(

    radius_mm=config.CYLINDER_RADIUS_MM,
    height_mm=config.CYLINDER_HEIGHT_MM
)

# =======================
# CYLINDER PHYSICS
# =======================

# Apply transforms BEFORE rigid body
bpy.context.view_layer.objects.active = cylinder_obj

cylinder_obj.select_set(True)

bpy.ops.object.transform_apply(
    location=False,
    rotation=False,
    scale=True
)

# Apply passive rigid body
setup_rigidbody(
    cylinder_obj,
    type='PASSIVE',
    mass=0.0,
    friction=config.WALL_FRICTION,
    restitution=config.WALL_RESTITUTION,
    shape='CONVEX_HULL'
)

bpy.context.view_layer.update()

# =======================
# WORLD SETUP
# =======================

scene = bpy.context.scene
scene.frame_set(scene.frame_current)

setup_rigidbody_world(scene, config)

# Reset timeline to initial frame
scene.frame_set(scene.frame_start)

# =======================
# PARTICLE EMITTER
# =======================

emitter = SphereEmitter(
    config,
    cylinder_radius_m,
    cylinder_height_m
)

emitter.register_handler()
print("Registering emitter...")
#bpy.ops.screen.animation_play()
scene.frame_set(config.FRAME_START)

print("Simulation started.")
