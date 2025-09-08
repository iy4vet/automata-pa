#!/bin/python3

# imports
import dataclasses
import pathlib
import sys
import os


# dataclass for hmm
@dataclasses.dataclass
class HMM:
    q0: int
    num_states: int
    num_obs: int
    mat_transition: list[list[float]]
    mat_observation: list[list[float]]


# function to read in hmm from file
def read_hmm(hmm_file: pathlib.Path) -> HMM:
    with open(hmm_file, "r", encoding="utf-8") as file:
        # init matrix A (transition matrix)
        mat_A: list[list[float]] = []
        # read first line to get number of states
        fl: str = file.readline().strip()
        num_states: int = len(fl.split(" "))
        # assemble first row of A
        mat_A.append([float(x) for x in fl.split(" ")])
        # read remaining rows of A
        for _ in range(num_states - 1):
            mat_A.append([float(x) for x in file.readline().strip().split(" ")])
        # init matrix B (observation matrix)
        mat_B: list[list[float]] = []
        # read first line to get number of observables
        fl = file.readline().strip()
        num_obs: int = len(fl.split(" "))
        # assemble first row of B
        mat_B.append([float(x) for x in fl.split(" ")])
        # read remaining rows of B
        for _ in range(num_states - 1):
            mat_B.append([float(x) for x in file.readline().strip().split(" ")])
        # hardcoded initial state (sad but what can you do :/)
        q0: int = 0
        # assemble and return the hmm
        return HMM(
            q0=q0,
            num_states=num_states,
            num_obs=num_obs,
            mat_transition=mat_A,
            mat_observation=mat_B,
        )


# function to predict most probable state run via viterbi's
def viterbi(hmm: HMM, obs_run: list[int]) -> list[int]:
    # length of observation run
    obs_len: int = len(obs_run)
    # init delta and psi tables
    delta: list[list[float]] = [
        [0.0 for _ in range(hmm.num_states)] for _ in range(obs_len)
    ]
    psi: list[list[int]] = [[0 for _ in range(hmm.num_states)] for _ in range(obs_len)]
    # base case (t = 0)
    for s in range(hmm.num_states):
        delta[0][s] = (
            hmm.mat_transition[hmm.q0][s] * hmm.mat_observation[s][obs_run[0]]
        )  # assuming uniform prior
        psi[0][s] = 0
    # recursive case (t > 0)
    for t in range(1, obs_len):
        for s in range(hmm.num_states):
            max_prob: float = -1.0
            max_state: int = -1
            for s_prev in range(hmm.num_states):
                prob: float = (
                    delta[t - 1][s_prev]
                    * hmm.mat_transition[s_prev][s]
                    * hmm.mat_observation[s][obs_run[t]]
                )
                if prob > max_prob:
                    max_prob = prob
                    max_state = s_prev
            delta[t][s] = max_prob
            psi[t][s] = max_state
    # backtrack to find most probable state run
    state_run: list[int] = [0 for _ in range(obs_len)]
    # find the final state with the highest probability
    max_prob: float = -1.0
    max_state: int = -1
    for s in range(hmm.num_states):
        if delta[obs_len - 1][s] > max_prob:
            max_prob = delta[obs_len - 1][s]
            max_state = s
    state_run[obs_len - 1] = max_state
    # backtrack through psi table
    for t in range(obs_len - 2, -1, -1):
        state_run[t] = psi[t + 1][state_run[t + 1]]
    return state_run


# --- main code ---

# arg check and parse
if len(sys.argv) != 2:
    print("Usage: python predictions.py '<input_path>'")
    sys.exit(1)
input_str = sys.argv[1]
lines_to_write = []

# fr main code
with open(input_str, "r", encoding="utf-8") as file:
    # open dataset corresponding to hmm
    hmm_dataset_file = file.readline().strip()
    base, ext = os.path.splitext(hmm_dataset_file)
    hmm_file_path = f"{base}_output.txt"
    # check if hmm file is in the same directory as input file
    input_dir = os.path.dirname(input_str)
    potential_hmm_path = os.path.join(input_dir, os.path.basename(hmm_file_path))
    # if not, check if it's in the root folder
    if not os.path.exists(potential_hmm_path):
        potential_hmm_path = hmm_file_path
    # open and read hmm
    hmm = read_hmm(pathlib.Path(potential_hmm_path))
    # read number of test cases
    num_cases: int = int(file.readline().strip())
    # run through test cases
    for _ in range(num_cases):
        # read and ignore the length of the upcoming observation run
        _ = int(file.readline().strip())
        # read the observation run
        obs_run: list[int] = [int(x) for x in file.readline().strip().split()]
        # predict state run
        state_run: list[int] = viterbi(hmm, obs_run)
        # save output
        lines_to_write.append(" ".join(map(str, state_run)) + "\n")

# write output to file
base, ext = os.path.splitext(input_str)
output_file = open(f"{base}_output.txt", "w")
output_file.writelines(lines_to_write)
output_file.close()
