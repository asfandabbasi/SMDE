import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the dataset
runner_data = pd.read_csv('Assignment2/marathon_results_2015.csv')
# Convert completion time to minutes with error handling
time_columns = ['Official Time', '5K', '10K', '15K', '20K', 'Half', '25K', '30K', '35K', '40K']
for col in time_columns:
    runner_data[col] = pd.to_timedelta(runner_data[col], errors='coerce').dt.total_seconds() / 60

# Drop rows with NaN values in any of the time columns
runner_data.dropna(subset=time_columns, inplace=True)

# Assume the first digit of the Bib number indicates runner level
# Example: Bib number 1-999 for elite, 1000-4999 for recreational, 5000+ for occasional
def get_runner_level(bib):
    # Convert to integer, if not number or cannot be converted, skip
    try:
        bib = int(bib)
    except:
        return 'Unknown'
    if bib < 50:
        return 'Elite'
    elif bib < 300:
        return 'Recreational'
    else:
        return 'Occasional'

runner_data['Runner Level'] = runner_data['Bib'].apply(get_runner_level)
adult_runners = runner_data[(runner_data['Age'] >= 30) & (runner_data['Age'] <= 35)]

adult_recreational_runners = adult_runners[adult_runners['Runner Level'] == 'Recreational']

# Check the normality of completion times
completion_times = adult_recreational_runners['Official Time']

# Visual inspection
sns.histplot(completion_times, kde=True)
plt.title('Histogram of Completion Times')
plt.show()

# Q-Q plot
stats.probplot(completion_times, dist="norm", plot=plt)
plt.title('Q-Q Plot')
plt.show()

# Normality tests
shapiro_test = stats.shapiro(completion_times)
ks_test = stats.kstest(completion_times, 'norm')

print('Shapiro-Wilk Test:', shapiro_test)
print('Kolmogorov-Smirnov Test:', ks_test)



# Define a function to create and evaluate a linear regression model for each distance
def linear_regression_for_distance(df, distance_column):
    X = df[[distance_column]]
    y = df['Official Time']
    
    # Fit the model
    model = LinearRegression()
    model.fit(X, y)
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Evaluate the model
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    # Print model summary
    print(f"Distance: {distance_column}")
    print(f"Coefficients: {model.coef_}")
    print(f"Intercept: {model.intercept_}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print("\n")
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Actual Time')
    plt.plot(X, y_pred, color='red', linewidth=2, label='Predicted Time')
    plt.title(f'Linear Regression for {distance_column}')
    plt.xlabel(f'{distance_column} Time (minutes)')
    plt.ylabel('Official Time (minutes)')
    plt.legend()
    plt.show()

# List of distance columns
distances = ['5K', '10K', '15K', '20K', 'Half', '25K', '30K', '35K', '40K']


def linear_regression_to_predict_time(df, distance_column):
    # Generate a feature for the distance in kilometers
    distance_values = {
        '5K': 5, '10K': 10, '15K': 15, '20K': 20, 
        'Half': 21.0975, '25K': 25, '30K': 30, 
        '35K': 35, '40K': 40
    }
    X = pd.DataFrame({'Distance': [distance_values[distance_column]] * df.shape[0]})
    y = df[distance_column]
    
    # Fit the model
    model = LinearRegression()
    model.fit(X, y)
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Evaluate the model
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    # Print model summary
    print(f"Distance: {distance_column}")
    print(f"Coefficients: {model.coef_}")
    print(f"Intercept: {model.intercept_}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print("\n")
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Actual Time')
    plt.plot(X, y_pred, color='red', linewidth=2, label='Predicted Time')
    plt.title(f'Linear Regression to Predict {distance_column} Time')
    plt.xlabel('Distance (kilometers)')
    plt.ylabel(f'{distance_column} Time (minutes)')
    plt.legend()
    plt.show()

# List of distance columns
distances = ['5K', '10K', '15K', '20K', 'Half', '25K', '30K', '35K', '40K', 'Official Time']

# Apply the function for each distance
#for distance in distances:
  #  linear_regression_to_predict_time(adult_recreational_runners, distance)

# Calculate mean and standard deviation for each distance
distance_stats = {}
for col in time_columns:
    distance_stats[col] = {
        'mean': adult_recreational_runners[col].mean(),
        'std': adult_recreational_runners[col].std()
    }

# Function to simulate time for each 5K interval
def simulate_times(num_simulations, distance_stats):
    simulation_results = {}
    for distance, stats in distance_stats.items():
        simulation_results[distance] = np.random.normal(stats['mean'], stats['std'], num_simulations)
    return simulation_results

# Simulate times for 1000 runners
num_simulations = 1000
simulated_times = simulate_times(num_simulations, distance_stats)

# Plot the distribution of simulated times for each distance
for distance, times in simulated_times.items():
    plt.figure(figsize=(10, 6))
    sns.histplot(times, kde=True)
    plt.title(f'Simulated Times for {distance}')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Frequency')
    plt.show()

# Print summary statistics for simulated times
#for distance, times in simulated_times.items():
 #   print(f"{distance} - Mean: {np.mean(times):.2f}, Std: {np.std(times):.2f}")

 # Calculate mean and standard deviation for each 5K interval
intervals = ['5K', '10K', '15K', '20K', '25K', '30K', '35K', '40K', 'Official Time']
interval_stats = {}
for i in range(len(intervals)):
    if i == 0:
        interval_stats[intervals[i]] = {
            'mean': adult_recreational_runners[intervals[i]].mean(),
            'std': adult_recreational_runners[intervals[i]].std()
        }
    else:
        previous_interval = intervals[i - 1]
        current_interval = intervals[i]
        interval_stats[current_interval] = {
            'mean': (adult_recreational_runners[current_interval] - adult_recreational_runners[previous_interval]).mean(),
            'std': (adult_recreational_runners[current_interval] - adult_recreational_runners[previous_interval]).std()
        }

# Function to simulate time for each 5K interval independently
def simulate_independent_times(num_simulations, interval_stats):
    simulation_results = {}
    for interval, stats in interval_stats.items():
        simulation_results[interval] = np.random.normal(stats['mean'], stats['std'], num_simulations)
    return simulation_results

# Simulate times for 1000 runners
num_simulations = 1000
simulated_times = simulate_independent_times(num_simulations, interval_stats)

# Convert cumulative times
cumulative_simulated_times = {}
for i, interval in enumerate(intervals):
    if i == 0:
        cumulative_simulated_times[interval] = simulated_times[interval]
    else:
        cumulative_simulated_times[interval] = cumulative_simulated_times[intervals[i - 1]] + simulated_times[interval]

# Plot the distribution of simulated times for each interval
'''for interval, times in simulated_times.items():
    plt.figure(figsize=(10, 6))
    sns.histplot(times, kde=True)
    plt.title(f'Simulated Independent Times for {interval}')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Frequency')
    plt.show()

# Plot the distribution of cumulative simulated times for each interval
for interval, times in cumulative_simulated_times.items():
    plt.figure(figsize=(10, 6))
    sns.histplot(times, kde=True)
    plt.title(f'Cumulative Simulated Times for {interval}')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Frequency')
    plt.show()'''

# Print summary statistics for cumulative simulated times
for interval, times in simulated_times.items():
    print(f"{interval} - Mean: {np.mean(times):.2f}, Std: {np.std(times):.2f}")