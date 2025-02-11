import numpy as np
import pandas as pd
import time
import warnings

# Turning off pandas future warning (one of the methods/functions is suppossed to be depracated!)
# source: https://stackoverflow.com/questions/15777951/how-to-suppress-pandas-future-warning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Read dataframe
csv_files = {
    'chicago' : 'chicago.csv',
    'newyork' : 'new_york_city.csv',
    'washington' : 'washington.csv'
}


# For mapping month from string format to numeric ones
month_dic =  {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'augest': 8, 'october': 9, 'september': 10, 'november': 11, 'december': 12}

# For mapping days of week from string format to numeric ones
day_dic =  {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}



# Get user input
def user_input():
    output = input('-> ').lower().replace(' ','')
    return output

# Get city name
def get_city():
    print('please write the name of the city: (newyork, chicago, washington)')
    output = input('-> ').lower().replace(' ','')
    return output

# Get month
def filter_month():
    month_check = input('Do you want to flter by month? (yes/no): ').lower().replace(' ','')
    month_name = None

    if 'yes' in month_check:
        i = 0
        while month_name not in month_dic:
            if i >= 1:
                print("Please write a value from this options:",
                    ", ".join(list(month_dic.keys()))
                    )
            month_name = input('Write month here: ').lower().replace(' ','')
            i+=1

        


    return month_name



# Get day
def filter_day():
    day_check = input('Do you want to flter by day? (yes/no): ').lower().replace(' ','')

    day_name = None

    if 'yes' in day_check:
        i = 0
        while day_name not in day_dic:
            if i >= 1:
                print(
                    "Please write a value between this options:",
                    ", ".join(list(day_dic.keys()))
                    )
            day_name = input('Write day of the week here: ').lower().replace(' ','')
            i+=1

    return day_name




# Cleaning the dataframe
def clean_df(city_name):
    df = pd.read_csv(csv_files[city_name])

    # Cleaning and changing data types
    df=df.drop(df.columns[0],axis=1)

    # Change Start Time and End Time data types
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])

    # change Birth Year data type to int (removing decimals)
    if city_name != 'washington':
        df['Birth Year']=df['Birth Year'].astype('Int64')
    return df

def month_filter(month:str,df:pd.DataFrame):
    return df[df['Start Time'].dt.month == month_dic[month]]

def day_filter(day:str,df:pd.DataFrame):
    return df[df['Start Time'].dt.dayofweek == day_dic[day]]


# all the needed operations to be applied over dataframe
def df_operation(df:pd.DataFrame,func:str,city_name):

    # For calculating the most popular hour
    if func == 'pop_hour':
        return df['Start Time'].dt.hour.mode()[0]
    
    # For finding the top 10 popular start stations
    elif func == 'pop_start_station':
        return "\n".join(df['Start Station'].value_counts()[:10].index.values)

    # For finding the top 10 popular end stations
    elif func == 'pop_end_station':
        return "\n".join(df['End Station'].value_counts()[:10].index.values)

    # For finding the top 10 popular start-end stations
    elif func == 'pop_start_end':
        df['start_end'] = df['Start Station']+ '-' + df['End Station']
        return "\n".join(df['start_end'].value_counts()[:10].index.values) 

    # For calculating total trip time in seconds
    elif func == 'total_trip_time':
        return int(df['Trip Duration'].sum()/3600)
    
    # For calculating the average trip time in minutes following by seconds
    elif func == 'avg_trip_time':
        return f"{int(df['Trip Duration'].mean()/60)}m and {int(df['Trip Duration'].mean()%60)}s"
    
    # Split user types into its categories
    elif func == 'user_type':
        output = list(zip(df['User Type'].value_counts(normalize=True).index.values , (df['User Type'].value_counts(normalize=True).values)))
        return "\n".join([f"{i[0]}: %{i[1]*100:.2f}" for i in output])

    # Split gender types into its categories
    elif func == 'gender_type':
        if city_name != 'washington':
            output = list(zip(df['Gender'].value_counts(normalize=True).index.values , df['Gender'].value_counts(normalize=True).values))
            return "\n".join([f"{i[0]}: %{i[1]*100:.2f}" for i in output])
        else:
            return False

    # Finding the oldest user
    elif func == 'earliest':
        if city_name != 'washington':
            return df['Birth Year'].min()
        else:
            return False
        
    # Finding the youngest user
    elif func == 'most_recent':
        if city_name != 'washington':
            df=df.sort_values(by=['Start Time'] , ascending=False)
            return int(df['Birth Year'].max())
        else:
            return False
    
    # Most common year of Birth
    elif func == 'most_common':
        if city_name != 'washington':
            df=df.sort_values(by=['Start Time'] , ascending=False)
            return int(df['Birth Year'].mode()) # most common
        else:
            return False



# Statistics result structure , it can be manipulate to and restructure as needed, all here
def options_dic():
    result_dic = [
        {
            'subject' : 'Popular time',
            'options' : [
                {
                    'title' : 'Most common hour of day',
                    'description' : 'is the most popular hour',
                    'func' : 'pop_hour'                   
                }
            ]
        },
        {
            'subject' : 'Popular stations and trip',
            'options' : [
                {
                    'title' : 'Top 10 common start stations',
                    'description' : '\nThese are the top 10 common start stations',
                    'func' : 'pop_start_station'
                },
                {
                    'title' : 'Top 10 common end stations',
                    'description' : '\nThese are the top 10 common end stations',
                    'func' : 'pop_end_station'
                },
                {
                    'title' : 'Top 10 common trip from start to end',
                    'description' : '\nThese are the top 10 common start-end stations',
                    'func' : 'pop_start_end'                
                }
            ]
        },
        {
            'subject' : 'Trip duration',
            'options' : [
                {
                    'title' : 'Total travel time',
                    'description' : 'is total trips in hours',
                    'func' : 'total_trip_time'
                },
                {
                    'title' : 'Average travel time',
                    'description' : 'is the average of each trip',
                    'func' : 'avg_trip_time'
                },
            ]
        },
        {
            'subject' : 'User info',
            'options' : [
                {              
                    'title' : 'Counts of each user type',
                    'description' : '',
                    'func' : 'user_type'
                },
                {
                    'title' : "Counts of each gender",
                    'description' : '',
                    'func' : 'gender_type'
                },
                {
                    'title' : "Earliest year of birth",
                    'description' : 'is the youngest person birth year',
                    'func' : 'earliest'
                },
                {
                    'title' : "Most recent year of birth",
                    'description' : 'is the most recent year of birth in last 1000 users on average',
                    'func' : 'most_recent'
                },
                {
                    'title' : "Most common year of birth",
                    'description' : 'is the birth year of users on average',
                    'func' : 'most_common'
                },
            ]
        },
    ]
    return result_dic

# Check the first 5 raw outputs
def raw_date(df:pd.DataFrame):
    user_input = input('Do you like to see first 5 raw of data?(yes/no)\n').lower().replace(' ','')
    if user_input == 'yes':

        # I should have search for this option (to display the full coulmns), I used stackoverflow
        # source: https://stackoverflow.com/questions/19124601/pretty-print-an-entire-pandas-series-dataframe
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df.head(5))

        # If user asked for more 
        i = 5
        while user_input == 'yes':
            user_input = input('Do you like to see the next 5 raw of data?(yes/no)\n').lower().replace(' ','')
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(df[i:i+5])
                i+=5
    else:
        pass




# main function
def main():
    while True:
        try:
            output = get_city()
            if output == 'exit':
                break
            else:
                df = clean_df(output)

                month = filter_month()
                if month is not None:
                    df = month_filter(month,df)
                
                day = filter_day()
                if day is not None:
                    df = day_filter(day , df)

                # Check if the dataframe output is empty
                if df.empty:
                    print(f"\nOoops! not data available for {output} city on {month} on {day}s.")
                
                else:
                    # Check first 5 raw data
                    raw_date(df)

                    # Iterating through descriptive statistics options
                    for options in options_dic():

                        print(f"\n\n|========================== {options['subject']} ==========================|\n")
                        for option in options['options']:
                            print(f"{option['title']}")
                            print()
                            if df_operation(df,option['func'],output):
                                print(
                                    df_operation(df,option['func'],
                                    output),
                                    option['description']
                                        )
                            else:
                                print(f"Oops! this data is not available in {output} city!")
                            print('\n..............................\n')  
                            time.sleep(1)

                
            print('\n\nDo you want to reset the program? (yes/no)\n')
            output = user_input().lower().replace(' ','')
            if output == 'exit' or output == 'no' or output == 'finish':
                break

        except KeyError:
            print('Wrong input!\n')

        except FileNotFoundError:
            print('Please check the data files directory, they should be in a data folder in the same directory of this file!\n')



if __name__ == "__main__":
    main()