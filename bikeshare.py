import time
import pandas as pd
import numpy as np
import datetime

# Static data structures
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_LIST = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
DAY_LIST = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
MONTH_LIST_INV = {MONTH_LIST[k]: k.capitalize() for k in MONTH_LIST}
DAY_LIST_INV = {DAY_LIST[k]: k.capitalize() for k in DAY_LIST}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington?')
        if city.lower() in CITY_DATA:
            break
        print('ERROR: City does not match.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Type month (January, February, March, April, May or June) to filter by or type 'all' for no filter")
        if month.lower() in MONTH_LIST or month.lower() == 'all':
            break
        print("ERROR: Input was not a month from January to June nor all.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Type day of the week to filter or type 'all' for no filter")
        if day.lower() in DAY_LIST or day.lower() == 'all':
            break
        print("ERROR: Input was not a day of the week nor all.")

    print('-'*40)
    return city, month, day


def load_data(city, month='all', day='all'):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city.lower()]).rename(columns={'Unnamed: 0': 'Trip Id'})
    cols = df.columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.dayofweek
    df['Start Hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month.lower() in MONTH_LIST:
        n_month = MONTH_LIST[month.lower()]
        df = df.loc[df['Month'] == n_month]

    # Filter by day of the week if applicable
    if day.lower() in DAY_LIST:
        n_day = DAY_LIST[day.lower()]
        df = df.loc[df['Day of Week'] == n_day]

    return df, cols


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    aux = df[['Month','Start Time']].groupby('Month').count()['Start Time']
    month_max = aux.idxmax()
    month_max_cnt = aux.max()
    print("Most common month was {} with {} trips.".format(MONTH_LIST_INV[month_max], month_max_cnt))

    # display the most common day of week
    aux = df[['Day of Week','Start Time']].groupby('Day of Week').count()['Start Time']
    day_max = aux.idxmax()
    day_max_cnt = aux.max()
    print("Most common day of the week was {} with {} trips.".format(DAY_LIST_INV[day_max], day_max_cnt))

    # display the most common start hour
    aux = df[['Start Hour','Start Time']].groupby('Start Hour').count()['Start Time']
    hour_max = aux.idxmax()
    hour_max_cnt = aux.max()
    print("Most common start hour was {} with {} trips.".format(str(hour_max)+":00", hour_max_cnt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    aux = df[['Start Station','Start Time']].groupby('Start Station').count()['Start Time']
    station_max = aux.idxmax()
    station_max_cnt = aux.max()
    print("Most common start station was {} with {} trips.".format(station_max, station_max_cnt))


    # display most commonly used end station
    aux = df[['End Station','Start Time']].groupby('End Station').count()['Start Time']
    station_max = aux.idxmax()
    station_max_cnt = aux.max()
    print("Most common end station was {} with {} trips.".format(station_max, station_max_cnt))


    # display most frequent combination of start station and end station trip
    df_copy = df.copy()
    df_copy['Station Combination'] = df_copy['Start Station'] + " - " + df_copy['End Station']
    aux = df_copy[['Station Combination','Start Time']].groupby('Station Combination').count()['Start Time']
    station_max = aux.idxmax()
    station_max_cnt = aux.max()
    print("Most common combination of start - end station was {} with {} trips.".format(station_max, station_max_cnt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    val = df['Trip Duration'].sum()/3600
    print("Total trip duration was {:.2f} hours".format(val))

    # display mean travel time
    val = df['Trip Duration'].mean()/60
    print("Average trip duration was {:.2f} minutes".format(val))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    aux = df[['User Type','Start Time']].groupby('User Type').count()
    aux = aux.reset_index().rename(columns={'Start Time': 'Count'})
    print("User Type statistics:")
    print(aux.to_string(index=False))


    # Display counts of gender
    if 'Gender' in df.columns:
        aux = df[['Gender','Start Time']].groupby('Gender').count()
        aux = aux.reset_index().rename(columns={'Start Time': 'Count'})
        print("\nGender statistics:")
        print(aux.to_string(index=False))
    else:
        print("\nThere is no gender information available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df[['Birth Year']].mode().loc[0,'Birth Year'])
        this_year = datetime.date.today().year
        print("\nEarliest birth year was {} (aged {} aprox.)".format(earliest_birth_year, this_year-earliest_birth_year))
        print("Most recent birth year was {} (aged {} aprox.)".format(most_recent_birth_year, this_year-most_recent_birth_year))
        print("Most common birth year was {} (aged {} aprox.)".format(most_common_birth_year, this_year-most_common_birth_year))
    else:
        print("There is no birth year information available for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data (trips sample)."""

    print('\nDisplaying individual trip sample...\n')
    start_time = time.time()

    cnt = 0
    rows = 5
    while True:
        if cnt+rows < df.shape[0]:
            aux = df.iloc[cnt:cnt+rows]
            print("\n" + aux.to_string(index=False))
            cnt += rows
            answer = input("Do you want to see more individual trips? (yes or no)")
            if answer != "yes":
                break
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():

    while True:
        city, month, day = get_filters()
        df, cols = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df[cols])

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
