import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago','new york city','washington']
months = ['all','january','february','march','april','may','june']
weekdays = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
   
    city = input('Which city would you like to explore?\nChicago? New York City? Washington? ').lower()
    while city not in cities:
            city = input('Please check your city and enter it again: ').lower()

    month = input('Which month would you like to explore?\nAll? January? Feburary? March? April? May? June? ').lower()
    while month not in months:
            month = input('Please check your month and enter it again: ').lower()


    day = input('Which day in the week would you like to explore?\nAll? Monday? Tuesday? Wednesday? Thursday? Friday? Saturday? Sunday? ').lower()
    while day not in weekdays:
             day = input('Please check your day and enter it again: ').lower()

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def show_data(df):
    i = 0
    raw_data = input('Would you like to see the frist 5 rows of data? Yes or No? ').lower()
    while raw_data not in ('yes','no'):
        raw_data = input('Please reenter your answer! Yes or No? ').lower()
    if raw_data == 'yes':
        while True:
            print(df.iloc[i:i+5])
            i += 5
            more = input('Would you like to see the additional 5 rows of data? Yes or No? ').lower()
            if more != 'yes':
                break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df["Start Time"].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', months[popular_month].title())

    df['day'] = df["Start Time"].dt.weekday
    popular_day = df['day'].mode()[0]
    print('Most Popular Start Day:', weekdays[popular_day].title())

    df['hour'] = df["Start Time"].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    popular_start = df['Start Station'].mode()[0]
    print("Most popular Start Station: ", popular_start)

    popular_end = df['End Station'].mode()[0]
    print("Most popular End Station: ", popular_end)

    df['Start End'] = df['Start Station'].map(str) + ' to ' + df['End Station']
    popular_start_end = df['Start End'].mode()[0]
    print("Most popular Combination: ", popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    total_time = df['Trip Duration'].sum()/3600
    print("Total travel time in hour: ", total_time, ' hours')

    mean_time = df['Trip Duration'].mean()/3600
    print("Average travel time: ", mean_time, ' hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    user_types = df['User Type'].value_counts()
    print('The number of each user type: \n',user_types)

    print('')

    try:
        gender = df["Gender"].value_counts()
        print('Gender: \n', gender)
    except:
        print('There is no gender information')
    print('')

    try:
        earliest = df["Birth Year"].min()
        latest = df["Birth Year"].max()
        most_common = df["Birth Year"].mode()[0]
        print('The earliest birth year: ', int(earliest))
        print('The most recent birth year: ', int(latest))
        print('The most popular birth year: ', int(most_common))
    except:
        print('There is no birth year information')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        show_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
