from demoparser2 import *
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



try:
    os.remove('positions.csv')
except Exception as e:
    print(e)

#insert .demo file here
file_loc = "C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\demos\sharks-vs-pain-m1-vertigo.dem"
freeze_time = 20
tickspeed = 64

parser = DemoParser(file_loc)
max_tick = parser.parse_event("round_end")["tick"].max()
details = parser.parse_header()
mapname = details['map_name']

image_path = f"icons/maps/{mapname}.png"
img = plt.imread(image_path)

game_data = ['total_rounds_played']
finalGameData = parser.parse_ticks(game_data,ticks=[max_tick])

roundStartDF = parser.parse_event("round_start")
roundStartDF.drop_duplicates(subset='round',keep='last',inplace=True)
roundStartDF['tick'] = roundStartDF['tick'] + (tickspeed * freeze_time)
roundStartTick = roundStartDF['tick'].tolist()

pos_wanted_props = ['X','Y','Z','team_name']
masterDF = pd.DataFrame()

for roundNumStartTick in range(len(roundStartTick)):
    currentTickPos = parser.parse_ticks(pos_wanted_props, ticks=[roundStartTick[roundNumStartTick]])
    masterDF = pd.concat([masterDF, currentTickPos])
    print('Round: ' + str(roundNumStartTick))
    for openingPos in range(0,1000,64):
        currentTickPos = parser.parse_ticks(pos_wanted_props, ticks=[roundStartTick[roundNumStartTick]+openingPos])
        masterDF = pd.concat([masterDF, currentTickPos])
        
masterDF.to_csv('positions.csv')

ct_color = '#68a3e5'
terrorist_color = '#e6f13d'

fig, ax = plt.subplots()
ax.imshow(img, extent=[masterDF['X'].min(), masterDF['X'].max(), masterDF['Y'].min(), masterDF['Y'].max()], aspect='auto')
scat = ax.scatter([], [], s=10)
ax.set_xlim(masterDF['X'].min() - 10, masterDF['X'].max() + 10)
ax.set_ylim(masterDF['Y'].min() - 10, masterDF['Y'].max() + 10)

def animate(i):
    tick_data = masterDF[masterDF['tick'] == i]
    tick_colors = [ct_color if team == 'CT' else terrorist_color for team in tick_data['team_name']]
    scat.set_offsets(tick_data[['X', 'Y']].values)
    scat.set_color(tick_colors) 
    return scat,

ani = FuncAnimation(fig, animate, frames=masterDF['tick'].unique(), interval=100, blit=True)


plt.show()



