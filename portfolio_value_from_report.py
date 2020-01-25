import pandas as pd




def pv_from_report(old,report):
    file_old = pd.read_csv(old,parse_dates=['Date'])



    file_new = pd.read_csv(report,skiprows=2,parse_dates=['Date'])

    file_new=file_new.drop(file_new.columns[[0,1]], axis=1)[:-1].rename(columns={'NAV':'total_value','Cash':'cash'})
    file_new=file_new[['Date','cash','total_value']]
    file_new['broker_id']=3
    file_new['account_number']=2530531
    file_new['currency']='USD'
    file_new['portfolio_value']=file_new['total_value']-file_new['cash']






    new_df = pd.concat([file_old,file_new],sort=False).reset_index(drop=True)


    new_df = new_df.drop_duplicates(subset='Date',inplace=False)

    sorted_df= new_df.sort_values('Date')
    new_df = sorted_df

    new_df.set_index('Date')
    new_df.to_csv(old)



pv_from_report('/Users/joanarau-schweizer/PycharmProjects/stockbot/db/mysql_db_csv/portfolio_value/2530531.csv','/Users/joanarau-schweizer/Downloads/joan_m_Arau_Schweizer_January_02_2020_January_21_2020.csv')
