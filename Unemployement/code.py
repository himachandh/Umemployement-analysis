import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
df = pd.read_csv('USUnemployment.csv')

# Task 1: Add column for average unemployment rate per year
month_columns = df.columns[1:]
df['Avg_Unemployment_Rate'] = df[month_columns].mean(axis=1)

# Task 1: Create a new DataFrame with Year and Avg_Unemployment_Rate columns
avg_unemployment_df = df[['Year', 'Avg_Unemployment_Rate']].nlargest(5, 'Avg_Unemployment_Rate')

print("Top 5 rows with maximum unemployment rate:")
print(avg_unemployment_df)


# Task 2: Categorize unemployment status
def categorize_unemployment(rate):
    if rate < 4:
        return 'Low'
    elif rate < 6:
        return 'Medium'
    else:
        return 'High'

df['Unemployment_Status'] = df['Avg_Unemployment_Rate'].apply(categorize_unemployment)
unemployment_status_counts = df['Unemployment_Status'].value_counts()
plt.pie(unemployment_status_counts, labels=unemployment_status_counts.index, autopct='%1.1f%%')
plt.title('Unemployment Status')
plt.show()
# Task 3: Add decade column
df['Decade'] = (df['Year'] // 10) * 10

# Task 3: Create a new DataFrame with Year, Unemployment_Status, and Decade columns
output_df = df[['Year', 'Unemployment_Status', 'Decade']].drop_duplicates(subset='Decade')

print("Output DataFrame with Year, Unemployment_Status, and Decade:")
print(output_df)


# Task 4: Perform season-wise average
season_map = {'Winter': ['Jan', 'Feb', 'Dec'],
              'Spring': ['Mar', 'Apr', 'May'],
              'Summer': ['Jun', 'Jul', 'Aug'],
              'Autumn': ['Sep', 'Oct', 'Nov']}

for season, months in season_map.items():
    df[season] = df[months].mean(axis=1)
years_range = range(1990, 2006)
seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
plt.figure(figsize=(10, 6))
for season in seasons:
    plt.plot(df.loc[df['Year'].isin(years_range), 'Year'], df.loc[df['Year'].isin(years_range), season], label=season)
plt.xlabel('Year')
plt.ylabel('Unemployment Rate')
plt.title('Season-wise Unemployment Rate')
plt.legend()
plt.show()

# Task 5: Calculate sliding window averages
window_size = 5
for season, months in season_map.items():
    sliding_avg_col = f"{season}_Sliding_Avg"
    df[sliding_avg_col] = df[months].rolling(window=window_size, min_periods=1).mean().mean(axis=1)

# Task 5: Print row data for specific years
specific_years = [1950, 1960, 1970, 1980, 1990, 2000]
print("Row data for specific years:")
specific_years_df = df[df['Year'].isin(specific_years)].reset_index(drop=True)
specific_years_df = specific_years_df[['Year'] + list(season_map.keys()) + [f"{season}_Sliding_Avg" for season in season_map.keys()]]
print(specific_years_df)

