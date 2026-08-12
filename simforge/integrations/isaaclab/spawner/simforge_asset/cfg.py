from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import MISSING
from typing import Any

from isaaclab.utils.configclass import configclass

from simforge import Articulation, Geometry, Model
from simforge.integrations.isaaclab.spawner.from_files import FileCfg
from simforge.integrations.isaaclab.spawner.simforge_asset.impl import (
    spawn_simforge_assets,
)


@configclass
class SimforgeAssetCfg(FileCfg):
    func: Callable = spawn_simforge_assets

    assets: list[Articulation | Geometry | Model] = MISSING  # type: ignore
    export_kwargs: Mapping[str, Any] = {}

    num_assets: int = 1
    seed: int = 0
    use_cache: bool = True

    random_choice: bool = False
