from typing import Dict, Any
try:
    import finesse
    from finesse.components import Laser, Mirror, Space, Beamsplitter
    from finesse.detectors import Power
except Exception as e:
    finesse = None
    Laser = Mirror = Space = Beamsplitter = Power = object  # placeholders

def ensure_finesse():
    if finesse is None:
        raise ImportError(\"Finesse 3 is not available. Please install finesse>=3 and try again.\")

def build_fp_cavity(model, cfg: Dict[str, Any]):
    \"\"\"Build a Fabry–Perot cavity from JSON.
    Expects two mirrors (m1, m2), a laser L0, spaces including the cavity space between m1 and m2.
    \"\"\"
    ensure_finesse()
    system = cfg[\"system\"]
    comps = system.get(\"components\", {})

    # Laser
    laser_cfg = system.get(\"laser\", {})
    P = float(laser_cfg.get(\"power\", 1.0))
    lam = float(laser_cfg.get(\"wavelength\", 1.064e-6))
    L0 = model.add(Laser(\"L0\", P=P, lam=lam))

    # Mirrors
    mirrors = {}
    for m in comps.get(\"mirrors\", []):
        mname = m[\"name\"]
        R = float(m.get(\"R\", 0.99))
        T = float(m.get(\"T\", 0.01))
        mirrors[mname] = model.add(Mirror(mname, R=R, T=T))

    # Spaces
    spaces = {}
    for s in comps.get(\"spaces\", []):
        sname = s[\"name\"]
        L = float(s.get(\"L\", 0.0))
        f = s.get(\"from\")
        t = s.get(\"to\")
        # Finesse 3 Python API uses ports like 'component.port'; we'll resolve later via model.get_port
        spaces[sname] = model.add(Space(sname, L=L, from_port=f, to_port=t))

    # Detectors (power)
    detectors = {}
    for d in comps.get(\"detectors\", []):
        if d.get(\"type\") == \"power\":
            name = d[\"name\"]
            port = d[\"port\"]
            detectors[name] = model.add(Power(name, port=port))

    return {\"laser\": L0, \"mirrors\": mirrors, \"spaces\": spaces, \"detectors\": detectors}
