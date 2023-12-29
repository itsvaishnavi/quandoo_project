import pandas as pd
import pymysql
from sqlalchemy import create_engine
from constants import Constants

class LoadData:
	def __init__(self, csv_file_path, table):
		self.csv_file_path = csv_file_path
		self.table = table

	def credentials(self):
		c = Constants()
		c.local(2)

		self.host = c.host
		self.user = c.user
		self.password = c.password
		self.database = c.database 

	def connect_and_insert_data(self):
		try:
			engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}")

			df = pd.read_csv(self.csv_file_path)

			df.to_sql(self.table, con=engine, index=False)

			engine.dispose()
			print("initial data inserted successfully....")
		except Exception as e:
			print(e)

# l = LoadData("Data_exported_from_db.csv","restaurant_db")
# l.credentials()
# l.connect_and_insert_data()