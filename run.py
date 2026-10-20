import argparse
import json

from bot.simulator import run_simulation, save_artifacts, synthetic_bars

parser = argparse.ArgumentParser(description="Deterministic paper-trading MVP; simulator only")
parser.add_argument("--bars", type=int, default=500)
parser.add_argument("--seed", type=int, default=7)
parser.add_argument("--out", default="artifacts")
args = parser.parse_args()
trades, report = run_simulation(synthetic_bars(args.bars, args.seed))
save_artifacts(trades, report, args.out)
print(json.dumps(report, indent=2))
