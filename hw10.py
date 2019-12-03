# ----------------------------------------------------------------------
# Name:     hw10.py
# Purpose:  Application using Pandas Series and DataFrame
#
# Author(s): Kiwibud
# ----------------------------------------------------------------------
"""
Extract information from 2019 FE Guide.csv

Demonstrate using Pandas to answer the following questions about
vehicle testing done at the Environmental Protection Agency's National Vehicle
and Fuel Emissions Laboratory in Ann Arbor, Michigan, and by vehicle
manufacturers with oversight by EPA.
1.How many cars are made by the division Acura?
2.How many 'Guzzlers'  (as indicated by the column 'Guzzler?')  are made by the
manufacturer General Motors?
3.What is the value of the lowest combined Fuel Efficiency as given by "Comb FE
(Guide) - Conventional Fuel"?
4.What car line has the highest Highway FE - Conventional Fuel as given by
"Hwy FE (Guide) - Conventional Fuel"?
5.What is the average combined FE - Conventional Fuel among all wheel drives.
Use 'Drive Desc'.
6.Which car line has the largest difference between Highway and City Fuel
efficiency - Conventional Fuel?
7.What is the average annual fuel cost (Annual Fuel1 Cost - Conventional Fuel)
of supercharged cars?  Use the "Air Aspiration Method Desc" to identify
supercharged cars.
8.What SUV has the highest annual fuel cost?   Use "Carline Class Desc" to
identify SUVs.
9.Which manufacturer has the most cars with manual transmission?
10.What is the average annual fuel cost by car division?
11.What criteria would you use to buy a car?  Write a function that returns
your perfect car based on your criteria.
"""

import pandas as pd
import re


def q1(df):
    """
    How many cars are made by the division Acura?
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: integer - number of cars made by the division Acura
    """
    return len(df[df['Division'] == 'Acura'])


def q2(df):
    """
    How many 'Guzzlers' made by the manufacturer General Motors?
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: integer - number of 'Guzzlers' made by General Motors
    """
    return len(df[(df['Guzzler?'] == 'G') &
                  (df['Mfr Name'] == 'General Motors')])


def q3(df):
    """
    What is the value of the lowest combined Fuel Efficiency as given by
    "Comb FE (Guide) - Conventional Fuel"?
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: float
    """
    return df['Comb FE (Guide) - Conventional Fuel'].min()


def q4(df):
    """
    What car line has the highest Highway FE - Conventional Fuel as given by
    "Hwy FE (Guide) - Conventional Fuel"?
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: string
    """
    return df['Hwy FE (Guide) - Conventional Fuel'].idxmax()


def q5(df):
    """
    What is the average combined FE - Conventional Fuel among all wheel drives.
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: float
    """
    return df.loc[df['Drive Desc'] == 'All Wheel Drive',
                  'Comb FE (Guide) - Conventional Fuel'].mean()


def q6(df):
    """
    Which car line has the largest difference between Highway and City Fuel
    efficiency - Conventional Fuel?
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: string
    """
    return abs(df['Hwy FE (Guide) - Conventional Fuel'] -
               df['City FE (Guide) - Conventional Fuel']).idxmax()


def q7(df):
    """
    What is the average annual fuel cost (Annual Fuel1 Cost-Conventional Fuel)
    of supercharged cars?  Use the "Air Aspiration Method Desc" to identify
    supercharged cars.
    'Annual Fuel1 Cost - Conventional Fuel'| Supercharged
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: float
    """
    return df.loc[df['Air Aspiration Method Desc'] == 'Supercharged',
                  'Annual Fuel1 Cost - Conventional Fuel'].mean()


def q8(df):
    """
    What SUV has the highest annual fuel cost? Use "Carline Class Desc" to
    identify SUVs.
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: string - carline
    """
    return df.loc[df['Carline Class Desc'].str.contains(r'\bSUV\b', na=False),
                  'Annual Fuel1 Cost - Conventional Fuel'].idxmax()


def q9(df):
    """
    Which manufacturer has the most cars with manual transmission?
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: string
    """
    manual_df = df[df['Trans Desc'] == 'Manual']
    return manual_df.groupby('Mfr Name')['Trans Desc'].count().idxmax()


def q10(df):
    """
    What is the average annual fuel cost by car division?
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: Pandas series
    """
    return df.groupby('Division')['Annual Fuel1 Cost - Conventional Fuel'] \
        .mean()


def q11_thy(df):
    """
    Write a function that returns your perfect car based on your criteria:
    Made by Toyota, automatic, not require a specific type of gasoline,
    Annual Fuel Cost is cheapest and less than 3000
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: string - carline
    """
    criteria = df[(df['Mfr Name'] == 'Toyota')
                  & (df['Trans Desc'] == 'Automatic')
                  & (df['Fuel Usage Desc - Conventional Fuel'].str.contains
                     ('Recommended'))
                  & (df['Annual Fuel1 Cost - Conventional Fuel'] < 3000)]
    return criteria['Annual Fuel1 Cost - Conventional Fuel'].idxmin()

def q11_grace(df):
    """
    Write a function that returns your perfect car based on your criteria:
    All wheel drive, not Two Seaters, Transmission is Auto, and has highest
    HWY FE (Guide) - Conventional Fuel
    :param df: Pandas DataFrame represents the data in 2019 FE Guide.csv
    :return: string - carline
    """
    goal = df.loc[(df['Drive Desc'] == 'All Wheel Drive') & (df['Carline '
            'Class Desc'] != 'Two Seaters') & (df['Transmission'].str.contains(
        r'\bAuto\b', flags=re.IGNORECASE, na=False))]
    return goal['Hwy FE (Guide) - Conventional Fuel'].idxmax()


def main():
    df = pd.read_csv('2019 FE Guide.csv', index_col=2, usecols=range(1, 70))
    print(f'Q1: {q1(df)}')
    print(f'Q2: {q2(df)}')
    print(f'Q3: {q3(df)}')
    print(f'Q4: {q4(df)}')
    print(f'Q5: {q5(df)}')
    print(f'Q6: {q6(df)}')
    print(f'Q7: {q7(df)}')
    print(f'Q8: {q8(df)}')
    print(f'Q9: {q9(df)}')
    print(f'Q10:\n{q10(df)}')
    print(f'Q11_Thy: {q11_thy(df)}')
    print(f'Q11_Grace: {q11_grace(df)}')

if __name__ == '__main__':
    main()