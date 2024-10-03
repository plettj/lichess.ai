import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
df = pd.read_csv('...')
WhiteTimes = df['WhiteTimes'].apply(eval)
SumW = []
for i in range(len(WhiteTimes)):
    total_sum = sum(WhiteTimes[i])
    SumW.append(total_sum)

BlackTimes = df['BlackTimes'].apply(eval)
SumB = []
for i in range(len(BlackTimes)):
    total_sum = sum(BlackTimes[i])
    SumB.append(total_sum)
gamelenarray = np.array(SumW)+np.array(SumB)
name = ['Gamelength']
gamelen = pd.DataFrame(gamelenarray,columns =name)

EloDifference = df['WhiteElo'] - df['BlackElo']
name = ['EloDifference']
Elodif = pd.DataFrame(EloDifference,columns =name)

result = df['Result']
resultnames = np.unique(result)
resultDict=dict(zip(resultnames,range(len(resultnames)))) 
resultarray = np.array([resultDict[cl] for cl in result]) 
name = ['Result'] 
Result = pd.DataFrame(resultarray,columns =name) 

dfin = df[['WhiteElo', 'BlackElo','Middlegame', 'Endgame']] 
df = pd.concat([dfin, gamelen,Result,Elodif], axis=1)
