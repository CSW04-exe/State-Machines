# ---------------------------------------------------------------
# Author : Carter Ward
# Class  : CS 330-1
# Date   : 11/13/2025
#
# Program 4: Hard-coded State Machine.
# Implements the Passing Maneuver state machine.
# Simulates transitions using random probabilities for two scenarios
# and outputs state and transition statistics to text files.
# ---------------------------------------------------------------

import random

# ---------------------------------------------------------------
# Configuration and constants
# ---------------------------------------------------------------
SCENARIOS = {
    1: [0.8, 0.4, 0.3, 0.4, 0.3, 0.3, 0.8, 0.8, 0.8],
    2: [0.9, 0.6, 0.3, 0.2, 0.2, 0.4, 0.7, 0.9, 0.7],
}

STATE_NAMES = {
    1: "Follow",
    2: "Pull out",
    3: "Accelerate",
    4: "Pull in ahead",
    5: "Pull in behind",
    6: "Decelerate",
    7: "Done",
}

# State constants for readability
FOLLOW, PULL_OUT, ACCEL, PULL_IN_AHEAD, PULL_IN_BEHIND, DECEL, DONE = range(1, 8)

# ---------------------------------------------------------------
# Stub functions (state actions)
# ---------------------------------------------------------------
def log_state(f, state, trace):
    """Stub action for a state: log to file and increment count."""
    if trace:
        f.write(f"state= {state} {STATE_NAMES[state]}\n")


# ---------------------------------------------------------------
# Transition evaluation
# ---------------------------------------------------------------
def next_state(state, probs):
    """Return next state and triggered transition number, per assignment logic."""
    r = random.random()

    if state == FOLLOW:
        if r < probs[0]:
            return PULL_OUT, 1
        else:
            return FOLLOW, None

    elif state == PULL_OUT:
        if r < probs[1]:
            return ACCEL, 2
        elif r < probs[1] + probs[3]:
            return PULL_IN_BEHIND, 4
        else:
            return PULL_OUT, None

    elif state == ACCEL:
        if r < probs[2]:
            return PULL_IN_AHEAD, 3
        elif r < probs[2] + probs[4]:
            return PULL_IN_BEHIND, 5
        elif r < probs[2] + probs[4] + probs[5]:
            return DECEL, 6
        else:
            return ACCEL, None

    elif state == PULL_IN_AHEAD:
        if r < probs[8]:
            return DONE, 9
        else:
            return PULL_IN_AHEAD, None

    elif state == PULL_IN_BEHIND:
        if r < probs[6]:
            return FOLLOW, 7
        else:
            return PULL_IN_BEHIND, None

    elif state == DECEL:
        if r < probs[7]:
            return PULL_IN_BEHIND, 8
        else:
            return DECEL, None

    else:
        return DONE, None


# ---------------------------------------------------------------
# Scenario runner
# ---------------------------------------------------------------
def run_scenario(scenario, iterations, trace=True, out_file="scenario_output.txt"):
    probs = SCENARIOS[scenario]
    state_count = {s: 0 for s in STATE_NAMES}
    trans_count = {i: 0 for i in range(1, 10)}

    with open(out_file, "w") as f:
        f.write(f"scenario                = {scenario}\n")
        f.write(f"trace                   = {str(trace).upper()}\n")
        f.write(f"iterations              = {iterations}\n")
        f.write("transition probabilities= " + " ".join(map(str, probs)) + "\n")

        for i in range(1, iterations + 1):
            if trace:
                f.write(f"\niteration= {i}\n")
            state = FOLLOW

            while state != DONE:
                state_count[state] += 1
                log_state(f, state, trace)
                next_s, tnum = next_state(state, probs)
                if tnum:
                    trans_count[tnum] += 1
                state = next_s

            state_count[DONE] += 1
            if trace:
                f.write("state= 7 Done\n")

        total_s = sum(state_count.values())
        total_t = sum(trans_count.values())
        f.write("state counts            = " + " ".join(str(state_count[s]) for s in STATE_NAMES) + "\n")
        f.write("state frequencies       = " + " ".join(f"{state_count[s]/total_s:.3f}" for s in STATE_NAMES) + "\n")
        f.write("transition counts       = " + " ".join(str(trans_count[i]) for i in range(1, 10)) + "\n")
        f.write("transition frequencies  = " + " ".join(f"{trans_count[i]/total_t:.3f}" for i in range(1, 10)) + "\n")


# ---------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Scenario 1: trace ON, 100 iterations
    run_scenario(1, 100, trace=True, out_file="scenario1_output.txt")

    # Scenario 2: trace OFF, 1,000,000 iterations
    run_scenario(2, 1_000_000, trace=False, out_file="scenario2_output.txt")
