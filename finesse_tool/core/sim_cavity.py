from pathlib import Path
import numpy as np
import pandas as pd
try:
    import finesse
    from finesse.model import Model
except Exception:
    finesse = None
    Model = object

from .builder import build_fp_cavity, ensure_finesse

def run_cavity_scan(cfg, outdir: Path):
    ensure_finesse()
    sim = cfg[\"simulation\"]
    scan_cfg = sim.get(\"scan\", {})
    param = scan_cfg.get(\"param\", \"s2.L\")
    start = float(scan_cfg.get(\"start\", -1e-6))
    stop = float(scan_cfg.get(\"stop\", 1e-6))
    num = int(scan_cfg.get(\"num\", 1001))

    readout = sim.get(\"readout\")  # detector name
    if not readout:
        raise ValueError(\"simulation.readout must reference a detector name defined in system.components.detectors\")

    # Build model
    m = Model()
    built = build_fp_cavity(m, cfg)

    # Prepare scan
    xs = np.linspace(start, stop, num)
    ys = []

    # We will scan by adjusting a parameter attribute on the model.
    # For simplicity, support space length scan: e.g., 's2.L'
    space_name, attr = param.split(\".\")
    if attr != \"L\":
        raise ValueError(\"Currently only scanning Space length ('.L') is implemented for FP cavity.\")

    for x in xs:
        # set parameter
        space = built[\"spaces\"][space_name]
        space.L = x + float(space.L)  # small offset around nominal
        # run DC solution and read detector
        res = m.run()
        pd_det = built[\"detectors\"][readout]
        val = float(res[pd_det]) if isinstance(res, dict) and pd_det in res else getattr(res, readout, np.nan)
        ys.append(val)

        # reset back nominal (simple approach: subtract x again)
        space.L = float(space.L) - x

    df = pd.DataFrame({param: xs, readout: ys})
    return df
