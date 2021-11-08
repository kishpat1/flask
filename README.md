**Steps to follow to get the API running**
1. Run script to set up environment variables and install requirements
a. `source env_setup.sh`
2. Run script to read in zip file of data and write to sqlite DB 
           a.`python3 main.py`
3. Get API running
              a.`flask run`

These are the following endpoints to use:

http://127.0.0.1:5000/companies?operator=HOMERO%20CARLOS%20DE%20SOUZA

http://127.0.0.1:5000/operators?company=RAFAEL%20COUROS%20LIMITADA

http://127.0.0.1:5000/graph?company=RAFAEL%20COUROS%20LIMITADA

**Architecture Discussion**
The main.py script reads in the CSV zip file of Brazilian companies, creates a sqlite DB, 
and writes the data to the DB. Brazilian Portuguese has different characters from English, so I had to
ensure that the encoding (utf-8) would handle all potential characters.

Pandas is used to read the file and write to the DB. I chose this approach because simplicity was valued over
performance. This also isn't a concern because the data just
needs to be transferred once.

SQLite was used as the RDBMS because all data could reside in 1 file, as opposed to a more complicated structure, like that of PostgreSQL or MySQL.

I chose Flask as the framework because it is more lightweight snd easier to setup than Django.

The Flask queries the DB and has 3 endpoints, 1 for each of the following actions:
get all operators from a given company,
get all companies from a given operator,
and get all companies that a share an operator with a given company.
