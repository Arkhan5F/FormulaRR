def initialize_data():
    # Drivers: [Name, Team, Points, Last race time, Fastest lap, Skill, Car performance, DNF%, Grid Position, Quali Performance]
    drivers = [
        ['Max Verstappen', 'Red Bull', 0, 0, 0, 28, 16, 18, 0, 95],
        ['Sergio Pérez', 'Red Bull', 0, 0, 0, 15, 16, 13, 0, 82],
        ['Lewis Hamilton', 'Mercedes', 0, 0, 0, 28, 15, 12, 0, 90],
        ['George Russell', 'Mercedes', 0, 0, 0, 24, 15, 7, 0, 92],
        ['Charles Leclerc', 'Ferrari', 0, 0, 0, 23, 15, 18, 0, 94],
        ['Carlos Sainz Jr.', 'Ferrari', 0, 0, 0, 14, 15, 18, 0, 88],
        ['Lando Norris', 'McLaren', 0, 0, 0, 19, 12, 18, 0, 91],
        ['Oscar Piastri', 'McLaren', 0, 0, 0, 15, 12, 15, 0, 85],
        ['Fernando Alonso', 'Aston Martin', 0, 0, 0, 22, 12, 15, 0, 89],
        ['Lance Stroll', 'Aston Martin', 0, 0, 0, 10, 12, 17, 0, 80],
        ['Pierre Gasly', 'Alpine', 0, 0, 0, 18, 10, 18, 0, 86],
        ['Esteban Ocon', 'Alpine', 0, 0, 0, 17, 10, 13, 0, 84],
        ['Alexander Albon', 'Williams', 0, 0, 0, 16, 8, 13, 0, 87],
        ['Logan Sargeant', 'Williams', 0, 0, 0, 8, 8, 15, 0, 75],
        ['Yuki Tsunoda', 'RB', 0, 0, 0, 14, 9, 18, 0, 83],
        ['Daniel Ricciardo', 'RB', 0, 0, 0, 19, 9, 18, 0, 85],
        ['Valtteri Bottas', 'Sauber', 0, 0, 0, 20, 7, 14, 0, 86],
        ['Zhou Guanyu', 'Sauber', 0, 0, 0, 13, 7, 14, 0, 81],
        ['Kevin Magnussen', 'Haas', 0, 0, 0, 16, 7, 14, 0, 82],
        ['Nico Hulkenberg', 'Haas', 0, 0, 0, 18, 7, 16, 0, 84]
    ]

    # Track: [Name, Lap Record & Avg lap time in secs, # Laps]
    tracks = [['Monaco GP', 74.26, 78.62, 78],
              ['French GP - Le Castellet', 92.74, 98.46, 53],
              ['Austrian GP - Red Bull Ring', 65.62, 70.69, 71],
              ['British GP - Silverstone', 87.1, 93.46, 52],
              ['Belgian GP - Spa', 106.29, 111.68, 44],
              ['Italian GP - Monza', 81.05, 87.37, 53],
              ['Singapore GP - Marina Bay', 101.91, 107.00, 61],
              ['Brazilian GP - Interlagos', 70.54, 72.92, 71]]

    current_race = 0
    is_qualification = True

    return drivers, tracks, current_race, is_qualification
