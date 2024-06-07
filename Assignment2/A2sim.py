import simpy
import random

# Define constants for weather conditions
HIGH_TEMPERATURE = 24.5  # Upper range of high temperature in Celsius
MEDIUM_TEMPERATURE = 17.0  # Upper range of medium temperature in Celsius
LOW_TEMPERATURE = 11.7  # Upper range of low temperature in Celsius

HIGH_HUMIDITY = 100  # Upper range of high humidity in percentage
MEDIUM_HUMIDITY = 56.9  # Upper range of medium humidity in percentage
LOW_HUMIDITY = 43  # Upper range of low humidity in percentage

# Weather condition effect multipliers
TEMP_EFFECT_HIGH = 8  # High temperature increases time by 8 minutes
TEMP_EFFECT_MEDIUM = 4  # Medium temperature increases time by 4 minutes
HUMIDITY_EFFECT_HIGH = 2  # High humidity increases time by 2 minutes
HUMIDITY_EFFECT_MEDIUM = 1  # Medium humidity increases time by 1 minute

# Sample weather conditions
current_temperature = HIGH_TEMPERATURE
current_humidity = HIGH_HUMIDITY

# Define the environmental adjustment function
def calculate_weather_adjustment():
    adjustment = 0
    # Adjust for temperature
    if current_temperature > MEDIUM_TEMPERATURE:
        adjustment += TEMP_EFFECT_HIGH
    elif current_temperature > LOW_TEMPERATURE:
        adjustment += TEMP_EFFECT_MEDIUM
    
    # Adjust for humidity
    if current_humidity > MEDIUM_HUMIDITY:
        adjustment += HUMIDITY_EFFECT_HIGH
    elif current_humidity > LOW_HUMIDITY:
        adjustment += HUMIDITY_EFFECT_MEDIUM
    
    return adjustment

# Define storage capacities
WATER_STORAGE_CAPACITY = 10000
BATHROOM_STORAGE_CAPACITY = 10
ENERGY_STORAGE_CAPACITY = 1000
MEDICAL_STORAGE_CAPACITY = 5

# Initialize environment and resources
env = simpy.Environment()
water_storage = simpy.Resource(env, capacity=WATER_STORAGE_CAPACITY)
bathroom_storage = simpy.Resource(env, capacity=BATHROOM_STORAGE_CAPACITY)
energy_storage = simpy.Resource(env, capacity=ENERGY_STORAGE_CAPACITY)
medical_storage = simpy.Resource(env, capacity=MEDICAL_STORAGE_CAPACITY)

# Runner attributes
FULL_ENERGY = 100
FULL_THRIST = 100
FULL_HEALTH = 100

# Calculate the weather adjustment once
weather_adjustment = calculate_weather_adjustment()

def runner(env, name):
    energy = FULL_ENERGY
    thirst = FULL_THRIST
    health = FULL_HEALTH

    def advance(mean, std, phase):
        nonlocal energy, thirst, health
        base_time = random.normalvariate(mean, std)
        adjusted_time = base_time + (weather_adjustment / len(MEAN_TIMES))
        print(f'{name} is running phase {phase} for {adjusted_time:.2f} minutes (adjusted for weather).')
        energy -= 5
        thirst -= 10
        health -= 1
        yield env.timeout(adjusted_time)

    def try_drink():
        nonlocal thirst
        with water_storage.request() as req:
            yield req
            drink_time = random.uniform(0.33, 0.38)
            print(f'{name} is drinking water for {drink_time:.2f} minutes.')
            thirst = min(FULL_THRIST, thirst + 20)
            yield env.timeout(drink_time)

    def try_energy_drink():
        nonlocal energy
        with energy_storage.request() as req:
            yield req
            energy_time = random.uniform(0.33, 0.38)
            print(f'{name} is drinking an energy drink for {energy_time:.2f} minutes.')
            energy = min(FULL_ENERGY, energy + 30)
            yield env.timeout(energy_time)

    def try_bathroom():
        with bathroom_storage.request() as req:
            yield req
            bathroom_time = random.uniform(2, 2.3)
            print(f'{name} is using the bathroom for {bathroom_time:.2f} minutes.')
            yield env.timeout(bathroom_time)

    def try_medical():
        nonlocal health
        with medical_storage.request() as req:
            yield req
            medical_time = random.uniform(10, 11)
            print(f'{name} is receiving medical attention for {medical_time:.2f} minutes.')
            health = min(FULL_HEALTH, health + 20)
            yield env.timeout(medical_time)

    def check_prob(prob):
        return random.random() < prob

    # Initial phase - first 5 km
    yield from advance(MEAN_TIMES[0], STD_TIMES[0], 'first 5 km')
    if thirst < 80 and check_prob(0.5):  # 50% chance to stop if thirsty
        yield from try_drink()

    # Next 10 km
    yield from advance(MEAN_TIMES[1], STD_TIMES[1], 'next 10 km')
    if thirst < 80 and check_prob(0.5):  # 50% chance to stop if thirsty
        yield from try_drink()
    if energy < 70 and check_prob(0.4):  # 40% chance to stop if low on energy
        yield from try_energy_drink()
    if check_prob(NEEDS_BATHROOM_PROB):
        yield from try_bathroom()

    # Next 15 km
    yield from advance(MEAN_TIMES[2], STD_TIMES[2], 'next 15 km')
    if thirst < 80 and check_prob(0.5):
        yield from try_drink()
    if health < 90 and check_prob(0.2):  # 20% chance to stop if health is low
        yield from try_medical()

    # Next 5 km
    yield from advance(MEAN_TIMES[3], STD_TIMES[3], 'next 5 km')
    if thirst < 80 and check_prob(0.5):
        yield from try_drink()
    if energy < 70 and check_prob(0.4):
        yield from try_energy_drink()
    if check_prob(NEEDS_BATHROOM_PROB):
        yield from try_bathroom()

    # Next 5 km
    yield from advance(MEAN_TIMES[4], STD_TIMES[4], 'next 5 km')
    if thirst < 80 and check_prob(0.5):
        yield from try_drink()

    # Next 5 km
    yield from advance(MEAN_TIMES[5], STD_TIMES[5], 'next 5 km')
    if thirst < 80 and check_prob(0.5):
        yield from try_drink()
    if energy < 70 and check_prob(0.4):
        yield from try_energy_drink()
    if check_prob(NEEDS_BATHROOM_PROB):
        yield from try_bathroom()
    if health < 90 and check_prob(0.2):
        yield from try_medical()

    # Next 5 km
    yield from advance(MEAN_TIMES[6], STD_TIMES[6], 'next 5 km')
    if thirst < 80 and check_prob(0.5):
        yield from try_drink()

    # Next 5 km
    yield from advance(MEAN_TIMES[7], STD_TIMES[7], 'next 5 km')
    if thirst < 80 and check_prob(0.5):
        yield from try_drink()
    if energy < 70 and check_prob(0.4):
        yield from try_energy_drink()
    if check_prob(NEEDS_BATHROOM_PROB):
        yield from try_bathroom()

    # Final 2.195 km
    yield from advance(MEAN_TIMES[8], STD_TIMES[8], 'final 2.195 km')
    print(f'{name} has finished the marathon!')

# Define values for means and standard deviations
MEAN_TIMES = [17.87, 17.97, 18.25, 18.46, 18.36, 18.90, 19.74, 19.67, 8.77]
STD_TIMES = [1.09, 0.91, 1.10, 1.01, 1.07, 1.24, 1.97, 2.39, 0.99]

# Define probabilities
THIRSTY_PROB = 0.25
LOW_ENERGY_PROB = 0.3
NEEDS_BATHROOM_PROB = 0.2
NEEDS_MEDICAL_PROB = 0.03

# Generate runners at intervals of 10 with a spread of 3
for i in range(3):
    env.process(runner(env, f'Runner_{i+1}'))
    env.run(until=env.now + 10)

env.run()
