import pandas as pd
import numpy as np

state_population = pd.read_csv('0.state_population_data.csv')
state_polling = pd.read_csv('1.polling_data_state.csv')
age_polling = pd.read_csv('2.polling_data_age.csv')
gender_polling = pd.read_csv('3.polling_data_gender.csv')
ethnic_polling = pd.read_csv('4.polling_data_ethnic.csv')

# Remove commas from the population column and ensure it is numeric
state_population['population'] = state_population['population'].str.replace(',', '')
state_population['population'] = pd.to_numeric(state_population['population'], errors='coerce')

# Convert percentages to numeric in polling datasets
for dataset in [state_polling, age_polling, gender_polling, ethnic_polling]:
    for col in ['democrat', 'republican', 'undecided']:
        dataset[col] = dataset[col].str.replace('%', '').astype(float) / 100

# Drop rows with NaN population values
state_population = state_population.dropna(subset=['population'])

# Total sample size
sample_size = 2000

# Calculate state-level allocation based on population
state_population['sample_allocation'] = (state_population['population'] / state_population['population'].sum()) * sample_size
state_population['sample_allocation'] = state_population['sample_allocation'].fillna(0).round().astype(int)

final_dataset = []

# Generate samples
for _, state_row in state_population.iterrows():
    state = state_row['state']
    state_samples = state_row['sample_allocation']
    print(f"Processing state: {state} with allocated samples: {state_samples}")

    # Get state-specific polling data
    state_poll = state_polling[state_polling['state'] == state]
    if state_poll.empty:
        print(f"No polling data for state: {state}")
        continue
    state_poll = state_poll.iloc[0]
    
    # Calculate votes for each party in the state
    for party in ['democrat', 'republican', 'undecided']:
        party_samples = round(state_samples * state_poll[party])
        print(f"  Party: {party}, Samples: {party_samples}")
        if party_samples == 0:
            continue
        
        # Split party samples by age
        for _, age_row in age_polling.iterrows():
            age_group = age_row['age']
            age_fraction = age_row[party]
            age_samples = round(party_samples * age_fraction)
            if age_samples == 0:
                continue
            
            # Split age samples by gender
            for _, gender_row in gender_polling.iterrows():
                gender = gender_row['gender']
                gender_fraction = gender_row[party]
                gender_samples = round(age_samples * gender_fraction)
                if gender_samples == 0:
                    continue
                
                # Split gender samples by ethnicity
                for _, ethnic_row in ethnic_polling.iterrows():
                    ethnic = ethnic_row['ethnic']
                    ethnic_fraction = ethnic_row[party]
                    ethnic_samples = round(gender_samples * ethnic_fraction)
                    if ethnic_samples == 0:
                        continue
                    
                    # Add rows to the dataset
                    for _ in range(ethnic_samples):
                        final_dataset.append({
                            'state': state,
                            'population': state_row['population'],
                            'age': age_group,
                            'gender': gender,
                            'ethnic': ethnic,
                            'predicted_vote': party
                        })

# Convert the final dataset to a DataFrame
final_dataset_df = pd.DataFrame(final_dataset)

# Normalize the dataset to match the exact sample size
current_size = len(final_dataset_df)
if current_size > sample_size:
    # Randomly drop excess rows
    final_dataset_df = final_dataset_df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    print(f"Reduced dataset to match sample size: {sample_size}")
elif current_size < sample_size:
    # Randomly duplicate rows to fill the deficit
    deficit = sample_size - current_size
    duplicates = final_dataset_df.sample(n=deficit, replace=True, random_state=42)
    final_dataset_df = pd.concat([final_dataset_df, duplicates]).reset_index(drop=True)
    print(f"Increased dataset to match sample size: {sample_size}")

# Save the dataset to a CSV file
output_path = "generated_polling_sample.csv"
final_dataset_df.to_csv(output_path, index=False)

print(f"Sample dataset generated and saved to {output_path}")
