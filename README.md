# State-Machines

A hard-coded finite state machine that simulates a vehicle **passing maneuver**, driving state transitions with random-number-based probabilities and reporting the resulting state and transition statistics.

## 1. Purpose

This project exists to demonstrate, in code, how a real-world sequential process — a car pulling out from behind another vehicle, accelerating past it, and pulling back in — can be modeled as a finite state machine (FSM). Instead of hand-tracing a state diagram on paper, the program encodes the states and transition probabilities directly and lets random simulation show what actually happens over many runs. The goal is both educational (applying FSM theory from a Computer Science course to a concrete, non-trivial example) and practical (producing verifiable output that shows the machine behaves the way the underlying probability model predicts).

## 2. Problem and approach

The assignment (CS 330, Program 4 — "Hard-coded State Machine") was to implement a specific passing-maneuver FSM with **7 states** — `Follow`, `Pull out`, `Accelerate`, `Pull in ahead`, `Pull in behind`, `Decelerate`, and `Done` — connected by **9 numbered transitions**, each transition gated by a probability rather than a deterministic rule. Two different probability profiles ("scenarios") were assigned, and the program had to run each one, trace what happens, and tally results.

The approach taken was to:

- Hard-code the state graph directly in a `next_state()` function, using cumulative probability thresholds (`if r < probs[i]`) drawn from `random.random()` to decide which transition fires out of each state.
- Separate the two scenarios' transition-probability tables into a lookup dictionary (`SCENARIOS`) so the same simulation engine could run either data set unmodified.
- Run **Scenario 1** with tracing turned on for a small number of iterations (100), so every individual state visited is logged and can be manually checked against the state diagram.
- Run **Scenario 2** with tracing turned off for a large number of iterations (1,000,000), trading a step-by-step trace for statistically meaningful aggregate frequencies.
- Have the simulation self-report by counting every state visited and every transition taken, then converting those counts into frequencies, so the results are auditable without re-running the program.

## 3. Structure and methodologies

The implementation is a single, self-contained Python script (`WardCS330Program4.py`) with no external dependencies or frameworks — just the Python standard library (`random`). The key structures and techniques used:

- **Constants via tuple unpacking**: `FOLLOW, PULL_OUT, ACCEL, PULL_IN_AHEAD, PULL_IN_BEHIND, DECEL, DONE = range(1, 8)` gives each state a readable name backed by an integer id.
- **Dictionaries** for all lookup data: `STATE_NAMES` (id → display name), `SCENARIOS` (scenario number → list of 9 transition probabilities), and, at runtime, `state_count` and `trans_count` dictionaries that accumulate how many times each state/transition occurs.
- **A pure transition function** (`next_state(state, probs)`): given the current state and the active probability table, draws one random float and walks a chain of cumulative thresholds to decide the next state and which numbered transition fired (or `None` if the state simply loops on itself).
- **A stub action function** (`log_state`): a minimal per-state "action" hook, used here to write trace lines — structured so it could be extended with real per-state behavior later.
- **A driver function** (`run_scenario`): owns the simulation loop (loop until `DONE`), file I/O (writes to a scenario-specific `.txt` output file), and the end-of-run reporting (counts and frequencies for both states and transitions).
- **File-based reporting** instead of console output, so each scenario produces a durable, reviewable artifact (`scenario1_output.txt`, `scenario2_output.txt`).

## 4. Process

Judging from the code's organization and comments, the build followed a natural bottom-up path typical of a state-machine assignment:

1. **Model the state diagram first.** The states and the 9 transitions between them were translated into constants and a `STATE_NAMES` dictionary before any simulation logic was written, since the transition function depends on having named, numbered states to branch on.
2. **Implement the transition logic.** `next_state()` was written as a direct, per-state `if/elif` translation of the assigned state diagram, using cumulative probability ranges so a single random draw could cleanly select among a state's multiple possible outgoing transitions.
3. **Parameterize the two scenarios.** Rather than duplicating the transition function per scenario, the two assigned probability sets were pulled out into the `SCENARIOS` dictionary, keeping `next_state()` scenario-agnostic and reusable.
4. **Build the simulation driver and instrumentation.** `run_scenario()` wraps `next_state()` in a loop that runs until the `DONE` state is reached, incrementing `state_count`/`trans_count` along the way — this is the piece that turns a single transition rule into a full run of the machine.
5. **Add tracing as an option, not a requirement.** The `trace` flag lets the same driver either write a full step-by-step log (useful for verifying correctness by hand on a small run) or skip that overhead entirely for a run large enough that per-step output would be unusable.
6. **Run and capture both required scenarios.** The `__main__` block calls `run_scenario` twice — once for Scenario 1 (traced, 100 iterations) and once for Scenario 2 (untraced, 1,000,000 iterations) — and both outputs were committed alongside the code (`scenario1_output.txt` at roughly 57 KB of per-iteration trace, `scenario2_output.txt` as a compact statistical summary), so the results are reproducible evidence rather than just a claim.

## 5. Outcome

The program produces concrete, verifiable results. For Scenario 2 (1,000,000 iterations of the machine, probabilities `0.9 0.6 0.3 0.2 0.2 0.4 0.7 0.9 0.7`), the recorded output shows:

- **State visit frequencies**: Follow 0.212, Pull out 0.238, Accelerate 0.159, Pull in ahead 0.068, Pull in behind 0.204, Decelerate 0.071, Done 0.048.
- **Transition frequencies** across all 9 transitions, ranging from 0.041 to 0.245, computed directly from raw counts that sum correctly across a run of a million completed maneuvers.
- A separate, human-checkable Scenario 1 trace (100 traced iterations) that lets every individual transition be cross-referenced against the state diagram by hand.

Building this reinforced several concrete skills: translating an abstract state diagram into working conditional logic without a state-machine library to lean on; using cumulative probability thresholds correctly so that a single random draw fairly represents several weighted outcomes; separating simulation *rules* (the transition function) from simulation *data* (the per-scenario probability tables) so the same engine drives two different experiments; and designing self-reporting code (counters plus derived frequencies) so correctness can be checked from the output alone, at both small scale (traced) and large scale (aggregate statistics), rather than trusting the code by inspection alone. It demonstrates the ability to take a course-assigned specification with strict state/transition/probability requirements and turn it into a correct, reproducible, and independently verifiable simulation.
