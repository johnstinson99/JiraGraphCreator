import pandas as pd
from datetime import datetime

class JiraDFReader:

    def __init__(self, my_file_and_path_string):
        self.jira_df_before_processing = pd.read_csv(my_file_and_path_string)
        self.final_df = self.process_df(self.jira_df_before_processing)

    def get_final_df(self):
        return self.final_df

    def process_df(self, df):
        print("df_before_processing = ")
        print(str(df))
        # df['Datetime'] = [datetime.strptime(date_string, '%d %b %Y %H:%M') for date_string in df['Date']]# datetime.strptime(df['Date'], "%d %m %Y %H:%M")
        df['FromDate'] = pd.to_datetime(df['FromDate'])
        df['Date'] = pd.to_datetime(df['Date'])
        # df.Date.dt.hour
        df['DayDiff'] = (df['Date'] - df['FromDate']).astype('timedelta64[h]')/24
        df['HoursOfDay'] = df['Date'].dt.hour + df['Date'].dt.minute/60
        df['DayOfWeek'] = df['Date'].dt.weekday
        # df['MinutesOfDay'] = df['Date'].dt.minute
        # df['Minutes'] = [date_time.hours*60 + date_time.minutes
        #                  for date_time in df['Datetime']]
        # datestring = '01 Jan 2016 10:00'
        # my_datetime = datetime.strptime(datestring, '%d %b %Y %H:%M')
        # print("my_datetme = " + str(my_datetime))
        print(str(df))
        # date_df = df["Date"]
        # print('date_df = ')
        # print(str(date_df))
        return df

# TO add in the from date:
# Firstly do group by project and issue number, then sort by date,
        # and within each section add a counter
    # Or can we use the index which is already a counter?