import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# Read the CSV file
df=pd.read_csv(r'C:\Users\LENOVO\OneDrive\Desktop\mymoviedb.csv', lineterminator='\n')
print(df.head())  # Display the first 5 rows
print(df.info())  # Display the columns of the DataFrame
print(df.shape)  # Display the shape of the DataFrame

print(df['Genre'].head(10))  # Display the first 10 rows of the 'genre' column
print(df.isnull().sum())  # Check for missing values in the DataFrame
print(df.duplicated().sum())  # Check for duplicate rows in the DataFrame

"""Exploration summary

1. we have a dataframe consisting of 9827 rows and 9 columns.
2. our dataset look tidy and clean, with no missing values or duplicates.
3. Release dat column need to be caste into date time format to extract year value.
4. Overview, original_language and poster-Url wouldn't be useful for our analysis. 
5. there is outliers in the popularity column.
6. vote_average be cateogrised for better analysis
7.genre column has a seprate value and white spaces that need to be  handled and casted into categorey. exploration summary 


"""
print(df['Popularity'].head(10))  # Display the first 10 rows of the 'popularity' column

df['Release_Date'] = pd.to_datetime(df['Release_Date'])
print(df['Release_Date'])  # Display the data type of the 'release_date' column

df['Release_Date'] = df['Release_Date'].dt.year  # Extracting the year from the 'release_date' column

#dropping the column

cols=['Overview','Original_Language','Poster_Url']
df.drop(columns=cols, inplace=True)  # Dropping the specified columns 
print(df.columns)  # Display the columns of the DataFrame after dropping columns

print(df['Vote_Average'].describe())  # Display the first 10 rows of the 'vote_average' column

# lable the movie accroding to their vote average

"""def label_vote_average(Vote_Average):
    if Vote_Average >= 8:
        return 'Excellent'
    elif Vote_Average >= 6:
        return 'Good'
    elif Vote_Average >= 4:
        return 'Average'
    else:
        return 'Poor'
# Applying the function to create a new column2
df['label_movie']=df['Vote_Average'].apply(label_vote_average)
print(df)"""

def categorize_col(df, col, labels) :

    edges = [df[col].describe()["min"],
             df[col].describe()["25%"],
             df[col].describe()["50%"],
             df[col].describe()["75%"],
             df[col].describe()["max"]]
    
    df[col]=pd.cut(df[col], edges, labels= labels, duplicates= 'drop')
    return df

labels = ['not popular', 'below average', 'average', 'popular'] 

categorize_col(df,'Vote_Average', labels)

print(df['Vote_Average'].head(10))  # Display the first 10 rows of the 'vote_average' column

print(df['Vote_Average'].value_counts())  # Display the value counts of the 'vote_average' column

df.dropna(inplace=True)  # Dropping rows with missing values
print(df.isna().sum())  # Check for missing values after dropping rows

# now we would split the genre into a list and then explode it to have each genre in a separate row
df['Genre'] = df['Genre'].str.split(', ')  # Splitting the 'genre' column into a list

print(df.head(10))  # Display the first 10 rows of the 'genre' column after splitting

df = df.explode('Genre').reset_index(drop= True)  # Exploding the 'genre' column to have each genre in a separate row
print(df['Genre'].head(10))  # Display the first 10 rows of the 'genre' column after exploding

#casting the genre column to category type

df['Genre']= df['Genre'].astype('category')  # Casting the 'genre' column to category type\
print(df['Genre'].dtype)

print(df.nunique()) # Display the number of unique values in each column.

# now we start our analysis

sns.set_style('whitegrid')  # Setting the style for seaborn plots

# Q1. What is the most frequent genre of mivie released on netflix?

print(df['Genre'].describe())

abc_plot=sns.catplot(y='Genre', data=df, kind='count', order= df['Genre'].value_counts().index,
            color='blue',height=7)
abc_plot.fig.suptitle('Most Frequent Genre of Movies Released on Netflix')
plt.tight_layout()
#plt.show()

# Q2.  which has the hightest vote in vote_average column?

xyz=sns.catplot(y='Vote_Average', data=df, kind='count', order= df['Vote_Average'].value_counts().index)
xyz.fig.suptitle('Vote Average Distribution')
#plt.show() 

#Q3. Which movie got the highest popularity? what its genre?   

max_popular= df['Popularity'].max()  # Finding the maximum popularity value
Highest_popular= df[df['Popularity']== max_popular] #filtering the DataFrame for the movie with the highest popularity
print(Highest_popular[['Title', 'Genre', 'Popularity']])  # Displaying the title, genre, and popularity of the movie with the highest popularity

""" spiderman is the most popular movie with a popularity score of 5083.954 and its genre is Action, Adventure, Science Fiction."""

#Q4. Which movie got the lowest popularity? what its genre?   

lowest_popular= df['Popularity'].min()  # Finding the minimum popularity value
Lowest_popular= df[df['Popularity'] == lowest_popular]  # Filtering the DataFrame for the movie with the lowest popularity
print(Lowest_popular[['Title', 'Genre', 'Popularity']])  # Displaying the title, genre, and popularity of the movie with the lowest popularity

""" The lowest popular movie is 'The Last Days of American Crime' and 'Threads' with a popularity score of 13.354 and its genre is (Action, Crime, Science Fiction) and (war, drama and scince fiction)."""

# Q5. Whaich year has the most number of movies released on netflix?
# Count the number of movies per year
# Count the number of movies per year
year_counts = df['Release_Date'].value_counts().sort_index()

# Plot as a bar chart for clear year-wise distribution
plt.figure(figsize=(12,6))
df['Release_Date'].hist(bins=10, color='purple', edgecolor='black')
plt.xlabel('Release Year')
plt.ylabel('Number of Movies')
plt.title('Number of Movies Released on Netflix per Year')
plt.tight_layout()
plt.show()



