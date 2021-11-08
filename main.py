import pandas as pd
from sqlalchemy import create_engine
import numpy as np

if __name__ == '__main__':

    connection = create_engine('sqlite:///data.db')

    #force pandas to use schema for certain columns
    pandas_schema = {"nr_cnpj": str, "nr_cpf_cnpj_socio": str, "in_cpf_cnpj": np.int32}

    print('Starting to read the zip file')
    df = pd.read_csv("cnpj_qsa.zip", dtype=pandas_schema, encoding='utf-8', sep='\t', compression='zip')
    print("The CSV has been read in")

    print('The data is being written to the SQLite DB. This may take a few minutes')
    df.to_sql(name='companies', if_exists='replace', con=connection, index=False, chunksize=10000)
    print("The data has been written to the DB")

    #close the connection to the database
    connection.dispose()