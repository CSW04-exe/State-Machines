# State Machines — Passing Maneuver FSM

**Type:** Individual project
**Contributor:** Carter Ward
**Course:** CS 330-1 (Artificial Intelligence / Game AI) — Program 4
**Completed:** 11/13/2025

## Purpose
This program implements a hard-coded finite state machine modeling a car's passing maneuver on a road. It's Program 4 in the CS 330 Game AI sequence, following Dynamic-Movement, Path-Following, and Path-Finding, moving from continuous motion into discrete, probability-driven decision-making. The goal was to build practical experience encoding states, transitions, and trigger probabilities, and to validate the resulting FSM empirically.

## Problem and Approach
The task was to design an FSM for a car overtaking another vehicle, then simulate it under two probability scenarios and report the resulting statistics. The FSM has seven states (Follow, Pull out, Accelerate, Pull in ahead, Pull in behind, Decelerate, Done) connected by nine probability-guarded transitions. Each state's outgoing logic draws one random number per step and compares it against thresholds (stacked/cumulative for states with multiple outgoing transitions) to decide whether to advance or self-loop. I hard-coded the transition logic as `if/elif` branches per the assignment's requirement for a hard-coded state machine, then wrapped it in a scenario runner that drives the FSM from Follow to Done across many iterations, tallying state and transition frequencies.

## Structure and Methodologies
- States as named integer constants (`FOLLOW, PULL_OUT, ACCEL, ...`) with a `STATE_NAMES` dict for output, rather than `enum`
- `next_state(state, probs)`: hard-coded `if/elif` dispatch that draws a random number and returns the next state and firing transition
- `SCENARIOS`: a dict of scenario number → 9-element probability vector, separating FSM structure from its tuning
- Counters accumulate per-state and per-transition counts across iterations, converted to frequencies for reporting
- Standard library only (`random.random()` for draws, built-in file I/O) — no third-party dependencies

## Process
1. `run_scenario` loads a scenario's probability vector, zeroes counters, and opens an output file
2. Each iteration runs the FSM from Follow to Done, tallying visited states and fired transitions
3. Scenario 1: 100 iterations, traced (every state visit logged) — for manual inspection of individual maneuvers
4. Scenario 2: 1,000,000 iterations, untraced — for statistical convergence of frequencies
5. Final state/transition counts and frequencies are written to each scenario's output file

## Outcome
Both scenarios terminated every iteration in `Done` with no invalid states, confirming basic FSM correctness. Scenario 1 (100 iterations) produced state frequencies of Follow 0.265, Pull out 0.269, Accelerate 0.124, Pull in ahead 0.043, Pull in behind 0.216, Decelerate 0.046, Done 0.037 — noisier numbers reflecting the small sample size. Scenario 2 (1,000,000 iterations) produced Follow 0.212, Pull out 0.238, Accelerate 0.159, Pull in ahead 0.068, Pull in behind 0.204, Decelerate 0.071, Done 0.048, with transition frequencies stable and smooth rather than noisy. The shift between scenarios (e.g. Scenario 2's higher `Follow → Pull out` and `Pull in ahead → Done` probabilities versus a lower `Accelerate → Pull in behind` abort chance) showed up as consistent shifts in aggregate frequencies, confirming the random-draw logic responds correctly to different tunings. This project reinforced FSM design as a concrete tool — discrete states, probability-driven transitions — and the value of validating a state machine empirically via both traced and large-scale runs.

## How to run
```
python WardCS330Program4.py
```
This regenerates `scenario1_output.txt` (100 traced iterations) and `scenario2_output.txt` (1,000,000 untraced iterations).
