import unittest
from data_storage import DataStorage_SQL
from scraper import Scraper
import requests

class Test(unittest.TestCase):
	# Send a valid request to the API endpoint
	def valid_request_test(self):
		response = requests.get("http://127.0.0.1:8000/")
		print(response)
		self.assertEqual(response.status_code, 200)

	# Send an invalid request 
	def invalid_request_test(self):
		response = requests.get("http://127.0.0.1:8000/retreive_data/187323002")
		self.assertEqual(response.status_code, 400)

	# Test current data count
	def data_count_test(self):
		ds = DataStorage_SQL()
		query = "select count(*) from restaurant_db"
				
		ds.cursor.execute(query)
		cnt = self.cursor.fetchone()[0]

		self.assertEqual(cnt,138)

	# Test insert query
	def insert_query_test(self):
		ds = DataStorage_SQL()
		query = "insert into restaurant_db(restaurant_id,url) values('test123','www.test.com');"
		
		try:
			ds.cursor.execute(query)
			ds.connection.commit()

		except:
			test_val = 0

		else:
			test_val = 1

		self.assertEqual(test_val,1)

	# Test if record with restaurant_id exists (This restaurant_id exists)
	def restaurant_id_test(self):
		ds = DataStorage_SQL()
		val = ds.check_if_record_exists('d4261461')
		self.assertEqual(val,0)

	# Test Scraper class
	
	def test_Scraper_class(self):
		ds = DataStorage_SQL()
		test_val = 0

		try:
			s = Scraper("187147")

			url = "https://www.tripadvisor.com/Restaurant_Review-g187147-d19261302-Reviews-Miura-Paris_Ile_de_France.html"
			s.start_base_url(url)
			s.get_restaurant_details()

			ds.insert_data(**s.restaurant_details)
			print("Record inserted successfully...")

		except Exception as e:
			test_val = 0
			print(e)

		else:
			test_val = 1

		self.assertEqual(test_val,1)
	
if __name__ == '__main__':
	unittest.main()