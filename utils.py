import json

def save_progress(file_name, drivers, tracks, current_race, is_qualification):
    with open(file_name, 'w') as f:
        json.dump({
            'drivers': drivers,
            'tracks': tracks,
            'current_race': current_race,
            'is_qualification': is_qualification
        }, f)

def display_starting_grid(drivers):
    print("\nStarting Grid:")
    sorted_drivers = sorted(drivers, key=lambda d: d[8])
    for driver in sorted_drivers:
        print(f'P{driver[8]} {driver[0]} - {driver[1]}')
    print("\n")

def display_standings(drivers):
    print('=================')
    print('F1 Season Results')
    print(f'Winner: {drivers[0][0]} - {drivers[0][1]} : {drivers[0][2]} Points')
    for position, driver in enumerate(drivers[1:]):
        print(f'#{position + 2}. {driver[0]} - {driver[1]} : {driver[2]} Points')