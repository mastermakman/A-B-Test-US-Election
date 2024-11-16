# How to run locally 

You will need Python with the following libraries installed:

	- pandas 
	- numpy
	- scipy.stats
	- matplotlib
	- seaborn

**Step 1:**
Download all the files locally and installed a any source code editor.

**Step 2:**
To run the test you will need to populate the 5 .csv files containing the polling datasets with up to date data on each of the 50 state's population, their respective predicted polling percentage as well as their demographic of age, gender and ethnic groups. These include:

	- 0.state_population_data
	- 1.polling_data_state
	- 2.polling_data_age
	- 3.polling_data_gender
	- 4.polling_data_ethnic

**Step 3:**
Once updated, you can run the "Sample_Generator" script and it will create a .csv file called "generated_polling_sample.csv" with 2000 samples of potential predicted votes. You are able to adjust sample size by simple changing it in the code:

    sample_size  =  2000

Keep in mind too small of a sample size will result in bigger Margin of Error for each state as less samples mean data will be more skewed and bias. While too big of a sample size will cause an unrealistic z-score making the standard deviation too far from the expected mean.

**Step 4:**
Once the generated sample has been created you can run the "Prediction_Analysis" script and it will create another .csv file called "predicted_results_table.csv" where you can see which state is likely to vote for which  party along with statistics of the Margin of Error, z-score, p_value, Significance and likely winner. You would also see the average support of each party overall and the average Margin of Error.

Three visuals will be displayed:

1. Bar chart - Predicted Winner by Party
2. Heatmap - Democratic & Republican Support % by 50 States
3. Scatterplot - Margin of Error by state.

# A/B test of US election polls

The Hypothesis Test:

	- Null Hypothesis H0 - Assume there is no difference in support for either party (Democrat or Republican).
	- Alternative Hypothesis H1 - Assumes there is a difference in support.

The aim of this project is to predict the party that would win the US election based on the polls given by these popular polling organisations:

FiveThirtyEight - https://projects.fivethirtyeight.com/polls/president-general/2024/

RealClearPolitics -https://www.realclearpolling.com/latest-polls/president/general-election

270toWin - https://www.270towin.com/2024-presidential-election-polls/

The Hill's Election Poll Tracker - https://elections2024.thehill.com/national/


The datasets gathered were put into .csv files to be imported into the sample_generator script to generate a set of 5,000 sample data. The sample data would then be processed by the predicted_analysis script and thus could predict the likely winner of each state and the overall winner.

# The Datasets
The polling data consists of 5 tables:

0.state_population_data
	- Columns: state, population
 
1.polling_data_state

2.polling_data_age

3.polling_data_gender

4.polling_data_ethnic
		- Columns: respective demographic (state, age, gender, ethnic), democrat, republican, undecided


The samples generated depends on the data in these 5 tables. The overall sample size is generated proportionally in relation to the population size of each state (0.state_population_data), so the higher the population, the more samples it would generate from that state. For example, California has a population of 38,965,193 out of the total 334,235,923, giving it a 11.66% share of the overall sample size, which makes up 5,830 of the 5,000 samples. 

It would then take the percentages of each of the following demographic tables and allocate a new column called "predicted_vote" where the result would be either, 'democrat', 'republican' or 'undecided'. Again the size of the sample for each demographic is proportional to the percentage that are polled to vote for one of the three options. For example, 46% of the samples aged 45-64 are polled to vote for democrat, therefore from the 5,830 California samples, there would be 2,682 that would be allocated to the predicted_vote of democrat.

The model can be kept up to date by changing the population size of each state and the polled percentages for each party.

# The Sample_Generator script
This script will generate a sample of 5,000 votes at random based on the numbers in the 5 datasets. It will then create a new .csv dataframe with a table with 6 columns of information about the voters demographic and their predicted_vote:

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

The script will create a new .csv file called "predicted_results_table.csv" 

## Margin of Error
The purpose of the margin of error is to quantify the range within which the true value is likely to fall. For example, Alaska has a predicted democrat support of 44% with a MoE of ±3%. This means the true value is likely to fall anywhere between 41% and 47%. To calculate the margin of error we use the equation:

![enter image description here](https://iili.io/2AVCS3P.png)

Where:

z = 1.96 (typically 95% confidence level of a standard normal distribution)

p = proportion of pooled votes as a percentage

n = sample size

## z-score & Standard Error (SE) 
The purpose of the z-score is to measure how far the observed result is from the expected mean, expressed in terms of standard deviations. It is used to standardize results and determine the statistical significance of the data. The z-score is heavily reliant on the sample size, here a sample size of 5000 gives a score of -3 to +3 with one or two exceptions. In this case to calculate the z-score, we use the equation:

z= (Democrat Support − Republican Support) / Standard Error​

Where:

Standard Error = Standard Deviation of the sampling distribution

The Standard Error is a measure of how much the sample data might differ from the true value. If we take multiple samples, the result will not be the same each time. The SE tells us how much those results are likely to vary. A smaller SE means the sample result is closer to the true value and a large SE  means the results are less reliable. It is calculated with the equation:

![enter image description here](https://iili.io/2A8usl2.png)

Where:

p = proportion of support for each party (e.g. 44% = 0.44)

n = total sample size

For example, Connecticut has a democratic support of 60%, a republican support of 40% and a Standard Error of 0.91287 therefore:

z-score = (0.6 - 0.4) / 0.091 =  0.2 / 0.091 = 2.19

This tells us that the observed difference (20%) is 2.19 deviations away from the mean.

## p_value
This tells us how likely the results are if the null hypothesis is true (there is no difference in support between the two parties). It asks, "How likely is this result just by random chance?" A small p-value (significant) of <0.05 means it's unlikely to see this result if the null hypothesis is true, this gives us strong evidence to reject the null hypothesis. A large p-value (not significant) of >0.05 means it's likely that this result was by random chance if the hypothesis is true. It is calculated using the equation:

p_value = 2 * P(Z>∣z∣) 

Where:

Z = z-score

P(Z>∣z∣) = the probability of getting a z-score greater than the absolute value of z (regardless if it's positive or negative)

For example, Mississippi has a p_value of 0.025 which is < 0.05 meaning that we should reject the hypothesis that there is no difference in support for either party for this state because the result we got was not by random chance. 

## Significance
This tells us if the state has a p_value below or above the 0.05 threshold. whether the results we got from the sample are Significant enough to believe the Hypothesis or not.

Significant = There is a statistical difference in support between the 2 parties for the state
Not Significant = There isn't much evidence to support there's a difference in support between the 2 parties for the state

# The results
With a sample size of 5000, the results show that Democrats have an overall higher average support (54.5%) than the Republicans (45.5%) with an average Margin of Error of (14.2%).

The statistics also show that the Democrats have more states with significant difference (18) than the Republicans (6) meaning there is a larger gaps of support in more states for the Democrats.  

The bar chart below shows that Democrats are predicted to win 29 states while Republicans are predicted to win 21.

![enter image description here](https://iili.io/2AvYGxn.png)

The heatmap shows a breakdown of support for the parties by each state. The Democrats on the left are represented in blue while the Republicans on the right are in red. The darker the shade of each colour, the more support they are predicted to have.

![enter image description here](https://iili.io/2AvlHNI.png)

The scatterplot shows the Margin of Error for each state. It ranges from the lowest MoE of California (±4%) to the state with the highest MoE which is Wyoming (±34%). This shows that the MoE is heavily dependent on the population size of the state as California has the most inhabitants and Wyoming with the least, thus the sample size adjusts accordingly. The legend shows the predicted winner by state, again with Democrats in blue and Republicans in red.

![enter image description here](https://iili.io/2Av413b.png)
