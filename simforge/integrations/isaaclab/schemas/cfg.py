from collections.abc import Callable

from isaaclab.utils.configclass import configclass

from simforge.integrations.isaaclab.schemas.impl import set_mesh_collision_properties


@configclass
class MeshCollisionPropertiesCfg:
    func: Callable = set_mesh_collision_properties

    mesh_approximation: str | None = None
    """Collision approximation to use for the collision shape.

    Supported values: "none", "convexHull", "convexDecomposition",
    "meshSimplification", "boundingCube", "boundingSphere", "sdf".
    """

    sdf_resolution: int = 128
    """Resolution of the SDF grid used for collision approximation."""
