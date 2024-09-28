import json
import os
from data import initialize_data
from simulation import run_qualification, run_race
from utils import save_progress, display_standings

print('**** Formula 1 Simulation  **** ')

# File to save progress
SAVE_FILE = 'f1_simulation_progress.json'

# Load progress if exists
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
        drivers = data['drivers']
        tracks = data['tracks']
        current_race = data['current_race']
        is_qualification = data['is_qualification']
else:
    drivers, tracks, current_race, is_qualification = initialize_data()

print(f'** {len(tracks)} Race F1 Season Simulation with {len(drivers)} Drivers **')

# Run qualification or race
if current_race < len(tracks):
    track = tracks[current_race]

    if is_qualification:
        run_qualification(track, drivers)
        is_qualification = False
    else:
        run_race(track, drivers)
        is_qualification = True
        current_race += 1

    save_progress(SAVE_FILE, drivers, tracks, current_race, is_qualification)

else:
    display_standings(drivers)