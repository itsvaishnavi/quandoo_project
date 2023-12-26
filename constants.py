class Constants:
	base_url = "https://www.tripadvisor.com/RestaurantSearch?Action=PAGE&geo={}&sortOrder=relevance&o=a%7Bpage_number%7D"
	
	next_page_url = "https://www.tripadvisor.com/RestaurantSearch?Action=PAGE&geo={}&sortOrder=relevance&o=a"
	
	

	# Set val=1 in data_storage.py to connect to local database and val=2 if using docker
	def local(self, val):
		if val == 1:
			self.user='root'
			self.password='root'
			self.host='localhost'
			self.port=3306
			self.database='db'

		if val == 2:
			self.user='root'
			self.password='password'
			self.host='my-db-1'
			self.port=6033
			self.database='db'