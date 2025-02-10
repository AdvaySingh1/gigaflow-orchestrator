#!/usr/bin/env python3
import subprocess
import argparse
import time
import os

# poll output of "ovs-appctl dpif-netdev/pmd-perf-show"
# and log it to a log file every N seconds


def main(args):
    running_seconds = 0
    while True:
        # create path using pathlib and counter
        next_log_path = os.path.join(args.destination, f'ovs-log-{running_seconds}-seconds.log')
        pmd_perf_log = subprocess.run(
                ['ovs-appctl', 'dpif-netdev/pmd-perf-show'], 
                capture_output=True, text=True)
        if pmd_perf_log:
            with open(next_log_path, 'w') as next_log:
                next_log.write(pmd_perf_log.stdout)
                # next_log.write(f"Dummy log for {running_seconds} seconds")
                print(f"Step {running_seconds} -> Wrote log to {next_log_path}")
        else:
            print(f"Step {running_seconds} -> Error: Could not write log to {next_log_path}")
        time.sleep(args.delay)
        running_seconds += args.delay


if __name__ == "__main__":
    CLI = argparse.ArgumentParser()
    CLI.add_argument("--destination", type=str, required=True)
    CLI.add_argument("--delay", type=int, required=True)
    # convert incoming args to a dictionary
    args = CLI.parse_args()
    main(args)
