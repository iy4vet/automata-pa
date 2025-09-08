#!/bin/python3

# imports
import dataclasses
import pathlib
import sys
import os


# define a dataclass to hold results from read_runs
@dataclasses.dataclass
class RunData:
    q0: int
    states_list: list[int]
    observables_list: list[int]
    transitions: dict[int, dict[int, int]]
    observations: dict[int, dict[int, int]]


# read the input and parse each run, return A and B
def read_runs(path: pathlib.Path) -> RunData:
    # init q0
    q0: int = -1
    # init sets for states and observables
    states_set = set()
    observables_set = set()
    # init dicts for transitions and observations
    transitions: dict[int, dict[int, int]] = {}
    observations: dict[int, dict[int, int]] = {}
    # open given file
    with open(path, "r", encoding="utf-8") as f:
        # read number of runs in file
        runs: int = int(f.readline())
        # process each run
        for _ in range(runs):
            # read in states and observations for this run
            states: list[int] = list(map(int, f.readline().split()))
            obs: list[int] = list(map(int, f.readline().split()))
            # set q0 if not set
            if q0 == -1:
                q0 = states[0]
            # add to sets
            states_set.update(states)
            observables_set.update(obs)
            # process transitions
            for i in range(len(states) - 1):
                u, v = states[i], states[i + 1]
                # init dicts
                transitions.setdefault(u, {})
                transitions[u].setdefault(v, 0)
                # increment count
                transitions[u][v] += 1
            # process observations
            for s, o in zip(states, obs):
                # init dicts
                observations.setdefault(s, {})
                observations[s].setdefault(o, 0)
                # increment count
                observations[s][o] += 1
    # assemble and return run data
    return RunData(
        q0,
        list(sorted(states_set)),
        list(sorted(observables_set)),
        transitions,
        observations,
    )


# construct matrices A and B from transitions and observations
def construct_matrices(run_data: RunData) -> list[str]:
    lines = []
    # unpack given run data
    q0, states_list, observables_list, transitions, observations = dataclasses.astuple(
        run_data
    )
    # write out matrix A
    # loop over rows
    for u in states_list:
        line = ""
        # collect total transitions from u
        sum_u: int = sum(transitions[u].values()) if u in transitions else 0
        # loop over columns in row
        for v in states_list:
            # write probability or 0
            if sum_u > 0 and (u in transitions) and (v in transitions[u]):
                line += f"{(transitions[u][v] / sum_u):.5f} "
            else:
                line += "0.00000 "
        lines.append(line.strip() + "\n")
    # write out matrix B
    # loop over rows
    for u in states_list:
        line = ""
        # collect total observations from u
        sum_u: int = sum(observations[u].values()) if u in observations else 0
        # loop over columns in row
        for o in observables_list:
            # write probability or 0
            if sum_u > 0 and (u in observations) and (o in observations[u]):
                line += f"{(observations[u][o] / sum_u):.5f} "
            else:
                line += "0.00000 "
        lines.append(line.strip() + "\n")
    return lines


# --- main code ---

# arg check and parse
if len(sys.argv) != 2:
    print("Usage: python construct.py '<input_path>'")
    sys.exit(1)
input_str = sys.argv[1]

# fr main code
run_data = read_runs(pathlib.Path(input_str))
lines_to_write = construct_matrices(run_data)

# write output to file
base, ext = os.path.splitext(input_str)
output_file = open(f"{base}_output.txt", "w")
output_file.writelines(lines_to_write)
output_file.close()
