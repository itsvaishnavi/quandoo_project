Please refer Readme.pdf for more details

You can find the scraped data of the restaurants in the Data_exported_from_db.csv file. 

How to reproduce the project

(A) Using docker-compose.yml

Step 1: Download the project zip file

Step 2: Install the docker

Step 3: Run the docker-compose.yml using the following command

docker-compose up

If running for the first time, use the following command

docker-compose up –build

Step 4: Access the endpoints: /scrape_data/{geo_id} and /retreive_data/{geo_id}

(B) Without using docker

Step 1: Download and extract the project zip file

Step 2: Install Python and Mysql workbench

Step 3: On the command prompt, go to the project folder.

Step 4: Create virtual environment
python -m venv venv

Step 5: Activate the virtual environment
(On windows) venv\Scripts\activate

pip install -r requirements.txt

Step 6: Connect to MySQL database

Step 7: Run load_csv_to_db.py to load the data to database

python load_csv_to_db.py

Step 6: Run app.py 

uvicorn app:app
