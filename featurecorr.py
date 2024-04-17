import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import fisher_exact

# fetch dataset 
phishing_websites = pd.read_csv("dataset_B_05_2020.csv")

# data (as pandas dataframes) 
X = phishing_websites.drop(["url", "status", "random_domain"], axis=1).copy()
y = phishing_websites["status"].replace({'phishing': 1, 'legitimate': 0})
print(X.shape[1])

# variable information 
feature_names = X.columns.values
columns = list(feature_names)

Xdf = pd.DataFrame(X)
print(Xdf['nb_or'])

import seaborn as sns

# Calculate Pearson correlation coefficients for all columns
output = Xdf.corr()
print(Xdf.shape)
print(output)
plt.figure(figsize=(16, 14))
sns.heatmap(output.astype(float), annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 3})
plt.title('Correlation Table')
output_file = "correlation_plot.pdf"
plt.savefig(output_file, format='pdf', bbox_inches='tight')
plt.close()

def calculate_chi2_p_values(df):
    num_columns = len(df.columns)
    p_values = np.empty((num_columns, num_columns))
    
    for i, col1 in enumerate(df.columns):
        for j, col2 in enumerate(df.columns):
            if i == j:
                p_values[i, j] = np.nan
            else:
                contingency_table = pd.crosstab(df[col1], df[col2])
                _, p_value, _, _ = chi2_contingency(contingency_table)
                p_values[i, j] = p_value
                
    return pd.DataFrame(p_values, index=df.columns, columns=df.columns)

def plot_chi2_p_values(p_values, output_file=None):
    plt.figure(figsize=(16, 14))
    sns.heatmap(p_values, cmap='coolwarm', annot=True, fmt=".2f", annot_kws={"size": 3})
    plt.title('Chi-Square Test P-Values for Each Column Pair')
    plt.xlabel('Column Index')
    plt.ylabel('Column Index')
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close

chisq_test = calculate_chi2_p_values(Xdf)

# Save and/or plot Chi-Square test p-values
output_file = "chi2_p_values_plot.pdf"
plot_chi2_p_values(chisq_test, output_file=output_file)

def calculate_fisher_exact_p_values(df):
    num_columns = len(df.columns)
    p_values = np.empty((num_columns, num_columns))
    
    for i, col1 in enumerate(df.columns):
        for j, col2 in enumerate(df.columns):
            if i == j:
                p_values[i, j] = np.nan
            else:
                contingency_table = pd.crosstab(df[col1], df[col2])
                if contingency_table.shape == (2, 2):
                    _, p_value = fisher_exact(contingency_table)
                else:
                    p_value = np.nan
                p_values[i, j] = p_value
                
    return pd.DataFrame(p_values, index=df.columns, columns=df.columns)

def plot_fisher_p_values(p_values, output_file=None):
    plt.figure(figsize=(16, 14))
    sns.heatmap(p_values, cmap='coolwarm', annot=True, fmt=".2f", annot_kws={"size": 3})
    plt.title('Fisher Exact Test P-Values for Each Column Pair')
    plt.xlabel('Column Index')
    plt.ylabel('Column Index')
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close

p_values_fisher = calculate_fisher_exact_p_values(Xdf)

# Plot Fisher's exact test p-values
plot_fisher_p_values(p_values_fisher, "fischer_output.pdf")
