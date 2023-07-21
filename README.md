
# Knight's Tour Visualization

_A [Knight's tour](https://en.wikipedia.org/wiki/Knight%27s_tour) visualizer with 2 main algorithm: brute-force and Warnsdorff's rule_

## Build
```
$ pip install -r requirements.txt
```


## Introduction
The Knight's Tour problem is a mathematical puzzle where the goal is to find a sequence of moves for a knight on a chessboard such that the knight visits every square exactly once.

## Algorithms
There are 2 algorithms illustrated in this application:
- Simple brute-force
- Warnsdorff heuristic

## Note
- This application only consider NxN boards with N>=5, since there is no solution for N < 5.
- If N is odd, you must start at a dark square, or there will not be any complete tour at all. Try to explain why!
- When N is odd, Warnsdorff's heuristic can turn into regular backtracking, since it's not guaranteed to find a solution in linear time.
- Brute-force algorithm often fail to find a solution in less than 15 minutes with N = 5, since it takes an average of 100,000 steps to find a solution.