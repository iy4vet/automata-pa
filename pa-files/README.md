# Programming Assignment Solutions

## Question 1: Hidden Markov Models

### `construct.py` - Building the HMM

xedThis script builds a Hidden Markov Model from a dataset of tagged sentences. It counts occurrences in the input data to produce two probability matrices:

- **Transition probabilities (A)**: how likely each state is to follow another state
- **Observation probabilities (B)**: how likely each word is to appear in each state

It then writes both matrices to an output file for the prediction step.

### `predictions.py` - Viterbi Decoding

Takes observation sequences and finds the most probable state sequence using the Viterbi algorithm. The code uses a custom `HMM` dataclass to hold the model parameters (transition and observation matrices, initial state, dimensions).

The Viterbi implementation maintains two tables:

- `delta[t][s]`: maximum probability of reaching state `s` at time `t`
- `psi[t][s]`: best previous state for reaching state `s` at time `t`

It starts by initialising probabilities for the first observation, combining initial state probabilities with observation likelihoods. For each subsequent time step, it finds the best path to each state by considering all possible previous states. Finally, it backtracks through `psi` to reconstruct the optimal state sequence.

## Question 2: Recursive Descent Parser

### `q2.py` - Syntax Analysis

A two-phase parser that validates code against a simple grammar. The tokeniser splits raw text into structured tokens with types (`IDENTIFIER`, `KEYWORD`, `INTEGER`, `FLOAT`, `SYMBOL`) stored as tuples.

The `Parser` class tracks its position in the token list via instance variables. Each grammar rule maps to its own method (`parse_atom`, `parse_factor`, `parse_expr`, etc.) - each one either consumes expected tokens or calls other parsing methods. `peek()` and `consume()` handle token traversal and validation.

For example, `parse_if_statement` expects an `if` keyword, calls `parse_cond` for the condition, optionally consumes a `then`, parses the main statement, handles an optional `else` clause, and finally looks for an `endif`. This mirrors the grammar structure directly in code.
