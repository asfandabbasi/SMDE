import simpy
import random

# Define constants for weather conditions
HIGH_TEMPERATURE = 24.5
LOW_TEMPERATURE = 11.7
HIGH_HUMIDITY = 100
LOW_HUMIDITY = 43

# Weather condition effect multipliers
TEMP_EFFECT_HIGH = 8
TEMP_EFFECT_MEDIUM = 4
HUMIDITY_EFFECT_HIGH = 2
HUMIDITY_EFFECT_MEDIUM = 1

# Function to calculate the environmental adjustment based on temperature and humidity
def calculate_weather_adjustment(temp, hum):
    adjustment = 0
    if temp == 'H':
        adjustment += TEMP_EFFECT_HIGH
    else:
        adjustment += TEMP_EFFECT_MEDIUM
    
    if hum == 'H':
        adjustment += HUMIDITY_EFFECT_HIGH
    else:
        adjustment += HUMIDITY_EFFECT_MEDIUM
    
    return adjustment

# Initialize environment and resources
def init_environment(water_capacity, toilet_capacity, energy_capacity, medical_capacity):
    env = simpy.Environment()
    water_storage = simpy.Resource(env, capacity=water_capacity)  # Adjustable capacity for storage
    bathroom_storage = simpy.Resource(env, capacity=toilet_capacity)  # Adjustable capacity for storage
    energy_storage = simpy.Resource(env, capacity=energy_capacity)  
    medical_storage = simpy.Resource(env, capacity=medical_capacity)  
    return env, water_storage, bathroom_storage, energy_storage, medical_storage

# Runner attributes
FULL_ENERGY = 100
FULL_THRIST = 100
FULL_HEALTH = 100
FULL_TOILET = 100

# Global dictionary to store counters for each experiment
experiment_counters = {}

def reset_counters():
    return {
        "water_station_counter": 0,
        "energy_station_counter": 0,
        "bathroom_station_counter": 0,
        "medical_station_counter": 0,
    }

def runner(env, name, weather_adjustment, counters, water_storage, bathroom_storage, energy_storage, medical_storage):
    energy = FULL_ENERGY
    thirst = FULL_THRIST
    health = FULL_HEALTH
    toilet = FULL_TOILET
    total_time = 0
    distance_since_last_water = 0
    distance_since_last_toilet = 0

    def advance(mean, std, phase, distance):
        nonlocal energy, thirst, health, total_time, distance_since_last_water, distance_since_last_toilet, toilet
        base_time = random.normalvariate(mean, std)
        adjusted_time = base_time + (weather_adjustment / len(MEAN_TIMES))
        energy -= random.normalvariate( 5, 2)
        health -= random.normalvariate(0.5, 1)
        # Thirst reduction based on distance since last water station
        thirst_reduction = min(distance_since_last_water * 2, 20)  # Thirst reduction function
        thirst -= thirst_reduction
        # Toilet reduction based on distance since last toilet station
        toilet_reduction = min(distance_since_last_toilet * 2, 20)  # Toilet reduction function
        toilet -= toilet_reduction
        total_time += adjusted_time
        distance_since_last_water += distance
        distance_since_last_toilet += distance
        yield env.timeout(adjusted_time)

    def try_drink():
        nonlocal thirst, distance_since_last_water, total_time
        with water_storage.request() as req:
            start_wait = env.now
            yield req
            wait_time = env.now - start_wait
            total_time += wait_time
            counters["water_station_counter"] += 1
            drink_time = abs(random.normalvariate(1, 2))
            thirst = min(FULL_THRIST, thirst + 40)
            distance_since_last_water = 0
            yield env.timeout(drink_time)

    def try_energy_drink():
        nonlocal energy, total_time
        with energy_storage.request() as req:
            start_wait = env.now
            yield req
            wait_time = env.now - start_wait
            total_time += wait_time
            counters["energy_station_counter"] += 1
            energy_time = abs(random.normalvariate(1, 2))
            energy = min(FULL_ENERGY, energy + 40)
            yield env.timeout(energy_time)

    def try_bathroom():
        nonlocal distance_since_last_toilet, toilet, total_time
        with bathroom_storage.request() as req:
            start_wait = env.now
            yield req
            wait_time = env.now - start_wait
            total_time += wait_time
            counters["bathroom_station_counter"] += 1
            bathroom_time = abs(random.normalvariate(5, 10))
            toilet = min(FULL_TOILET, toilet + 40)
            distance_since_last_toilet = 0
            yield env.timeout(bathroom_time)

    def try_medical():
        nonlocal health, total_time
        with medical_storage.request() as req:
            start_wait = env.now
            yield req
            wait_time = env.now - start_wait
            total_time += wait_time
            counters["medical_station_counter"] += 1
            medical_time = abs(random.normalvariate(15, 20))
            health = min(FULL_HEALTH, health + 50)
            yield env.timeout(medical_time)


    phases = [
        {"distance": 5, "mean": MEAN_TIMES[0], "std": STD_TIMES[0]},
        {"distance": 10, "mean": MEAN_TIMES[1], "std": STD_TIMES[1]},
        {"distance": 15, "mean": MEAN_TIMES[2], "std": STD_TIMES[2]},
        {"distance": 20, "mean": MEAN_TIMES[3], "std": STD_TIMES[3]},
        {"distance": 25, "mean": MEAN_TIMES[4], "std": STD_TIMES[4]},
        {"distance": 30, "mean": MEAN_TIMES[5], "std": STD_TIMES[5]},
        {"distance": 35, "mean": MEAN_TIMES[6], "std": STD_TIMES[6]},
        {"distance": 40, "mean": MEAN_TIMES[7], "std": STD_TIMES[7]},
        {"distance": 42.195, "mean": MEAN_TIMES[8], "std": STD_TIMES[8]},
    ]

    for phase in phases:
        yield from advance(phase["mean"], phase["std"], f'{phase["distance"]} km', 5)
        
        thirst_modifier = (FULL_THRIST - thirst) / FULL_THRIST
        energy_modifier = (FULL_ENERGY - energy) / FULL_ENERGY
        health_modifier = (FULL_HEALTH - health) / FULL_HEALTH
        toilet_modifier = (FULL_TOILET - toilet) / FULL_TOILET

        if phase["distance"] % 5 == 0 and check_prob(0.4, thirst_modifier):
            yield from try_drink()
        if phase["distance"] % 20 == 0 and check_prob(0.2, energy_modifier):
            yield from try_energy_drink()
        if phase["distance"] % 10 == 0 and check_prob(0.2, toilet_modifier):
            yield from try_bathroom()
        if phase["distance"] % 15 == 0 and check_prob(0.3, health_modifier):
            yield from try_medical()

    total_times.append(total_time)

# Define values for means and standard deviations
MEAN_TIMES = [17.87, 17.97, 18.25, 18.46, 18.36, 18.90, 19.74, 19.67, 8.77]
STD_TIMES = [1.09, 0.91, 1.10, 1.01, 1.07, 1.24, 1.97, 2.39, 0.99]

# Define the check_prob function
def check_prob(base_prob, modifier):
    return random.random() < base_prob * modifier

# Design of Experiments (DOE) setup
num_runners = 100
water_capacity_per_runner = 0.05  # Example: 5 liters per 1000 runners
toilet_capacity_per_runner = 0.025  # Example: 2.5 units per 1000 runners
energy_capacity = num_runners * 0.1  # Example: 100 units per 1000 runners
medical_capacity = num_runners * 0.05  # Example: 50 units per 1000 runners

experiments = [
    {'temp': 'L', 'hum': 'L', 'water_capacity': int(num_runners * water_capacity_per_runner), 'toilet_capacity': int(num_runners * toilet_capacity_per_runner)},
    {'temp': 'L', 'hum': 'L', 'water_capacity': int(num_runners * 1.5 * water_capacity_per_runner), 'toilet_capacity': int(num_runners * 1.5 * toilet_capacity_per_runner)},
    {'temp': 'L', 'hum': 'H', 'water_capacity': int(num_runners * water_capacity_per_runner), 'toilet_capacity': int(num_runners * 1.5 * toilet_capacity_per_runner)},
    {'temp': 'L', 'hum': 'H', 'water_capacity': int(num_runners * 1.5 * water_capacity_per_runner), 'toilet_capacity': int(num_runners * toilet_capacity_per_runner)},
    {'temp': 'H', 'hum': 'L', 'water_capacity': int(num_runners * water_capacity_per_runner), 'toilet_capacity': int(num_runners * 1.5 * toilet_capacity_per_runner)},
    {'temp': 'H', 'hum': 'L', 'water_capacity': int(num_runners * 1.5 * water_capacity_per_runner), 'toilet_capacity': int(num_runners * toilet_capacity_per_runner)},
    {'temp': 'H', 'hum': 'H', 'water_capacity': int(num_runners * water_capacity_per_runner), 'toilet_capacity': int(num_runners * toilet_capacity_per_runner)},
    {'temp': 'H', 'hum': 'H', 'water_capacity': int(num_runners * 1.5 * water_capacity_per_runner), 'toilet_capacity': int(num_runners * 1.5 * toilet_capacity_per_runner)}
]

# To track the total times of all runners across experiments
all_total_times = []

# Run the experiments
for exp_index, exp in enumerate(experiments):
    print(f"Running experiment with temp={exp['temp']}, hum={exp['hum']}, water capacity {exp['water_capacity']} units, toilet capacity {exp['toilet_capacity']} units")
    total_times = []
    counters = reset_counters()
    env, water_storage, bathroom_storage, energy_storage, medical_storage = init_environment(exp['water_capacity'], exp['toilet_capacity'], energy_capacity, medical_capacity)
    weather_adjustment = calculate_weather_adjustment(exp['temp'], exp['hum'])
    
    for i in range(num_runners):  # Number of runners
        env.process(runner(env, f'Runner_{i+1}', weather_adjustment, counters, water_storage, bathroom_storage, energy_storage, medical_storage))
    env.run()
    
    experiment_counters[exp_index] = counters
    all_total_times.append((exp, total_times))

# Calculate and print average times and station usage
for i, (exp, times) in enumerate(all_total_times):
    average_time = sum(times) / len(times)
    print(f'Experiment {i+1} with temp={exp["temp"]}, hum={exp["hum"]}, water capacity {exp["water_capacity"]} units, toilet capacity {exp["toilet_capacity"]} units average time: {average_time:.2f} minutes')
    counters = experiment_counters[i]
    print(f'Water station usage: {counters["water_station_counter"]}')
    print(f'Energy drink station usage: {counters["energy_station_counter"]}')
    print(f'Bathroom usage: {counters["bathroom_station_counter"]}')
    print(f'Medical station usage: {counters["medical_station_counter"]}')
