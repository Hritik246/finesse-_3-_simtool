[README.md](https://github.com/user-attachments/files/21821063/README.md)
# Finesse 3 Simulation Tool

A Python-based command-line tool that reads a JSON configuration, builds an optical system using the **Finesse 3 Python API**, runs simulations, and writes plots and data files.

- **Focus**: Optical cavities (Fabry–Perot) .
- **Next**: Basic interferometry (Michelson) scaffold included.
- **Input**: JSON specification.
- **Output**: CSV data and PNG plots in an output folder.

> Tested with Python 3.10+. Requires a working Finesse 3 installation.

---

## Quick Start

```bash
# 1) Create & activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Run an example Fabry–Perot cavity
python -m finesse_tool run --config examples/fp_cavity.json --out runs/fp

# 4) (Optional) Run Michelson scaffold (currently basic power readout)
python -m finesse_tool run --config examples/michelson_basic.json --out runs/mich
```

Outputs will appear under the folder provided with `--out`, e.g. `runs/fp/`:
- `scan.csv` – numerical results
- `scan.png` – the plot of the scan

---

## JSON Schema (simplified)

```json
{
  "system": {
    "type": "cavity",        // "cavity" | "interferometer"
    "topology": "FP",        // For cavity: "FP" (Fabry–Perot). For interferometer: "Michelson"
    "laser": { "power": 1.0, "wavelength": 1.064e-6 },
    "components": {
      "mirrors": [
        {"name": "m1", "R": 0.99, "T": 0.01},
        {"name": "m2", "R": 0.99, "T": 0.01}
      ],
      "spaces": [
        {"name": "s1", "from": "L0.p1", "to": "m1.p1", "L": 0.0},
        {"name": "s2", "from": "m1.p2", "to": "m2.p1", "L": 1.0}
      ],
      "beamsplitters": [],
      "detectors": [
        {"type": "power", "name": "PD_trans", "port": "m2.p2"}
      ]
    }
  },
  "simulation": {
    "scan": {"param": "s2.L", "start": -1e-6, "stop": 1e-6, "num": 1001},
    "readout": "PD_trans"   // detector name to record
  }
}
```

For a **Michelson** (scaffold), switch `type` to `"interferometer"` and `topology` to `"Michelson"`. See `examples/michelson_basic.json`.

---

## Design

- `finesse_tool/core/builder.py` – parses JSON and builds Finesse 3 models.
- `finesse_tool/core/sim_cavity.py` – Fabry–Perot cavity simulation (implemented).
- `finesse_tool/core/sim_michelson.py` – basic Michelson scaffold (extend here).
- `finesse_tool/io/loader.py` – JSON loader and validation helpers.
- `finesse_tool/cli.py` – command-line interface.
- `finesse_tool/plotting.py` – matplotlib plotting helpers.

---

## Extending

- Add other cavities (e.g., bow-tie) by authoring a new builder function reusing the same JSON schema shape.
- Add more detectors (e.g., frequency response, phase readouts) by extending `builder.py` and `plotting.py`.
- Add unit tests in `tests/`.

---

## License

MIT
