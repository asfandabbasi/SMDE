import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load the dataset
runner_data = pd.read_csv('Assignment2/marathon_results_2015.csv')

# Convert Bib to numerical values, removing invalid entries
runner_data['Bib'] = pd.to_numeric(runner_data['Bib'], errors='coerce')
runner_data = runner_data.dropna(subset=['Bib'])
runner_data['Bib'] = runner_data['Bib'].astype(int)

# Define relevant features for PCA
features = ['Age', 'Bib', '5K', '10K', '15K', '20K', 'Half', '25K', '30K', '35K', '40K', 'Official Time']

# Convert time features to total seconds
for feature in features[2:]:
    # remove rows that have '-' in the feature
    runner_data = runner_data[~runner_data[feature].str.contains('-')]
    runner_data[feature] = pd.to_timedelta(runner_data[feature]).dt.total_seconds()

# Drop rows with missing values in the selected features
runner_data = runner_data.dropna(subset=features)

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(runner_data[features])

# Apply PCA
pca = PCA(n_components=2)  # Reduce to 2 principal components for visualization
pca_result = pca.fit_transform(scaled_features)

# Add PCA results to the dataframe
runner_data['PCA1'] = pca_result[:, 0]
runner_data['PCA2'] = pca_result[:, 1]


# Use a clustering algorithm to identify groups, e.g., KMeans
from sklearn.cluster import KMeans

# Perform KMeans clustering
kmeans = KMeans(n_clusters=3)  # Example: 3 clusters
runner_data['Cluster'] = kmeans.fit_predict(pca_result)

# Check for normality in each cluster
for cluster in range(3):
    cluster_data = runner_data[runner_data['Cluster'] == cluster]
    completion_times = cluster_data['Official Time']
    
    sns.histplot(completion_times, kde=True)
    plt.title(f'Histogram of Completion Times for Cluster {cluster}')
    plt.show()
    
    # Q-Q plot
    stats.probplot(completion_times, dist="norm", plot=plt)
    plt.title(f'Q-Q Plot for Cluster {cluster}')
    plt.show()
    
    # Shapiro-Wilk test
    shapiro_test = stats.shapiro(completion_times)
    print(f'Shapiro-Wilk Test for Cluster {cluster}: {shapiro_test}')
