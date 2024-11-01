from demoparser2 import *
import pandas as pd
parser = DemoParser("C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\demos\ence-vs-astralis-m1-vertigo.dem")

pos = parser.parse_ticks(["X", "Y", "Z"])

pos.to_csv('pos.csv')