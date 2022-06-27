import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir("C:/Users/Syafiq Irfan/OneDrive/Desktop/Projects/EPL_2122")
epl_2122 = pd.read_csv("EPL_2122.csv")

epl_2122.isna().sum()
print(epl_2122)

## Teams with the most Home goals----------------------------------------------

Home = epl_2122.loc[:,["HomeTeam", "FTHG"]]
print(Home)
HomeGoals = Home.groupby('HomeTeam',as_index = False)['FTHG'].sum().sort_values(by = 'FTHG', ascending=True)
print(HomeGoals)

c = ['green']
bar = HomeGoals.plot.barh(x="HomeTeam", y="FTHG", alpha=1, color=c)
bar.set_xlabel("Goals Scored")
bar.set_ylabel("Teams")
bar.title.set_text("Goals Scored by Home Teams")

## Teams with the most Away goals----------------------------------------------

Away = epl_2122.loc[:,["AwayTeam", "FTAG"]]
print(Away)
AwayGoals = Away.groupby('AwayTeam',as_index = False)['FTAG'].sum().sort_values(by = 'FTAG', ascending=True)
print(AwayGoals)

c = ['red']
bar = AwayGoals.plot.barh(x="AwayTeam", y="FTAG", alpha=1, color=c)
bar.set_xlabel("Goals Scored")
bar.set_ylabel("Teams")
bar.title.set_text("Goals Scored by Away Teams")

## Teams with most goals-------------------------------------------------------

numberofgoalscored = AwayGoals.join(HomeGoals)
numberofgoalscored['Total Goals Scored'] = numberofgoalscored.FTHG + numberofgoalscored.FTAG

numberofgoalscored = numberofgoalscored.drop(columns= ['HomeTeam'])
numberofgoalscored['Team']  = numberofgoalscored['AwayTeam']
numberofgoalscored = numberofgoalscored.drop(columns = 'AwayTeam')
numberofgoalscored = numberofgoalscored[['Team','FTAG','FTHG','Total Goals Scored']]

## Teams with most goals conceded----------------------------------------------

mostgoalsconceded = epl_2122.loc[:,['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
hometeamconceded = mostgoalsconceded.groupby('HomeTeam',as_index = False)['FTAG'].sum().sort_values(by = 'FTAG', ascending=True)
awayteamconceded = mostgoalsconceded.groupby('AwayTeam',as_index = False)['FTHG'].sum().sort_values(by = 'FTHG', ascending=True)
totalgoalsconceded = awayteamconceded.join(hometeamconceded)
totalgoalsconceded['Total Goals Conceded'] = totalgoalsconceded.FTHG + totalgoalsconceded.FTAG

totalgoalsconceded['Team'] = totalgoalsconceded['AwayTeam']
totalgoalsconceded = totalgoalsconceded.drop(columns= ['HomeTeam','AwayTeam'])
totalgoalsconceded = totalgoalsconceded[['Team','FTHG','FTAG','Total Goals Conceded']]

## Goal Difference-------------------------------------------------------------

mosteffectiveteam = totalgoalsconceded.join(numberofgoalscored['Total Goals Scored'])

mosteffectiveteam = mosteffectiveteam.reset_index()
mosteffectiveteam = mosteffectiveteam.drop(columns='index')
mosteffectiveteam = mosteffectiveteam.drop(columns= ['FTAG','FTHG'])

mosteffectiveteam['Goals/Conceded Goals'] = mosteffectiveteam['Total Goals Scored']/ mosteffectiveteam['Total Goals Conceded']
mosteffectiveteam = mosteffectiveteam.sort_values(by='Goals/Conceded Goals',ascending=True)


# Plotting the most effective team
ax = mosteffectiveteam.plot.scatter(x = 'Total Goals Conceded', y = 'Total Goals Scored', figsize = (15,10),color = c)
# Plotting the labels for the scatter plot
mosteffectiveteam[['Total Goals Conceded','Total Goals Scored','Team']].apply(lambda x: ax.text(*x),axis=1)
# Making the labels bigger
plt.rcParams.update({'font.size': 14})
plt.tick_params(axis='x', labelsize=14)
plt.tick_params(axis='y', labelsize=14)
# Inverting x axis so the least number of goals is on the right side instead of left
plt.gca().invert_xaxis()
# Labeling the data
plt.xlabel('Total Goals Conceded', fontsize=18)
plt.ylabel('Total Goals Scored', fontsize=16)
plt.title('Who is the most effective team in the Premier League?', fontsize= 20)
plt.show()






