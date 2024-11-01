from demoparser2 import DemoParser
import csv
file_loc = "D:\demos\csc\s15-M09-SaltyScripters-vs-SirloinSizzlers-mid4924-0_de_dust2-2024-10-25_02-09-01.dem"
parser = DemoParser(file_loc)

# If you just want the names of all events then you can use this:
event_names = parser.list_game_events()

# Currently the event "all" gives you all events. Cursed solution for now
df = parser.parse_event("round_start")
df2 = parser.parse_events(["all"])

print(df)
# for i in range(len(df2)):
#     print(df2[i])