"""
Udacity Project: Exploring US Bikeshare Data

Purpose: "In this project, you will write Python code to import US bike share data and answer interesting questions about it by computing descriptive statistics.
 You will also write a script that takes in raw input to create an interactive experience in the terminal to present these statistics."

Ressources used:
Pandas to_datetime:  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
Help on converting seconds to hours, minutes and seconds: https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
Answer from tutor Wang to question regarding mode() and mean(): https://knowledge.udacity.com/questions/663366
Mode() function in python: https://www.geeksforgeeks.org/python-statistics-mode-function/
Mean() function in python: https://www.geeksforgeeks.org/python-statistics-mean-function/
Answer from tutor Raghavendra Prasad regarding mode and count: https://knowledge.udacity.com/questions/639181

"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
            city = input('From which city do you want to see the data? We have Chicago, New York City, Washington: ').lower()
            if city not in CITY_DATA:
                        print('That is not in our database. Please choose Chicago, New York City or Washington!')
            else:
                        break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
            month = input('Please enter a month from January to June, or enter "all" to see all data: ').lower()
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            if month !='all' and month not in months:
                         print('Please enter a valid month')
            else:
                         break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('Please enter the day of the week you want to examine or enter "all" to see data of all weekdays: ').lower()
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            if day !=  'all' and day not in days:
                print('Please enter a valid day! ')
            else:
                break

    print('-'*40)

    print('\nDisplaying the results for: ', city.title(), ', Month:', month.title(), ', Day of the week: ', day.title(), '\n')

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data into the dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week into new columns
    df['month']=df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by months
    if month != 'all':
        # extract the moths int value from the months list index
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of the week
        if day != 'all':

        # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    """ Find the most common Rental Month of the week with mode()"""
    most_common_month = df['month'].mode()[0]

    """ Define and use list of months' text names for better readability """
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The most common Rental Month is: ', months[most_common_month-1].capitalize(), "\n")

    # TO DO: display the most common day of week
    """ Find the most common Rental Day of the week with mode()"""
    most_common_day = df ['day_of_week'].mode()[0]
    print('The most common Rental Day of the week is: ', most_common_day, "\n")

    # TO DO: display the most common start hour
    """ Select hour from Start Time column """
    df['hour'] = df['Start Time'].dt.hour
    """ Find the most common Rental Start Hour with mode()"""
    most_common_hour = df ['hour'].mode()[0]
    print('The most common Rental Start Hour of the day is: ', most_common_hour, "\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('The most commonly used Start Station is ', most_common_start, '. Count: ', df['Start Station'].value_counts()[0], '.')

    # TO DO: display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('The most commonly used End Station is ', most_common_end, '. Count: ', df['End Station'].value_counts()[0], '.')

    # TO DO: display most frequent combination of start station and end station trip
    df['most_frequent_station_combo'] = df['Start Station'] + ' and ' + df['End Station']
    print('The most frequent combination of Start Station and End Trip Station is: ', df['most_frequent_station_combo'].mode()[0], '. Count: ', df['most_frequent_station_combo'].value_counts()[0], '.\n'),

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    """Define a function that calculates hours, minutes and remaining seconds from the total seconds value to print a more readable value """
    def hms(seconds):
         seconds = int(seconds)
         h = seconds // 3600
         m = seconds % 3600 // 60
         s = seconds % 3600 % 60
         return '{:02d} hours {:02d} minutes {:02d} seconds'.format(h, m, s)

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    hours_min_sec = hms(total_travel_time)
    print('Total Travel Time is ', total_travel_time, 'seconds, that is:', hours_min_sec, '. \n')

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    hours_min_sec_mean = hms(mean_time)

    print('Mean Travel Time is ', mean_time, 'seconds, that is (rounded):', hours_min_sec_mean, '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, '\n')


    if 'Gender' in df:
    # TO DO: Display counts of gender
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender), '\n'
    else:
        print('We have no information on the gender of the customers in this city.\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nYear of Birth:')
        earliest_birthyear = df['Birth Year'].min()
        most_recent_birthyear = df['Birth Year'].max()
        most_common_birthyear = df['Birth Year'].mode()[0]
        print("\nThe earliest year of birth is ", int(earliest_birthyear))
        print("The most recent year of birth is ", int(most_recent_birthyear))
        print("The most common year of birth is ", int(most_common_birthyear))
    else:
        print('We have no information on the birth year of the customers in this city.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
