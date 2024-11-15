# A/B test of US election polls

The aim of this project is to predict the party that would win the US election based on the polls given by these popular polling organisations:

FiveThirtyEight - https://projects.fivethirtyeight.com/polls/president-general/2024/

RealClearPolitics -https://www.realclearpolling.com/latest-polls/president/general-election

270toWin - https://www.270towin.com/2024-presidential-election-polls/

The Hill's Election Poll Tracker - https://elections2024.thehill.com/national/

The datasets gathered were put into .csv files to be imported into the sample_generator script to generate a set of 50,000 sample data. The sample data would then be processed by the predicted_analysis script and thus could predict the likely winner of each state and the overall winner.

# The Datasets

The polling data consists of 5 tables:

0.state_population_data
	
 - Columns: state, population
 
1.polling_data_state

2.polling_data_age

3.polling_data_gender

4.polling_data_ethnic
		
  - Columns: respective demographic (state, age, gender, ethnic), democrat, republican, undecided

The samples generated depends on the data in these 5 tables. The overall sample size is generated proportionally in relation to the population size of each state (0.state_population_data), so the higher the population, the more samples it would generate from that state. For example, California has a population of 38,965,193 out of the total 334,235,923, giving it a 11.66% share of the overall sample size, which makes up 5,830 of the 50,000 samples. 

It would then take the percentages of each of the following demographic tables and allocate a new column called "predicted_vote" where the result would be either, 'democrat', 'republican' or 'undecided'. Again the size of the sample for each demographic is proportional to the percentage that are polled to vote for one of the three options. For example, 46% of the samples aged 45-64 are polled to vote for democrat, therefore from the 5,830 California samples, there would be 2,682 that would be allocated to the predicted_vote of democrat.

The model can be kept up to date by changing the population size of each state and the polled percentages for each party.

# The Sample_Generator script
This script will generate a sample of 50,000 votes at random based on the numbers in the 5 datasets. It will then create a new .csv dataframe with a table with 6 columns of information about the voters demographic and their predicted_vote:

	- State
 
	- Population
 
	- Age
 
	- Gender
 
	- Ethnic
 
	- Predicted vote

The new .csv file will be called "generated_polling_sample.csv"

# The Predition_Analysis script
This script will take the newly generated polling sample and run statistics based on the sample data. It will calculate 6 columns of data for each state:
	- State
 
	- Democrat Support
 
	- Republican Support
 
	- Margin of Error
 
	- z-score
 
	- p_value
 
	- Significance
 

## Margin of Error
The purpose of the margin of error is to quantify the range within which the true value is likely to fall. For example, Alaska has a predicted democrat support of 44% with a MoE of ±3%. This means the true value is likely to fall anywhere between 41% and 47%. To calculate the margin of error we use the equation:

![enter image description here](https://iili.io/2AVCS3P.png)

Where:

z = 1.96 (typically 95% confidence level of a standard normal distribution)

p = proportion of pooled votes as a percentage

n = sample size

## z-score & p_value
The purpose of the z-score is to measure how far the observed result is from the expected mean, expressed in terms of standard deviations. It is used to standardize results and determine the statistical significance of the data. In this case to calculate the z-score, we use the equation:

z= (Democrat Support − Republican Support) / Standard Error​

Where:

Standard Error = Standard Deviation of the sampling distribution
