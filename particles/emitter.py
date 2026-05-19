import bpy
import random

from bpy.app.handlers import persistent

from physics.rigidbody import setup_rigidbody


class SphereEmitter:

    def __init__(
        self,
        config,
        cylinder_radius_m,
        cylinder_height_m
    ):

        self.config = config

        self.cylinder_radius_m = cylinder_radius_m
        self.cylinder_height_m = cylinder_height_m

        self.spawned_spheres = 0

        # Deterministic random seed
        random.seed(42)

        # Sequential temporal emission
        self.next_spawn_frame = (
            self.config.FRAME_START
        )

    # =======================
    # CREATE ONE PARTICLE
    # =======================
    print("Handler running...")
    def emit_sphere(self, scene):

        current_frame = scene.frame_current

        # Stop if maximum number reached
        if self.spawned_spheres >= self.config.NUM_SPHERES:
            return

        # Wait until next scheduled emission
        if current_frame < self.next_spawn_frame:
            return

        sphere_radius_m = (
            self.config.SPHERE_DIAMETER_MM / 2.0
        ) / 1000.0

        # Random horizontal distribution
        x = random.uniform(
            -self.cylinder_radius_m * 0.4,
             self.cylinder_radius_m * 0.4
        )

        y = random.uniform(
            -self.cylinder_radius_m * 0.7,
             self.cylinder_radius_m * 0.7
        )

        # Spawn height above bed
        z = self.cylinder_height_m + 0.01

        bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64,
        ring_count=32,
        radius=sphere_radius_m,
        location=(x, y, z)
        )

        sphere = bpy.context.active_object

        sphere.name = (
            f"Sphere_{self.spawned_spheres:03d}"
        )

        # Apply rigid body physics
        setup_rigidbody(
            sphere,
            type='ACTIVE',
            mass=self.config.SPHERE_MASS_KG,
            friction=self.config.SPHERE_FRICTION,
            restitution=self.config.SPHERE_RESTITUTION,
            shape='SPHERE',
            linear_damping=self.config.SPHERE_LINEAR_DAMPING,
            angular_damping=self.config.SPHERE_ANGULAR_DAMPING
        )

        print(
            f"Frame {current_frame}: "
            f"created {sphere.name}"
        )

        self.spawned_spheres += 1

        # Schedule next emission
        self.next_spawn_frame += (
            self.config.SPAWN_INTERVAL
        )

    # =======================
    # STOP SIMULATION
    # =======================

    def stop_simulation(self, scene):

        if scene.frame_current >= scene.frame_end:

            bpy.ops.screen.animation_cancel(
                restore_frame=False
            )

            print("Simulation finished.")

    # =======================
    # REGISTER HANDLERS
    # =======================

    def register_handler(self):

        @persistent
        def emission_handler(scene):

            self.emit_sphere(scene)

        @persistent
        def stop_handler(scene):

            self.stop_simulation(scene)

        bpy.app.handlers.frame_change_pre.clear()

        bpy.app.handlers.frame_change_pre.append(
            emission_handler
        )

        bpy.app.handlers.frame_change_pre.append(
            stop_handler
        )

        print("Emitter handler registered.")