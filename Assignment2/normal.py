import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
runner_data = pd.read_csv('Assignment2/marathon_results_2015.csv')
runner_data['Official Time'] = pd.to_timedelta(runner_data['Official Time']).dt.total_seconds() / 60
#runner_data = runner_data[runner_data['M/F'] == 'M']
# Convert Bib to numerical values, removing invalid entries
runner_data['Bib'] = pd.to_numeric(runner_data['Bib'], errors='coerce')
runner_data = runner_data.dropna(subset=['Bib'])
runner_data['Bib'] = runner_data['Bib'].astype(int)

# Function to categorize runners by age groups
def get_age_group(age):
    if 20 <= age <= 29:
        return '20-29'
    elif 30 <= age <= 39:
        return '30-39'
    elif 40 <= age <= 49:
        return '40-49'
    elif 50 <= age <= 59:
        return '50-59'
    else:
        return '60+'

runner_data['Age Group'] = runner_data['Age'].apply(get_age_group)

# Example categories to check for normal distribution
categories = {
    'Elite Male 20-29': runner_data[(runner_data['Bib'] < 1000) & (runner_data['M/F'] == 'M') & (runner_data['Age Group'] == '20-29')],
    'Elite Female 20-29': runner_data[(runner_data['Bib'] < 1000) & (runner_data['M/F'] == 'F') & (runner_data['Age Group'] == '20-29')],
    'Recreational Male 30-39': runner_data[(runner_data['Bib'] >= 1000) & (runner_data['Bib'] < 5000) & (runner_data['M/F'] == 'M') & (runner_data['Age Group'] == '30-39')],
    'Recreational Female 30-39': runner_data[(runner_data['Bib'] >= 1000) & (runner_data['Bib'] < 5000) & (runner_data['M/F'] == 'F') & (runner_data['Age Group'] == '30-39')],
    'Middle Pack 30-39': runner_data[(runner_data['Overall'] > 1000) & (runner_data['Overall'] <= 3000) & (runner_data['Age Group'] == '30-39')]
}

# Check for normality in each category
for category, data in categories.items():
    completion_times = pd.to_timedelta(data['Official Time']).dt.total_seconds()
    sns.histplot(completion_times, kde=True)
    plt.title(f'Histogram of Completion Times for {category}')
    plt.show()
    
    # Q-Q plot
    stats.probplot(completion_times, dist="norm", plot=plt)
    plt.title(f'Q-Q Plot for {category}')
    plt.show()
    
    # Shapiro-Wilk test
    shapiro_test = stats.shapiro(completion_times)
    print(f'Shapiro-Wilk Test for {category}: {shapiro_test}')
