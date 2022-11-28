# Minor trouble-shooting guidance was found on QA websites such as Stack Overflow.
# A new function has been added in response to reviewer ("data_display") to enable the user to view subsets of the filtered data frame

import time
import calendar as cdr
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_columns', 15)

CITY_DATA = { 'chicago': 'chicago.csv','new york': 'new_york_city.csv','washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter the name of the city you are interested in (Chicago, New York or Washington): ").lower()
        if city not in ("chicago", "new york", "washington"):
            print("\nThat spelling is incorrect, please try again.\n")
        else:
            break
    print("You have selected: {}".format(city.title()))
    print()
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to review (January, February, March, April, May, June, or All?: ").lower()
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("\nThat spelling is incorrect, please try again.\n")
        else:
            break
    print("You have selected: {}".format(month.title()))
    print()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of the week would you like to review (Sunday, Monday, etc., or All)?: ").lower()
        if day not in ("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"):
            print("\nThat spelling is incorrect, please try again.\n")
        else:
            break
    print("You have selected: {}".format(day.title()))
    print()
    print('-'*40)
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
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['start_hour'] = df['Start Time'].dt.hour
    df['end_hour'] = df['End Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != ('all'):
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != ('all'):
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month   
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', cdr.month_name[popular_month])

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week:', popular_day)

    # display the most common start hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['start_hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df["combo_stations"] = "From " + df['Start Station'] + " " + "to" + " " + df['End Station']
    popular_stations = df['combo_stations'].mode()[0]
    print('Most Common Combination of Start and End Stations:', popular_stations)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_travel_time = np.sum(df['Trip Duration'])
    total_days_travel_time = sum_travel_time/60/60/24
    print('Total Travel Time: {} days'.format(total_days_travel_time))
    
    # display mean travel time
    mean_travel_time = (np.mean(df['Trip Duration']))/60
    print('Average Trip Duration: {} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' not in df:
        print("No Gender information available")
    else:
        female_count = np.sum(df['Gender'] == 'Female')
        print('Total number of female riders: ', female_count)
        male_count = np.sum(df['Gender'] == 'Male')
        print('Total number of male riders: ', male_count)
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print("No Birth Year information available")
    else:
        earliest_dob = np.min(df['Birth Year'])
        print('Earliset year of birth: ', int(earliest_dob))
        recent_dob = np.max(df['Birth Year'])
        print('Most recent year of birth: ', int(recent_dob))
        most_common_dob = df['Birth Year'].mode()[0]
        print('Most common year of birth: ', int(most_common_dob))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_display(df):
    """Queries the user whether they want to view at least five rows of data from the data frame."""
    while True:    
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no? \n").lower()
        if view_data.lower() != "yes":
            break
        else:
            start_loc = 0
            row_count = len(df.index)
            while (start_loc < row_count):
                print(df.iloc[start_loc:(start_loc + 5)])
                start_loc += 5
                view_display = input("\n Do you wish to see five more rows of data? Enter yes or no: \n").lower()
                if view_display.lower() != 'yes':
                    break
            break

def main():
    """Runs each of the functions based on user inputs."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_display(df)

        restart = input('\nWould you like to restart and select a new city? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
