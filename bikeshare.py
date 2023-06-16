import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
        city = input("What is the city you would like to analyze? (Chicago, New York City, or Washington): ").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('\nThat is not a valid city. Please try again. (Make sure you have entered either Chicago, New York City, or Washington') #Specify correct inputs

            
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to filter by? (all, january, february, ... , june): ").lower() #update
        if month in MONTHS or month == 'all':
            break
        else:
            print('\nThat is not a valid month. Please try again.') #Specify correct inputs

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day of the week would you like to filter by? (all, monday, tuesday, ... , sunday): ").lower() #update
        if day in DAYS or day == 'all':
            break
        else:
            print('That is not a valid day. Please try again.') #Specify correct inputs

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
    filename = CITY_DATA.get(city)
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'all':   
        month = MONTHS.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        day = DAYS.index(day)
        df = df[df['Day'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    popular_month = MONTHS[popular_month -1]
    print("Most Common Month:", popular_month.title())

    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    popular_day = DAYS[popular_day]
    print("Most Common Day:", popular_day.title())

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print("Most Common Start Hour:", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print("Most Common Start Station:", pop_start)

    # display most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print("Most Common End Station:", pop_end)

    # display most frequent combination of start station and end station trip
    df['Start_End'] = df['Start Station'] + " and " + df['End Station']
    pop_start_end = df['Start_End'].mode()[0]
    print("Most Frequent Combination of Start Station and End Station Trip:", pop_start_end)
    df.drop(['Start_End'], axis = 1, inplace = True)   #dropping added start & end column that was used for finding most frequent combo 
    

    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum())
    print("Total Tavel Time (seconds):", total_travel_time)
    
    # display mean travel time
    avg_travel_time = round(df['Trip Duration'].mean())
    print("Average Travel Time (seconds)", avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    user_types = df['User Type'].value_counts()
    print(user_types)
    

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('\n',gender)  
    else:
        print("\nThe city you selected does not include gender data.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("\nEarliest Birth Year:", round(df['Birth Year'].min()))
        print("Most Recent Birth Year:", round(df['Birth Year'].max()))
        print("Most Common Birth Year:", round(df['Birth Year'].mode()[0]))
    else:
        print("\n The city you selected does not include birth year data.")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def yes_or_no(question):
    """Requires yes or no response from user.

    Returns:
    (str) answer - user input, either yes or no. """

    while True:
        answer = input(question)
        if answer.lower() in ['yes', 'no']: 
            break
        else:
            print("\nInvalid input. Please make sure you have entered either Yes or No.")
    return answer


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        
        show_data = yes_or_no('\nWould you like to see the first 5 lines of the raw data? (Enter Yes or No): ')
        i = 0
        
        while (show_data.lower() == 'yes') and (i+5 <= len(df.index)):
            print(df.iloc[i:i+5,:])
            show_data = yes_or_no('\nWould you like to see 5 more lines of data? (Yes or No): ')
            i += 5
           
        restart = yes_or_no('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
