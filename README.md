# AT - Programming Assignment

Coursework for the CS1.302 - Automata Theory (Monsoon '25) course at IIIT Hyderabad. Two problems - one on probabilistic modelling, one on formal language processing.

## Questions

### Question 1 - Hidden Markov Models

Given tagged training data, build an HMM and use the Viterbi algorithm to decode the most likely hidden state sequence from observations.

- **`construct.py`** - reads training data and computes the transition and observation probability matrices.
- **`predictions.py`** - runs Viterbi decoding with dynamic programming (delta/psi tables) to recover the optimal state path.

### Question 2 - Recursive Descent Parser

A two-phase compiler frontend: first tokenise, then parse.

- **Tokeniser** - breaks raw source into identifiers, keywords (`if`, `else`, `print`), integers, floats, and symbols.
- **Parser** - walks the token stream against a grammar that supports if-else-endif, arithmetic, comparisons, and print statements. Outputs "Lexical Error", "Syntax Error", or "No Error".

## Structure

```txt
pa-files/
├── README.md               Detailed solution documentation
├── q2 explanation.md        In-depth Q2 tokeniser & parser breakdown
├── materials/               Test data, autograders, assignment spec
├── Question-1/
│   ├── construct.py         HMM construction
│   └── predictions.py       Viterbi decoding
└── Question-2/
    └── q2.py                Tokeniser + recursive descent parser
```

## Running

```bash
# Question 1 - Part 1 (construct HMM)
cd pa-files/Question-1
python construct.py

# Question 1 - Part 2 (Viterbi predictions)
python predictions.py

# Question 2 (parser)
cd pa-files/Question-2
python q2.py
```

Autograders are in `pa-files/materials/` - see the instructions files there for usage.
