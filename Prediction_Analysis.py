from scipy.stats import norm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sample_table = pd.read_csv('generated_polling_sample-5kv3.csv')

# Aggregate sample data by state and calculate support proportions
state_support = sample_table.groupby(['state', 'predicted_vote']).size().unstack(fill_value=0)
state_support['total'] = state_support.sum(axis=1)
state_support['Democratic_pct'] = state_support['democrat'] / state_support['total']
state_support['Republican_pct'] = state_support['republican'] / state_support['total']
state_support = state_support[['Democratic_pct', 'Republican_pct']]

results = []

# Z-score for 95% confidence level
z = 1.96

for state in state_support.index:
    # Get the Democrat and Republican proportions
    democrat_pct = state_support.loc[state, 'Democratic_pct']
    republican_pct = state_support.loc[state, 'Republican_pct']
    total_votes = sample_table[sample_table['state'] == state].shape[0]  # Sample size for the state

    # Calculate the pooled proportion
    pooled_pct = (democrat_pct + republican_pct) / 2
    pooled_prop = (democrat_pct * total_votes + republican_pct * total_votes) / (2 * total_votes)

    # Calculate margin of error
    margin_of_error = z * np.sqrt(pooled_pct * (1 - pooled_pct) / total_votes)
    
    # Calculate standard error for the difference in proportions
    standard_error = np.sqrt(pooled_prop * (1 - pooled_prop) * (2 / total_votes))
    
    # Calculate the z-score for the difference in proportions
    z_score = (democrat_pct - republican_pct) / standard_error
    
    # Calculate the p-value (two-tailed)
    p_value = 2 * (1 - norm.cdf(abs(z_score)))
    
    # Determine if the difference is statistically significant
    significance = "Significant" if p_value < 0.05 else "Not Significant"
    
    # Store the result for this state
    results.append({
        'State': state,
        'Democrat Support': democrat_pct,
        'Republican Support': republican_pct,
        'Margin of Error': margin_of_error,
        'z_score': z_score,
        'p_value': p_value,
        'Significance': significance
    })

results_df = pd.DataFrame(results)
results_df['likely_winner'] = np.where(
    results_df['Democrat Support'] > results_df['Republican Support'], 'Democrat', 'Republican'
)

# Group by likely winner and significance, then count the number of states in each group
significant_counts_by_winner = results_df.groupby(['likely_winner', 'Significance']).size().unstack(fill_value=0)

# Count the number of states each party is likely to win
winner_counts = results_df['likely_winner'].value_counts()

# Calculate mean support percentages and mean margins of error
mean_democrat_pct = results_df['Democrat Support'].mean()
mean_republican_pct = results_df['Republican Support'].mean()
mean_moe = results_df['Margin of Error'].mean()

# Create a stacked bar chart showing the number of likely winners for each party
winner_counts = results_df['likely_winner'].value_counts()

# Create bar graph for likely winner
plt.figure(figsize=(8, 6))
winner_counts.plot(kind='bar', stacked=True, color=['blue', 'red'])
plt.title('Predicted Winner by Party', fontsize=22, weight='bold')
plt.ylabel('Number of States', fontsize=20, weight='bold')
plt.xlabel('Party ', fontsize=20, weight='bold')
plt.yticks(rotation=0, fontsize=18)
plt.xticks(rotation=0, fontsize=18)
plt.tight_layout()
plt.show()

# Prepare the data: creating a DataFrame for the heatmap where states are the rows
heatmap_data = results_df[['State', 'Democrat Support', 'Republican Support']]

# Set the state as the index for the heatmap
heatmap_data = heatmap_data.set_index('State')

# Create the heatmap, with the states on the y-axis and parties on the x-axis
plt.figure(figsize=(14, 10))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm_r', center=0.5, cbar_kws={'label': 'Support Percentage (%)'}
).figure.axes[-1].yaxis.label.set_size(16)
plt.title('Democrat & Republican Support % by 50 States', fontsize=22, weight='bold')
plt.ylabel('State', fontsize=20, weight='bold')
plt.xlabel('Party', fontsize=20, weight='bold')
plt.yticks(rotation=0, fontsize=12)
plt.xticks(rotation=0, fontsize=18)
plt.tight_layout()
plt.show()

# Create scatterplot for Margin of Error
plt.figure(figsize=(12, 10))
sns.scatterplot(data=results_df, x='Margin of Error', y='State', hue='likely_winner', palette={'Democrat': 'blue', 'Republican': 'red'}, s=100)
plt.title('Margin of Error by State', fontsize=22, weight='bold')
plt.xlabel('Margin of Error', fontsize=20, weight='bold')
plt.ylabel('State', fontsize=20, weight='bold')
plt.yticks(rotation=0, fontsize=12)
plt.xticks(rotation=0, fontsize=18)
plt.tight_layout()
plt.show()

# Export the DataFrame to a CSV file
output_path = "predicted_results_table.csv"
results_df.to_csv(output_path, index=False)

print(f"Table successfully exported to {output_path}")
