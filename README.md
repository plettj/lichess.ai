# lichess.ai

Hosted publicly on [lichess.ai](https://lichess.ai/), this repo contains significant machine learning analysis of the popular [lichess.org Open Database](https://database.lichess.org/), specifically the **265,504** [Chess960](https://en.wikipedia.org/wiki/Fischer_random_chess) games from August 2024.

### Data Analysis

<details>
<summary>A table showing every attribute of our analyzed data.</summary>

<br>

Note that `EloDifference` and every attribute after `FEN` was computed by us.

| **Attribute**         | **Data Type / Values**       | **Description**                                                        |
| --------------------- | ---------------------------- | ---------------------------------------------------------------------- |
| `Result`              | `{1, 0, -1}`                 | 1 = White win, 0 = Draw, -1 = Black win                                |
| `WhiteElo`            | `int > 0`                    |                                                                        |
| `BlackElo`            | `int > 0`                    |                                                                        |
| `EloDifference`       | `-1000 < int < 1000`         | Signed difference between player Elos                                  |
| `TimeControl`         | `{"180+0"}`                  | Always 3\|0 time control                                               |
| `Termination`         | `{"Normal", "Time forfeit"}` | Game termination type                                                  |
| `FEN`                 | `string`                     | Forsyth-Edwards Notation for the starting board position (960 options) |
| `WhiteTimes`          | `{int > 0}[]`                | Array of time spent on each move by White                              |
| `BlackTimes`          | `{int > 0}[]`                | Array of time spent on each move by Black                              |
| `TotalPlies`          | `int > 0`                    | Total number of half-moves (plies) in the game                         |
| `Middlegame`          | `int > 0`                    | Ply number when the middlegame starts                                  |
| `Endgame`             | `{int > 0, -1}`              | Ply number when the endgame starts (-1 if no endgame)                  |
| `WhiteOpeningTime`    | `0 < int <= 1`               | Percentage of total time White spent in the opening                    |
| `BlackOpeningTime`    | `0 < int <= 1`               | Percentage of total time Black spent in the opening                    |
| `WhiteMiddlegameTime` | `0 < int <= 1`               | Percentage of total time White spent in the middlegame                 |
| `BlackMiddlegameTime` | `0 < int <= 1`               | Percentage of total time Black spent in the middlegame                 |
| `WhiteEndgameTime`    | `{0 < int <= 1, -1}`         | Percentage of total time White spent in the endgame (-1 if no endgame) |
| `BlackEndgameTime`    | `{0 < int <= 1, -1}`         | Percentage of total time Black spent in the endgame (-1 if no endgame) |
| `WhiteTotalTime`      | `0 <= int <= 1`              | Percentage of total time White used throughout the game                |
| `BlackTotalTime`      | `0 <= int <= 1`              | Percentage of total time Black used throughout the game                |

_All custom attributes were generated by [Josiah Plett](https://plett.dev/)._

---

</details>

### Machine Learning Analysis

Below is a summary of the notable analysis we performed.

#### 1. Data transformation

We parsed each [PGN](https://en.wikipedia.org/wiki/Portable_Game_Notation) and calculated the point where the middlegame and endgame began (based on [Stockfish](https://github.com/official-stockfish/Stockfish)'s strategies) for each game. We then computed the total thinking time of each player during all three periods of the game.

Other small adjustments were made too, like [standardizing](https://en.wikipedia.org/wiki/Standard_score) the data and including attributes like [Elo](https://en.wikipedia.org/wiki/Elo_rating_system) difference.

#### 2. Feature Extraction

In [Report 1](/lichess.ai/public/static/reports/feature-extraction-and-visualization.pdf) we performed [Principle Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis) to see which attributes had the biggest effect on the final result of each game.

#### 3. Regression for predicting Game Length

This part is of interest to any avid blitz players. In [Report 2](/lichess.ai/public/static/reports/supervised-learning-classification-and-regression.pdf), we explored how well one could predict the total [plies](<https://en.wikipedia.org/wiki/Ply_(game_theory)>) of their game based only on time spent during different periods of the game. [Regularization](<https://en.wikipedia.org/wiki/Regularization_(mathematics)>) was used to prevent overfitting. We discovered two interesting phenomenon.

First, a larger Elo difference between players actually indicates a (mildly) **increased** game length! This is because the stronger player intends to reduce variance in game outcome and therefore plays slower and more methodically.

Second, by getting a sense of purely how long (in clock time) the opening of your blitz chess game has taken, you can increase your prediction of game length (by plies)'s accuracy by over **20%**. Slower-moving openings lead to longer games!

These insights should help with [clock management](https://www.chess.com/article/view/the-art-of-time-management).

#### 4. Classification for predicting Game Outcome

Like Regression above, this section uses [two-layer](https://scikit-learn.org/1.5/auto_examples/model_selection/plot_nested_cross_validation_iris.html) 10-fold [cross-validation](<https://en.wikipedia.org/wiki/Cross-validation_(statistics)>) to assess the strength of each [Classification Tree](https://en.wikipedia.org/wiki/Decision_tree_learning) model trained on subsets of our data.

Interestingly, using Classification Trees on input like time usage throughout the game, one can predict the outcome of a game **1.19 times** better than purely looking at the Elo difference of the players. Specifically, the error rate decreases from **36.64%** to **30.70%**.

### Usage

Take a look at our analysis [README.md](/analysis/README.md).

### lichess.ai website

The website ([lichess.ai](https://lichess.ai)) is created with [Next.js](https://nextjs.org/docs) with [Tailwind](https://tailwindcss.com/docs/), [shadcn/ui](https://ui.shadcn.com/docs/components/button), [pnpm](https://pnpm.io/installation), and hosted on [Vercel](https://vercel.com/docs).
