import pickle
import pandas as pd
from datetime import datetime, timedelta
import sys
import warnings
warnings.filterwarnings('ignore')

def get_date_list(n):
  date_str = '03-25-2019'
  date_object = datetime.strptime(date_str, '%m-%d-%Y').date()
  date_list = [date_object + timedelta(days=(i+1)) for i in range(n)]
  df = pd.DataFrame(date_list)
  df.columns = ['date']
  return df

def create_features_pred(df):
    """
    Create time series features based on time series index.
    """

    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    df = df.copy()
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofmonth'] = df.index.day
    df['dayofweek'] = df.index.dayofweek

    return df

def model_predict(date_list):

  model = pickle.load(open('finalized_model.sav', 'rb'))

  date_list['sales'] = model.predict(date_list[['month', 'year', 'dayofmonth', 'dayofweek']])
  date_list = date_list.reset_index()

  return date_list[['date', 'sales']]

if __name__ == "__main__":
    n = int(sys.argv[1])
    date_list = get_date_list(n)
    date_list = create_features_pred(date_list)
    output = model_predict(date_list)
    print(output)

# H:\D_drive\dim_assignment\dim_tech_assignmrnt\finalized_model.sav
