import argparse
from .io.loader import load_config
from .core.sim_cavity import run_cavity_scan
from .core.sim_michelson import run_michelson_basic
from .plotting import plot_scan
import pandas as pd
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Finesse 3 JSON-driven simulations")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run a simulation from JSON")
    run_p.add_argument("--config", required=True, help="Path to JSON configuration")
    run_p.add_argument("--out", required=True, help="Output directory")

    args = parser.parse_args()

    cfg = load_config(args.config)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    system_type = cfg["system"]["type"].lower()
    topology = cfg["system"].get("topology", "").lower()

    if system_type == "cavity" and topology in ("fp", "fabry-perot", "fabry_perot"):
        df = run_cavity_scan(cfg, outdir)
        csv_path = outdir / "scan.csv"
        df.to_csv(csv_path, index=False)
        png_path = outdir / "scan.png"
        plot_scan(df, png_path, title="Fabry–Perot Cavity Scan")
        print(f\"Wrote: {csv_path}\")
        print(f\"Wrote: {png_path}\")
    elif system_type == "interferometer" and topology in ("michelson",):
        df = run_michelson_basic(cfg, outdir)
        csv_path = outdir / "scan.csv"
        df.to_csv(csv_path, index=False)
        png_path = outdir / "scan.png"
        plot_scan(df, png_path, title="Michelson Output (basic)")
        print(f\"Wrote: {csv_path}\") 
        print(f\"Wrote: {png_path}\")
    else:
        raise ValueError(f\"Unsupported system/type combination: {system_type=}, {topology=}\")

if __name__ == "__main__":
    main()
