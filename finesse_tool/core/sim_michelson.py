from pathlib import Path
import numpy as np
import pandas as pd
try:
    import finesse
    from finesse.model import Model
    from finesse.components import Laser, Beamsplitter, Mirror, Space
    from finesse.detectors import Power
except Exception:
    finesse = None
    Model = object

from .builder import ensure_finesse

def run_michelson_basic(cfg, outdir: Path):
    ensure_finesse()
    m = Model()

    # Minimal Michelson: L0 -> BS -> arms to m1, m2; read power at BS output port p3
    # Parameters
    sys = cfg[\"system\"]
    lam = float(sys.get(\"laser\", {}).get(\"wavelength\", 1.064e-6))
    P = float(sys.get(\"laser\", {}).get(\"power\", 1.0))
    arm = float(sys.get(\"components\", {}).get(\"arm_length\", 1.0))
    dscan = cfg[\"simulation\"].get(\"scan\", {})
    start = float(dscan.get(\"start\", -1e-6))
    stop = float(dscan.get(\"stop\", 1e-6))
    num = int(dscan.get(\"num\", 1001))

    # Build
    L0 = m.add(Laser(\"L0\", P=P, lam=lam))
    bs = m.add(Beamsplitter(\"bs\", R=0.5, T=0.5))
    m1 = m.add(Mirror(\"m1\", R=0.999, T=0.001))
    m2 = m.add(Mirror(\"m2\", R=0.999, T=0.001))

    s_in = m.add(Space(\"s_in\", L=0.0, from_port=\"L0.p1\", to_port=\"bs.p1\"))
    s1 = m.add(Space(\"s1\", L=arm, from_port=\"bs.p2\", to_port=\"m1.p1\"))
    s2 = m.add(Space(\"s2\", L=arm, from_port=\"bs.p3\", to_port=\"m2.p1\"))

    PD = m.add(Power(\"PD_out\", port=\"bs.p4\"))

    xs = np.linspace(start, stop, num)
    ys = []
    for x in xs:
        s2.L = arm + x
        res = m.run()
        # same caveat as in cavity: extract PD value
        try:
            ys.append(float(res[PD]))
        except Exception:
            ys.append(np.nan)
        s2.L = arm  # reset

    df = pd.DataFrame({\"delta_L\": xs, \"PD_out\": ys})
    return df
