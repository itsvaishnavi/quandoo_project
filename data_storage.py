# Import essential libraries
from constants import Constants
import pymysql
import pandas as pd
from datetime import datetime

# Database connection and operations
class DataStorage_SQL:
	# Connect to database
	def __init__(self):
		c = Constants()

		# 2 represents that we want to connect to the docker image db so fetching the right credentials
		c.local(2)
		# self.connection = pymysql.connect(user=c.user,password=c.password,host=c.host,database=c.database)
		
		self.connection = pymysql.connect(user=c.user,password=c.password,host=c.host,database=c.database)
		
		print("Database connected successfully...")

		self.cursor = self.connection.cursor()
		
	# Create table
	def create_table(self):
		query = """ 
			create table restaurant_db(
			url varchar(255),
			restaurant_id varchar(50) primary key,
			fetch_count int,
			time_of_fetching_data varchar(100),
			rating float,
			rest_name varchar(255),
			address varchar(255),
			telephone varchar(255),
			website varchar(255),
			tags varchar(255),
			CUISINES varchar(255),
			Special_Diets varchar(255),
			Meals varchar(255),
			is_michelin varchar(3),
			menu_link_available varchar(3),
			neighborhood varchar(255),
			restaurant_rank varchar(255),
			Food_Rating float,
			Value_Rating float,
			Service_Rating float,
			Atmosphere_Rating float,
			PRICE_RANGE varchar(100),
			FEATURES text,
			total_reviews int,
			menu_link varchar(255),
			geo_id varchar(20)
		);

		"""
		self.cursor.execute(query)

		print("Table created successfully...")

	# Check if record with requested restaurant_id already exists. If yes, return 1, else return 0
	def check_if_record_exists(self, restaurant_id):
		val = 0
		query = "select count(*) from restaurant_db where restaurant_id=%s"

		self.cursor.execute(query,(restaurant_id,))

		result = self.cursor.fetchone()[0]

		if result > 0:
			print("Record with "+restaurant_id+" exists...")
			val = 1

		else:
			val = 0

		print(val)
		return val

	# Insert data
	def insert_data(self, **restaurant_details:dict):
		# print(restaurant_details["restaurant_id"])
		val = self.check_if_record_exists(restaurant_details["restaurant_id"])

		# If data does not exists
		if val == 0:
			columns = ','.join(x for x in tuple(restaurant_details.keys()))

			val = tuple(restaurant_details.values())
			query = "insert into restaurant_db (%s) values %s;" %(columns,tuple(restaurant_details.values()))
			print(query)
			self.cursor.execute(query)
			self.connection.commit()
			print("Data inserted successfully...")

		else:
			pass


	# This function fetches the data for requested geo_id
	def fetch_data_by_geo_id(self, geo_id):
		query = "select * from restaurant_db where geo_id=%s"
		self.cursor.execute(query,(geo_id,))
		records = self.cursor.fetchall()
		return records

	# This function fetches all data from the database
	def retreive_data(self):
		self.cursor.execute("select * from restaurant_db")

		records = self.cursor.fetchall()

		for r in records:
			print(r)

	def close_connection(self):
		self.connection.close()


# This class deals with creating the csv file using pandas
class DataStorage_Dataframe:
	def __init__(self):
		self.rows = []
		pass

	# Add dictionary to self.rows[]
	def add_record(self, **restaurant_details):
		self.rows.append(restaurant_details)

	# Create dataframe
	def create_dataframe(self):
		self.df = pd.DataFrame.from_dict(self.rows, orient='columns')

	# Create CSV
	def store_as_csv(self):
		self.df.to_csv("restaurant_details_"+datetime.now().strftime("%d_%m_%Y_%H_%M_%S")+".csv", encoding='utf-8')

	# Display data
	def show_dataframe(self):
		self.df.head()


# d = {'url': 'https://www.tripadvisor.com/Restaurant_Review-g187147-d19261302-Reviews-Miura-Paris_Ile_de_France.html', 'restaurant_id': 'd19261302', 'geo_id': '187147', 'fetch_count': 1, 'time_of_fetching_data': '23/12/2023 16:28:30', 'total_reviews': 159, 'rating': 5.0, 'rest_name': 'Miura', 'address': "15, rue de l'Arc de Triomphe, 75017 Paris France", 'telephone': '+33 1 47 54 00 28', 'website': '', 'tags': "['$$$$', 'French', 'European', 'Contemporary']", 'CUISINES': "['French', 'European', 'Healthy', 'Contemporary']", 'Special_Diets': '', 'Meals': "['Lunch', 'Dinner', 'Drinks']", 'is_michelin': 'No', 'menu_link_available': 'No', 'menu_link': '', 'neighborhood': '17th Arr. - Batignolles-Monceau0.2 miles from Arc de Triomphe', 'restaurant_rank': '#23 of 14,523 Restaurants in Paris', 'Food_Rating': 0.0, 'Service_Rating': 0.0, 'Value_Rating': 0.0, 'Atmosphere_Rating': 0.0, 'PRICE_RANGE': "['$65 - $94']", 'FEATURES': "['Reservations', 'Seating', 'Serves Alcohol', 'Full Bar', 'Accepts Credit Cards', 'Table Service', 'Private Dining', 'Street Parking', 'Wine and Beer', 'Dog Friendly', 'Non-smoking restaurants', 'Gift Cards Available']"}

# ds=DataStorage_SQL()

# ds.insert_data(**d)