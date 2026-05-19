import bpy


def setup_rigidbody(
    obj,
    type='ACTIVE',
    mass=1.0,
    friction=0.5,
    restitution=0.2,
    shape='MESH',
    linear_damping=0,
    angular_damping=0
):

    bpy.context.view_layer.objects.active = obj

    bpy.ops.rigidbody.object_add()

    rb = obj.rigid_body

    rb.type = type
    rb.mass = mass
    rb.friction = friction
    rb.restitution = restitution
    rb.collision_shape = shape
    rb.linear_damping = linear_damping
    rb.angular_damping = angular_damping
    rb.use_deactivation = False
    #rb.use_margin = True
    #rb.collision_margin = 0.00001


def setup_rigidbody_world(scene, config):

    if not scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()

    rb_world = scene.rigidbody_world

    rb_world.time_scale = config.SIMULATION_TIME_SCALE
    rb_world.substeps_per_frame = config.SIMULATION_SUBSTEPS
    rb_world.solver_iterations = (
        config.SIMULATION_SOLVER_ITERATIONS
    )

    scene.gravity = config.GRAVITY

    scene.frame_start = config.FRAME_START
    scene.frame_end = config.FRAME_END

    rb_world.point_cache.frame_start = config.FRAME_START
    rb_world.point_cache.frame_end = config.FRAME_END