from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from isaaclab.sim import schemas
from isaaclab.sim.utils import get_current_stage
from pxr import UsdGeom, UsdPhysics

if TYPE_CHECKING:
    from simforge.integrations.isaaclab.schemas.cfg import MeshCollisionPropertiesCfg

logger = logging.getLogger(__name__)

# Mapping from user-facing approximation names to the corresponding
# ``MeshCollisionBaseCfg`` subclass in ``isaaclab.sim.schemas``.
_MESH_APPROXIMATION_CFG_MAP: dict[str, type[schemas.MeshCollisionBaseCfg]] = {
    "none": schemas.TriangleMeshPropertiesCfg,
    "convexHull": schemas.ConvexHullPropertiesCfg,
    "convexDecomposition": schemas.ConvexDecompositionPropertiesCfg,
    "meshSimplification": schemas.TriangleMeshSimplificationPropertiesCfg,
    "boundingCube": schemas.BoundingCubePropertiesCfg,
    "boundingSphere": schemas.BoundingSpherePropertiesCfg,
    "sdf": schemas.SDFMeshPropertiesCfg,
}


def set_mesh_collision_properties(prim_path: str, cfg: MeshCollisionPropertiesCfg):
    """Apply mesh collision properties to all mesh prims under *prim_path*.

    Delegates to the built-in :func:`isaaclab.sim.schemas.define_mesh_collision_properties`
    for each mesh child prim found in the hierarchy.
    """
    if cfg.mesh_approximation is None:
        return

    approx = cfg.mesh_approximation
    cfg_cls = _MESH_APPROXIMATION_CFG_MAP.get(approx)
    if cfg_cls is None:
        logger.warning(
            "Unsupported mesh approximation '%s'. Supported: %s",
            approx,
            list(_MESH_APPROXIMATION_CFG_MAP.keys()),
        )
        return

    # Build kwargs for the specific mesh collision cfg class
    mesh_cfg_kwargs: dict = {"mesh_approximation_name": approx}
    if approx == "sdf" and cfg.sdf_resolution is not None:
        mesh_cfg_kwargs["sdf_resolution"] = cfg.sdf_resolution

    mesh_cfg = cfg_cls(**mesh_cfg_kwargs)

    stage = get_current_stage()
    parent_prim = stage.GetPrimAtPath(prim_path)
    if not parent_prim.IsValid():
        return

    # Walk all child prims and apply mesh collision to mesh / collision prims
    queue = [parent_prim]
    while queue:
        child_prim = queue.pop(0)
        queue.extend(child_prim.GetChildren())

        if not (
            child_prim.IsA(UsdGeom.Mesh) or child_prim.HasAPI(UsdPhysics.CollisionAPI)  # type: ignore
        ):
            continue

        if approx == "none" and _is_part_of_rigid_body(child_prim):
            logger.warning(
                'Prim "%s" is part of a rigid body — consider using a collision approximation instead of "none".',
                child_prim.GetPath(),
            )

        child_prim_path = str(child_prim.GetPath())
        schemas.define_mesh_collision_properties(child_prim_path, mesh_cfg, stage=stage)


def _is_part_of_rigid_body(prim: Usd.Prim) -> bool:  # type: ignore[override]
    """Return True if *prim* or any ancestor has the RigidBodyAPI applied."""
    while prim.IsValid():
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):  # type: ignore
            return True
        prim = prim.GetParent()
    return False
