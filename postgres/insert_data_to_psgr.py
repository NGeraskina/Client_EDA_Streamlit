import pandas as pd
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine


# Load .env file
load_dotenv()

host_db = os.getenv('HOST_DB')
user_db = os.getenv('USER_DB')
pswd_db = os.getenv('PSWD_DB')
name_db = os.getenv('NAME_DB')

conn_string = f'postgresql://{user_db}:{pswd_db}@{host_db}/{name_db}?sslmode=require'
db = create_engine(conn_string)
conn_eng = db.connect()


for name, link in zip(['clients',
                       'close_loans',
                       'job',
                       'last_credit',
                       'loan',
                       'pens',
                       'salary',
                       'target',
                       'work',],
                      ['https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_clients.csv',
                       'https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_close_loan.csv',
                       'https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_job.csv',
                       'https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_last_credit.csv',
                       'https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_loan.csv',
                       'https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_pens.csv',
                       'https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_salary.csv',
                       'https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_target.csv',
                       'https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/D_work.csv',]):
    df = pd.read_csv(link)
    print(df.info())
    df.to_sql(name, con=conn_eng, if_exists='replace',
              index=False)


# Close the cursor and connection
conn_eng.close()


