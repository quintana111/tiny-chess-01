# Tiny Chess Search

A deterministic, standard-library-only chess bot for tiny-chess-01. It parses FEN, searches legal positions with fixed-depth alpha-beta, orders captures, and posts UCI moves through `MAKEFUN_ENV_URL`. `main.py` is self-contained and does not read repository files.

## Run

`MAKEFUN_ENV_URL=http://... python3 main.py`

The search uses depth 2 below each candidate and a fixed 25,000-node cap; ties follow deterministic UCI ordering. The environment remains the authority for root legal moves.
