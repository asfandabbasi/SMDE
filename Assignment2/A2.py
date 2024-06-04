import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# Load the dataset
runner_data = pd.read_csv('Assignment2/marathon_results_2015.csv')
#convert completion time to minutes
runner_data['Official Time'] = pd.to_timedelta(runner_data['Official Time']).dt.total_seconds() / 60

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

