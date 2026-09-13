# State-Machines

## Purpose

This is Program 4 for CS 330 (Game AI / Movement and Decision Making), the fourth assignment in the same course sequence as my earlier Dynamic-Movement, Path-Following, and Path-Finding projects. Where those programs dealt with continuous motion and pathing, this one moves into discrete decision-making: implementing a **hard-coded finite state machine (FSM)** that models a vehicle's passing maneuver on a road. The assignment exists to build practical experience with FSMs as a behavior-modeling tool in game AI — a pattern used constantly for NPC and vehicle logic — including how to encode states, transitions, and trigger probabilities, and how to validate that a hand-built state machine actually behaves the way it was designed to.

## Problem and Approach

The problem was to design and implement an FSM for a car overtaking another vehicle, then simulate it across two different probability scenarios and report on the resulting state/transition statistics.

The FSM has seven states:

1. `Follow` — trailing the car ahead
2. `Pull out` — moving into the passing lane
3. `Accelerate` — speeding up to pass
4. `Pull in ahead` — merging back in front of the passed car
5. `Pull in behind` — aborting/merging back behind the passed car
6. `Decelerate` — slowing down (e.g., an aborted pass)
7. `Done` — terminal state, maneuver complete

Transitions are triggered by nine numbered rules (1–9), each guarded by a probability rather than a fixed condition. I represented each state's outgoing logic as `if r < threshold` checks against a single random draw `r = random.random()` per step, so a state can either advance along one of its outgoing transitions or self-loop (stay in the same state) for another simulation step. The transition graph is:

- **1**: `Follow → Pull out` (prob. `probs[0]`)
- **2**: `Pull out → Accelerate` (prob. `probs[1]`)
- **4**: `Pull out → Pull in behind` (prob. `probs[3]`, cumulative with transition 2)
- **3**: `Accelerate → Pull in ahead` (prob. `probs[2]`)
- **5**: `Accelerate → Pull in behind` (prob. `probs[4]`, cumulative)
- **6**: `Accelerate → Decelerate` (prob. `probs[5]`, cumulative)
- **9**: `Pull in ahead → Done` (prob. `probs[8]`)
- **7**: `Pull in behind → Follow` (prob. `probs[6]`)
- **8**: `Decelerate → Pull in behind` (prob. `probs[7]`)

`Accelerate` and `Pull out` are the only states with more than one outgoing transition, so their branches use stacked/cumulative probability bands (e.g. `Accelerate` checks `r < probs[2]`, then `r < probs[2]+probs[4]`, then `r < probs[2]+probs[4]+probs[5]`) to divide the `[0,1)` range into "take transition 3", "take transition 5", "take transition 6", or "stay in Accelerate."

My approach was to hard-code the transition logic directly as a chain of `if/elif` branches keyed on the current state (rather than building a generic transition-table engine), since the assignment specifically calls for a "hard-coded state machine." I then wrapped that per-step logic in a scenario runner that drives the FSM from `Follow` to `Done`, repeated for a configurable number of iterations, tallying how often each state is visited and each transition fires, and dividing by totals to get frequencies I could sanity-check against the input probabilities.

## Structure and Methodologies

- **State representation**: states are plain integers `1`–`7`, given readable names via named constants (`FOLLOW, PULL_OUT, ACCEL, PULL_IN_AHEAD, PULL_IN_BEHIND, DECEL, DONE = range(1, 8)`) and a `STATE_NAMES` dict used for logging/output. This is a lightweight enum-by-convention rather than Python's `enum` module.
- **Transition logic**: `next_state(state, probs)` is the core transition function — a hard-coded `if/elif` dispatch on the current state that draws one random number and returns `(next_state, transition_number)`. This stands in for a transition table; instead of a lookup dict of `{(state, event): next_state}`, the branching *is* the table, matching the "hard-coded state machine" assignment framing.
- **Scenario configuration**: `SCENARIOS` is a dict mapping scenario number → a list of 9 transition probabilities (`probs[0]`…`probs[8]`), one per transition. This separates the "what can happen" (the FSM structure in `next_state`) from "how likely is it" (the scenario's probability vector), so the same state machine can be re-run under different tunings.
- **Counters**: `state_count` and `trans_count` are dicts that accumulate visit/fire counts per state and per transition across all iterations of a scenario, later converted to frequencies (proportions) for the summary output.
- **Dependencies**: only the Python standard library — `random` (specifically `random.random()` for uniform `[0,1)` draws) and built-in file I/O (`open`, `with`). No third-party libraries.
- **Output**: each scenario run writes a self-contained text report (`scenario1_output.txt`, `scenario2_output.txt`) via `run_scenario(...)`, with an optional `trace` mode that logs every single state visited on every iteration.

## Process

Running the program (`python WardCS330Program4.py`) executes both scenarios back to back from `__main__`:

1. **Initialize**: `run_scenario` is called with a scenario number, an iteration count, a `trace` flag, and an output filename. It loads that scenario's probability vector from `SCENARIOS`, zeroes out the state and transition counters, and opens the output file, writing a header (scenario number, trace flag, iteration count, probability vector).
2. **Simulate**: for each iteration, the FSM starts in `Follow` and repeatedly calls `next_state` — incrementing the visited state's counter, optionally logging it (if `trace`), and following whichever transition fires (or self-looping) — until the state reaches `Done`. Each iteration is an independent full run of the passing maneuver from start to finish.
3. **Scenario 1** (`trace=True`, 100 iterations, probabilities `0.8 0.4 0.3 0.4 0.3 0.3 0.8 0.8 0.8`): exercises the *verbose/debugging* path — every single state transition across all 100 iterations is written to `scenario1_output.txt`, so the file is large (100 traced runs) and lets me manually inspect individual maneuvers, confirm self-loops behave correctly, and confirm the machine always terminates at `Done`.
4. **Scenario 2** (`trace=False`, 1,000,000 iterations, probabilities `0.9 0.6 0.3 0.2 0.2 0.4 0.7 0.9 0.7`): exercises the *statistical convergence* path — no per-step trace, just final counts — so the output is small but the huge iteration count drives the empirical state/transition frequencies close to their theoretical values under this scenario's probabilities.
5. **Report**: after all iterations for a scenario complete, the runner writes final `state counts`, `state frequencies`, `transition counts`, and `transition frequencies` lines to the output file, summarizing behavior across the whole run.

## Outcome

Comparing the two output files confirms the FSM behaves correctly and as expected under both scenarios:

- Both scenarios' traced/counted runs only ever visit the seven defined states and only ever fire transitions 1–9, and every iteration terminates in `Done` (state 7) — there are no dead ends or invalid states, which is the basic correctness bar for a hard-coded FSM like this.
- **Scenario 1** (100 iterations, trace on): final state frequencies were `Follow 0.265, Pull out 0.269, Accelerate 0.124, Pull in ahead 0.043, Pull in behind 0.216, Decelerate 0.046, Done 0.037`. With `probs[0]=0.8` (a high `Follow → Pull out` chance) and a fairly even split between `Accelerate → Pull in ahead` (0.3) vs. the combined abort paths (`Pull in behind`/`Decelerate`, 0.3 + 0.3 = 0.6), the trace shows plenty of aborted passes (looping back through `Pull in behind → Follow` on transition 7) alongside successful ones — consistent with the lower probabilities given to the "commit and finish" path (`probs[2]=0.3`, `probs[8]=0.8`).
- **Scenario 2** (1,000,000 iterations, trace off): final state frequencies were `Follow 0.212, Pull out 0.238, Accelerate 0.159, Pull in ahead 0.068, Pull in behind 0.204, Decelerate 0.071, Done 0.048`, with transition frequencies close to their expected proportions (e.g. transition 1 at 0.245 vs. transition 7 at 0.184, reflecting `probs[0]=0.9` driving many `Follow → Pull out` transitions relative to the `Pull in behind → Follow` return path at `probs[6]=0.7`). At a million iterations the frequencies are smooth and stable rather than noisy the way the 100-iteration Scenario 1 numbers are, which is exactly what I'd expect: larger sample size converges the empirical frequencies toward the values implied by the input probabilities, giving me confidence the random-draw logic in `next_state` isn't biased or buggy.
- Together, the two runs show the same FSM code responding correctly and differently to two distinct probability tunings — Scenario 2's higher "keep moving forward" probabilities (`probs[0]=0.9`, `probs[6]=0.7`, `probs[8]=0.9` vs. Scenario 1's `0.8/0.8/0.8`) combined with a lower "abort to Pull in behind" probability on Accelerate (`probs[4]=0.2` vs. `0.3`) show up as small but consistent shifts in the aggregate frequencies, which is the kind of behavior a correctly-implemented FSM should produce.

This assignment reinforced FSM design as a concrete tool: defining a discrete state set, encoding event-driven transitions between them, and using probability rather than fixed conditions to drive branching decisions — plus validating a state machine empirically (via traced runs for close inspection and large-scale runs for statistical convergence) rather than just trusting the code. It's a direct extension of the decision-making side of game AI I'd been building toward through Dynamic-Movement, Path-Following, and Path-Finding, and it gave me a much better feel for how something as simple as chained `if` statements and a running counter can produce and verify complex, realistic-looking emergent behavior — like a car repeatedly aborting and retrying a pass — out of a small set of rules.

## How to run

```
python WardCS330Program4.py
```

This regenerates `scenario1_output.txt` (100 traced iterations) and `scenario2_output.txt` (1,000,000 untraced iterations) in the current directory.
