from collections.abc import Callable

from isaaclab.sim.spawners.from_files.from_files_cfg import FileCfg as __FileCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg as __UsdFileCfg
from isaaclab.utils.configclass import configclass

from simforge.integrations.isaaclab.schemas import MeshCollisionPropertiesCfg
from simforge.integrations.isaaclab.spawner.from_files.impl import spawn_from_usd


@configclass
class FileCfg(__FileCfg):
    """Extended file configuration that adds mesh collision property support.

    Inherits all fields from :class:`isaaclab.sim.spawners.from_files.from_files_cfg.FileCfg`,
    including ``physics_material`` and ``visual_material``.
    """

    mesh_collision_props: MeshCollisionPropertiesCfg | None = None
    """Mesh collision approximation settings applied after spawning."""


@configclass
class UsdFileCfg(FileCfg, __UsdFileCfg):
    func: Callable = spawn_from_usd
