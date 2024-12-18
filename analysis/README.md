# Chess Game Data Analysis

This folder is where our data analysis, in Python, will be based. The data is found in the `data/` folder, in `pgn.zst` format.

### Processing the Data

This section documents our process of getting the data classified and in a format that supports our analysis goals.

1. Download the appropriate `.pgn.zst` file from [the lichess variants database](https://database.lichess.org#variant_games).

2. Use [PeaZip](https://peazip.github.io/peazip-64bit.html) on Windows (other platforms have other tools) to extract the `.pgn` from the `.zst` zipped file.

3. Run `pgn_parser.py` to compute all additional attributes on the data, and a `.csv` will be added to your `data/` folder with all the updated data.

### Data Attributes

<details>
<summary><b>A table showing every attribute of our analyzed data.</b></summary>

<br>

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

All attributes are analyzed and/or generated by [Josiah Plett](https://plett.dev/).

</details>
