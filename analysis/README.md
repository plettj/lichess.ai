# Chess Game Data Analysis

This folder is where our data analysis, in Python, will be based. The data is found in the `data/` folder, in `pgn.zst` format.

### Processing the Data

This section documents our process of getting the data classified and in a format that supports our analysis goals.

1. Download the appropriate `.pgn.zst` file from [the lichess variants database](https://database.lichess.org#variant_games).

2. Use [PeaZip](https://peazip.github.io/peazip-64bit.html) on Windows (other platforms have other tools) to extract the `.pgn` from the `.zst` zipped file.

3. Remove all non-blitz games: anything faster than 3|1 and slower than 5|5 ([explanation of time controls](https://support.chess.com/en/articles/8584509-how-do-time-controls-work-on-chess-com#:~:text=is%20Daily%20Chess%3F-,Understanding%20time%20controls,represented%20by%20two%20numbers)), and parse the data into a `.csv`.

4. Classify additional attributes representing beginning, middle, and end game average move time as a _Continuous_, _Ratio_ attribute, normalized to be relative to the total time spent during the game.

5. Calculate the variance between individual move times across the three stages of the game, creating three _Continuous_, _Ordinal_ attributes.
