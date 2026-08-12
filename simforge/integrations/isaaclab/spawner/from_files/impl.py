from __future__ import annotations

from typing import TYPE_CHECKING

from isaaclab.sim import clone
from isaaclab.sim.spawners.from_files.from_files import (
    spawn_from_usd as __spawn_from_usd,
)
from pxr import Usd

if TYPE_CHECKING:
    from simforge.integrations.isaaclab.spawner.from_files.cfg import (
        FileCfg,
        UsdFileCfg,
    )


@clone
def spawn_from_usd(
    prim_path: str,
    cfg: UsdFileCfg,
    translation: tuple[float, float, float] | None = None,
    orientation: tuple[float, float, float, float] | None = None,
    **kwargs,
) -> Usd.Prim:
    """Spawn a USD asset and apply SimForge-specific mesh collision properties.

    Delegates the heavy lifting (prim creation, rigid/collision/mass/… schemas,
    material binding) to the upstream
    :func:`isaaclab.sim.spawners.from_files.from_files.spawn_from_usd`, then
    applies any ``mesh_collision_props`` afterwards.
    """
    # Let the upstream spawner create the prim and apply all standard schemas
    prim = __spawn_from_usd(prim_path, cfg, translation, orientation, **kwargs)

    # Apply mesh collision approximation (must happen after collision schemas)
    if cfg.mesh_collision_props is not None:
        cfg.mesh_collision_props.func(prim_path, cfg.mesh_collision_props)

    return prim
