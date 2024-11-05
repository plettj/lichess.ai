"""
DATA FORMAT REFERENCE

Result               {1, 0, -1}
WhiteElo             int > 0
BlackElo             int > 0
EloDifference        -1000 < int < 1000
TimeControl          {"180+0"}
Termination          {"Normal", "Time forfeit"}
FEN                  string                      # 960 different options
WhiteTimes           {int > 0}[]
BlackTimes           {int > 0}[]
TotalMoves           int > 0
Middlegame           int > 0
Endgame              {int > 0, -1}
WhiteOpeningTime     0 < int <= 1
BlackOpeningTime     0 < int <= 1
WhiteMiddlegameTime  {0 < int <= 1, -1}
BlackMiddlegameTime  {0 < int <= 1, -1}
WhiteEndgameTime     {0 < int <= 1, -1}
BlackEndgameTime     {0 < int <= 1, -1}
WhiteTotalTime       0 <= int <= 1
BlackTotalTime       0 <= int <= 1
"""

"""
REGRESSION - PART A - PART 1

Explain what variable is predicted based on which other variables and what
you hope to accomplish by the regression. Mention your feature transformation
choices such as one-of-K coding. Since we will use regularization momentarily,
apply a feature transformation to your data matrix X such that each column
has mean 0 and standard deviation 1.
"""

import csv
import ast

def regularize_data(data):
    pass
