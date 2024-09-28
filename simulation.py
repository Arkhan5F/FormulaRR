import random
import datetime
from utils import display_starting_grid

# Tire compounds and their characteristics
tire_compounds = {
    'S': {'degradation': 0.3, 'speed': {'Dry': 1.0, 'Light Rain': 0.85, 'Heavy Rain': 0.7}, 'lifespan': 20},
    'M': {'degradation': 0.2, 'speed': {'Dry': 0.98, 'Light Rain': 0.88, 'Heavy Rain': 0.75}, 'lifespan': 30},
    'H': {'degradation': 0.1, 'speed': {'Dry': 0.96, 'Light Rain': 0.90, 'Heavy Rain': 0.8}, 'lifespan': 40},
    'I': {'degradation': 0.25, 'speed': {'Dry': 0.94, 'Light Rain': 1.0, 'Heavy Rain': 0.9}, 'lifespan': 25},
    'W': {'degradation': 0.15, 'speed': {'Dry': 0.92, 'Light Rain': 0.95, 'Heavy Rain': 1.0}, 'lifespan': 35}
}

dnf_reasons = [
    "crash",
    "collision with {}",
    "engine failure",
    "gearbox issue",
    "hydraulics problem",
    "brake failure",
    "tire puncture",
    "electrical issue",
    "fuel system problem",
    "suspension failure"
]


def run_qualification(track, drivers):
    print(f'Qualification for {track[0]}')
    base_time = track[1] - 0.5
    for driver in drivers:
        driver_performance = (driver[5] + driver[6]) / 100
        quali_performance = driver[9] / 100
        performance_factor = (driver_performance - 0.5) * 0.05 + (quali_performance - 0.5) * 0.05
        random_factor = random.random() * 0.2
        qual_time = base_time * (1 - performance_factor) + random_factor
        driver[3] = round(qual_time, 3)

    drivers.sort(key=lambda dr: dr[3])

    print("Qualification Results:")
    for position, driver in enumerate(drivers):
        gap = "pole" if position == 0 else f"+{(driver[3] - drivers[0][3]):.3f}"
        driver[8] = position + 1
        print(f'P{position + 1} {driver[0]} - {driver[1]} * Time: {driver[3]:.3f} ({gap})')


def initialize_race(track, drivers):
    weather = random.choice(['Dry', 'Light Rain', 'Heavy Rain'])
    pit_crew_busy = {driver[1]: 0 for driver in drivers}
    race_length = track[3]
    no_pit_window = max(5, int(race_length * 0.1))

    # Assign initial tires and display starting grid
    print(f"\nStarting Grid (Initial weather: {weather}):")
    for driver in drivers:
        initial_tire = choose_tire_compound(weather, 0, race_length)
        driver.append(initial_tire)
        driver.append(0)  # Laps on current tire
        driver.append([])  # List to store damage
        print(f"[START] {driver[8]} - {driver[0]} ({driver[-3]})")

    return weather, pit_crew_busy, race_length, no_pit_window, drivers

def check_weather_change(current_weather):
    if random.random() < 0.05:
        new_weather = random.choice(['Dry', 'Light Rain', 'Heavy Rain'])
        if new_weather != current_weather:
            return new_weather, f"Weather change: {new_weather} conditions!"
    return current_weather, None

def check_dnf(driver, race_length, drivers):
    if random.random() < driver[7] / (100 * race_length):
        driver[3] = 99999
        driver[4] = 9999
        dnf_reason = random.choice(dnf_reasons)
        if dnf_reason == "collision with {}":
            other_drivers = [d for d in drivers if d != driver and d[3] != 99999]
            if other_drivers:  # Check if there are any other drivers still in the race
                other_driver = random.choice(other_drivers)
                dnf_reason = dnf_reason.format(other_driver[0])
            else:
                dnf_reason = "collision with barrier"  # Fallback if no other drivers are available
        return f"DNF: {driver[0]} - {dnf_reason}"
    return None

def check_tire_puncture(driver):
    tire_age = driver[-1]
    tire_lifespan = tire_compounds[driver[-2]]['lifespan']
    puncture_chance = max(0, (tire_age - tire_lifespan) / 100)
    if random.random() < puncture_chance:
        driver[-1] = tire_lifespan  # Force a pit stop
        return f"PUNCTURE: {driver[0]} - Forced to pit"
    return None

def handle_pit_stop(driver, weather, laps_completed, race_length, pit_crew_busy):
    if pit_crew_busy[driver[1]] == 0:
        pit_time = random.uniform(20, 25)
        new_tire = choose_tire_compound(weather, laps_completed, race_length)
        pit_crew_busy[driver[1]] = 2
        driver[3] += pit_time
        driver[-2] = new_tire
        driver[-1] = 0
        return f"PIT: {driver[0]} {driver[-2]} -> {new_tire}, Stop: {pit_time:.2f}s"

def calculate_lap_time(driver, track, weather):
    # Calculate lap time
    base_lap_time = track[1] + (track[2] - track[1]) / 2
    driver_adjust = (driver[5] + driver[6]) / 100
    tire_speed = tire_compounds[driver[-3]]['speed'][weather]
    tire_deg = tire_compounds[driver[-3]]['degradation'] * driver[-2]
    old_tire_penalty = max(0, (driver[-2] - tire_compounds[driver[-3]]['lifespan']) * 0.01)

    damage_penalty = 0
    for damage in driver[-1]:
        if damage.startswith('unfixable'):
            damage_penalty += random.uniform(0.5,
                                             1.5)  # 0.5 to 1.5 seconds penalty per lap for each unfixable damage
        elif damage == 'front_wing':
            front_wing_penalty = random.uniform(0.3,
                                                0.7)  # 0.3 to 0.7 seconds penalty per lap for damaged front wing
            damage_penalty += front_wing_penalty

    lap_time = base_lap_time * (1 - driver_adjust) * tire_speed * (1 + tire_deg) * (
                1 + old_tire_penalty) + damage_penalty
    driver[3] += lap_time
    driver[-2] += 1  # Increment laps on current tire


def process_overtakes(drivers, previous_order):
    overtakes = []
    for new_pos, driver in enumerate(drivers):
        if driver[3] == 99999:  # Skip DNF'd drivers
            continue
        old_pos = previous_order.index(driver)
        if new_pos < old_pos:
            for overtaken in previous_order[new_pos:old_pos]:
                if overtaken[3] != 99999:  # Ensure overtaken driver hasn't DNF'd
                    overtakes.append((driver, overtaken, new_pos + 1, old_pos + 1))
    return overtakes

def generate_overtake_messages(overtakes):
    overtake_summary = {}
    for overtaker, overtaken, new_pos, old_pos in overtakes:
        if new_pos <= 10 or old_pos <= 10:  # Only consider overtakes involving top 10 positions
            if overtaker[0] not in overtake_summary:
                overtake_summary[overtaker[0]] = {'start': old_pos, 'end': new_pos, 'passed': []}
            overtake_summary[overtaker[0]]['end'] = new_pos
            overtake_summary[overtaker[0]]['passed'].append(overtaken[0])

    messages = []
    for driver, summary in overtake_summary.items():
        if summary['start'] != summary['end']:
            passed_drivers = ', '.join(summary['passed'])
            if summary['end'] <= 3 or summary['start'] <= 3:
                messages.append(f"MAJOR OVERTAKE: {driver} gained {summary['start'] - summary['end']} "
                                f"positions (P{summary['start']} -> P{summary['end']}), "
                                f"passing {passed_drivers}")
            else:
                messages.append(f"OVERTAKE: {driver} gained {summary['start'] - summary['end']} "
                                f"positions (P{summary['start']} -> P{summary['end']}), "
                                f"passing {passed_drivers}")
    return messages


def check_driver_error(driver, weather):
    error_chance = 0.01 * (1 + (0.5 if weather != 'Dry' else 0))  # Increased chance in wet conditions
    if random.random() < error_chance:
        error_type = random.choices(['wide', 'fixable_damage', 'unfixable_damage'],
                                    weights=[0.7, 0.2, 0.1])[0]
        time_loss = random.uniform(1, 5)

        if error_type == 'wide':
            return f"ERROR: {driver[0]} went wide, losing {time_loss:.2f} seconds", time_loss, None
        elif error_type == 'fixable_damage':
            return f"ERROR: {driver[0]} damaged front wing, losing {time_loss:.2f} seconds", time_loss, 'front_wing'
        else:
            part = random.choice(['rear wing', 'floor', 'sidepods'])
            return f"ERROR: {driver[0]} damaged {part}, losing {time_loss:.2f} seconds", time_loss, f'unfixable_{part}'
    return None, 0, None


def check_collision(driver1, driver2):
    collision_chance = 0.001  # Adjust as needed
    if random.random() < collision_chance:
        time_loss = random.uniform(5, 15)
        dnf_chance = 0.3  # 30% chance of DNF for each driver

        outcomes = []
        for driver in [driver1, driver2]:
            if random.random() < dnf_chance:
                outcomes.append(
                    (f"DNF: {driver[0]} - Collision with {driver1[0] if driver == driver2 else driver2[0]}", 'DNF'))
            else:
                damage_type = random.choice(['none', 'fixable', 'unfixable'])
                if damage_type == 'none':
                    outcomes.append((f"COLLISION: {driver[0]} lost {time_loss:.2f} seconds", 'time_loss'))
                elif damage_type == 'fixable':
                    outcomes.append(
                        (f"COLLISION: {driver[0]} damaged front wing, losing {time_loss:.2f} seconds", 'front_wing'))
                else:
                    part = random.choice(['rear wing', 'floor', 'sidepods'])
                    outcomes.append(
                        (f"COLLISION: {driver[0]} damaged {part}, losing {time_loss:.2f} seconds", f'unfixable_{part}'))

        return outcomes, time_loss
    return None, 0


def run_race(track, drivers):
    print(f'\n{"=" * 50}\nRace: {track[0]} - {track[3]} Laps\n{"=" * 50}')

    # Initialize race conditions
    weather, pit_crew_busy, race_length, no_pit_window, drivers = initialize_race(track, drivers)
    laps_completed = 0


    print(f'\n{"=" * 50}\nRace Start\n{"=" * 50}')

    previous_order = drivers.copy()

    while laps_completed < race_length:
        laps_completed += 1
        lap_events = []

        # Weather change
        if random.random() < 0.05:
            new_weather = random.choice(['Dry', 'Light Rain', 'Heavy Rain'])
            if new_weather != weather:
                weather = new_weather
                lap_events.append(f"Weather change: {weather} conditions!")

        for i, driver in enumerate(drivers):
            if driver[3] == 99999:  # Driver has already DNF'd
                continue

            # Check for driver error
            error_event, error_time_loss, damage = check_driver_error(driver, weather)
            if error_event:
                lap_events.append(error_event)
                driver[3] += error_time_loss
                if damage:
                    driver[-1].append(damage)

            # Check for collision with nearby drivers
            for other_driver in drivers[max(0, i - 1):i] + drivers[i + 1:min(len(drivers), i + 2)]:
                if other_driver[3] != 99999:
                    collision_outcomes, collision_time_loss = check_collision(driver, other_driver)
                    if collision_outcomes:
                        for outcome, outcome_type in collision_outcomes:
                            lap_events.append(outcome)
                            if outcome_type == 'DNF':
                                if outcome.startswith(f"DNF: {driver[0]}"):
                                    driver[3] = 99999
                                else:
                                    other_driver[3] = 99999
                            elif outcome_type == 'time_loss':
                                if outcome.startswith(f"COLLISION: {driver[0]}"):
                                    driver[3] += collision_time_loss
                                else:
                                    other_driver[3] += collision_time_loss
                            else:
                                if outcome.startswith(f"COLLISION: {driver[0]}"):
                                    driver[-1].append(outcome_type)
                                else:
                                    other_driver[-1].append(outcome_type)

            if driver[3] == 99999:  # If driver DNF'd due to collision, skip to next driver
                continue

            # Check for DNF
            if random.random() < driver[7] / (100 * race_length):
                driver[3] = 99999
                driver[4] = 9999
                dnf_reason = random.choice(dnf_reasons)
                if dnf_reason == "collision with {}":
                    other_driver = random.choice([d for d in drivers if d != driver and d[3] != 99999])
                    dnf_reason = dnf_reason.format(other_driver[0])
                lap_events.append(f"DNF: {driver[0]} - {dnf_reason}")
                continue

            # Check for tire puncture
            tire_age = driver[-2]
            tire_lifespan = tire_compounds[driver[-3]]['lifespan']
            puncture_chance = max(0, (tire_age - tire_lifespan) / 100)
            if random.random() < puncture_chance:
                lap_events.append(f"PUNCTURE: {driver[0]} - Forced to pit")
                driver[-2] = tire_lifespan  # Force a pit stop

            # Decide if driver needs to pit
            laps_remaining = race_length - laps_completed
            needs_to_pit = (
                    laps_remaining > no_pit_window and
                    ((weather == 'Heavy Rain' and driver[-3] != 'W') or
                     (weather == 'Light Rain' and driver[-3] not in ['I', 'W']) or
                     (weather == 'Dry' and driver[-3] in ['I', 'W']) or
                     (driver[-2] >= tire_compounds[driver[-3]]['lifespan'] and
                      random.random() < 0.7 * (laps_remaining / race_length)) or
                     'front_wing' in driver[-1])
            )

            if needs_to_pit:
                if pit_crew_busy[driver[1]] == 0:
                    pit_time = random.uniform(20, 25)
                    new_tire = choose_tire_compound(weather, laps_completed, race_length)

                    if 'front_wing' in driver[-1]:
                        pit_time += random.uniform(5, 10)  # Additional time for front wing change
                        driver[-1].remove('front_wing')
                        lap_events.append(
                            f"PIT: {driver[0]} changed front wing and tires {driver[-3]} -> {new_tire}, Stop: {pit_time:.2f}s")
                    else:
                        lap_events.append(f"PIT: {driver[0]} {driver[-3]} -> {new_tire}, Stop: {pit_time:.2f}s")

                    driver[3] += pit_time
                    driver[-3] = new_tire
                    driver[-2] = 0
                    pit_crew_busy[driver[1]] = 2
                else:
                    lap_events.append(f"{driver[0]} needs to pit but crew is busy")

            # Calculate lap time
            base_lap_time = track[1] + (track[2] - track[1]) / 2
            driver_adjust = (driver[5] + driver[6]) / 100
            tire_speed = tire_compounds[driver[-3]]['speed'][weather]
            tire_deg = tire_compounds[driver[-3]]['degradation'] * driver[-2]
            old_tire_penalty = max(0, (driver[-2] - tire_compounds[driver[-3]]['lifespan']) * 0.01)

            damage_penalty = 0
            for damage in driver[-1]:
                if damage.startswith('unfixable'):
                    damage_penalty += random.uniform(0.5,
                                                     1.5)  # 0.5 to 1.5 seconds penalty per lap for each unfixable damage

            lap_time = base_lap_time * (1 - driver_adjust) * tire_speed * (1 + tire_deg) * (
                        1 + old_tire_penalty) + damage_penalty
            driver[3] += lap_time
            driver[-2] += 1  # Increment laps on current tire

        # Sort drivers by race time and check for overtakes
        drivers.sort(key=lambda dr: dr[3])

        overtakes = []
        for new_pos, driver in enumerate(drivers):
            if driver[3] == 99999:  # Skip DNF'd drivers
                continue
            old_pos = previous_order.index(driver)
            if new_pos < old_pos:
                for overtaken in previous_order[new_pos:old_pos]:
                    if overtaken[3] != 99999:  # Ensure overtaken driver hasn't DNF'd
                        overtakes.append((driver, overtaken, new_pos + 1, old_pos + 1))

        # Process overtakes and generate messages for top 10
        overtake_summary = {}
        for overtaker, overtaken, new_pos, old_pos in overtakes:
            if new_pos <= 10 or old_pos <= 10:  # Only consider overtakes involving top 10 positions
                if overtaker[0] not in overtake_summary:
                    overtake_summary[overtaker[0]] = {'start': old_pos, 'end': new_pos, 'passed': []}
                overtake_summary[overtaker[0]]['end'] = new_pos
                overtake_summary[overtaker[0]]['passed'].append(overtaken[0])

        # Generate lap events from the summary
        for driver, summary in overtake_summary.items():
            if summary['start'] != summary['end']:
                passed_drivers = ', '.join(summary['passed'])
                if summary['end'] <= 3 or summary['start'] <= 3:
                    lap_events.append(f"MAJOR OVERTAKE: {driver} gained {summary['start'] - summary['end']} "
                                      f"positions (P{summary['start']} -> P{summary['end']}), "
                                      f"passing {passed_drivers}")
                else:
                    lap_events.append(f"OVERTAKE: {driver} gained {summary['start'] - summary['end']} "
                                      f"positions (P{summary['start']} -> P{summary['end']}), "
                                      f"passing {passed_drivers}")

        previous_order = drivers.copy()

        # Decrement pit crew busy counters
        for team in pit_crew_busy:
            if pit_crew_busy[team] > 0:
                pit_crew_busy[team] -= 1

        # Print lap events
        if lap_events:
            print(f"\n[LAP {laps_completed}]")
            for event in lap_events:
                print(event)

        if laps_completed % 10 == 0:
            print(f"\n[LAP {laps_completed}/{race_length}] Race Progress (Weather: {weather})")
            for position, driver in enumerate(drivers[:3], 1):
                if driver[3] != 99999:
                    print(f"P{position}: {driver[0]} ({driver[-3]}, {driver[-2]} laps old)")

    print(f'\n{"=" * 50}\nRace Finish\n{"=" * 50}')
    print("\nFinal Results:")
    for position, driver in enumerate(drivers, 1):
        if driver[3] == 99999:
            format_time = 'DNF'
        else:
            format_time = str(datetime.timedelta(seconds=round(driver[3], 3)))[:-3]
        print(f'P{position} {driver[0]} - {driver[1]} * Time: {format_time} (Started: P{driver[8]})')

    allocate_points(drivers)

def print_race_results(drivers):
    print(f'\n{"=" * 50}\nRace Finish\n{"=" * 50}')
    print("\nFinal Results:")
    for position, driver in enumerate(drivers, 1):
        if driver[3] == 99999:
            format_time = 'DNF'
        else:
            format_time = str(datetime.timedelta(seconds=round(driver[3], 3)))[:-3]
        print(f'P{position} {driver[0]} - {driver[1]} * Time: {format_time} (Started: P{driver[8]})')


def choose_tire_compound(weather, laps_completed, race_length):
    laps_remaining = race_length - laps_completed
    if weather == 'Heavy Rain':
        return 'W'
    elif weather == 'Light Rain':
        return 'I'
    else:  # Dry
        if laps_remaining > 30:
            return random.choice(['M', 'H'])
        elif laps_remaining > 15:
            return random.choice(['S', 'M'])
        else:
            return 'S'


def allocate_points(drivers):
    points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    for position, point in enumerate(points):
        if position < len(drivers) and drivers[position][3] != 99999:
            drivers[position][2] += point

    fastest_lap_driver = min((driver for driver in drivers[:min(10, len(drivers))] if driver[3] != 99999),
                             key=lambda dr: dr[4])
    fastest_lap_driver[2] += 1
    print(f'** Fastest Lap(+1 point): {fastest_lap_driver[0]} - {fastest_lap_driver[4]}')

    drivers.sort(key=lambda dr: dr[2], reverse=True)

    print('-------------------')
    print('STANDINGS - Points:')
    for position, driver in enumerate(drivers):
        print(f'{position + 1}. {driver[0]} - {driver[1]} - Points: {driver[2]}')