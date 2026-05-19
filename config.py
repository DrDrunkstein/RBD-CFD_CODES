# =======================
# GEOMETRY
# =======================

CYLINDER_RADIUS_MM = 6.0
CYLINDER_HEIGHT_MM = 120.0

# =======================
# PARTICLES
# =======================

SPHERE_DIAMETER_MM = 3.0
NUM_SPHERES = 50

# =======================
# PARTICLE PHYSICS
# =======================

SPHERE_MASS_KG = 0.01
SPHERE_FRICTION = 0.5
SPHERE_RESTITUTION = 0.4
SPHERE_LINEAR_DAMPING = 0.0002
SPHERE_ANGULAR_DAMPING = 0.0005

# =======================
# WALL PHYSICS
# =======================

WALL_FRICTION = 0.5
WALL_RESTITUTION = 0.2

# =======================
# WORLD PHYSICS
# =======================

SIMULATION_SOLVER_ITERATIONS = 150
SIMULATION_TIME_SCALE = 0.1
GRAVITY = (0.0, 0.0, -9.81)

# Blender 4.x
SIMULATION_SUBSTEPS = 50

# =======================
# TEMPORAL FILLING
# =======================

SPAWN_INTERVAL = 7

# =======================
# TIMELINE
# =======================

FRAME_START = 1
STABILIZATION_FRAMES = 300

FRAME_END = (
    FRAME_START
    + NUM_SPHERES * SPAWN_INTERVAL
    + STABILIZATION_FRAMES
)

# =======================
# EXPORT
# =======================

OUTPUT_CSV = "sphere_centers.csv"