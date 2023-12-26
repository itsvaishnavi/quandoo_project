from data_storage import DataStorage_SQL
from datetime import date

class DataMart:
	def __init__(self):
		self.ds = DataStorage_SQL()
		

	# Calculated data of how much cuisine types are ingested per price range

	# Calculated data of review ratings per cuisine type

	# Count of different cuisines ingested
	def get_cuisines_count(self):
		self.cuisines_set = set()
		self.ds.cursor.execute("select distinct CUISINES from restaurant_db")

		records = self.ds.cursor.fetchall()

		for row in records:
			raw = row[0].replace("[","").replace("]","").replace("'","").split(",")

			for c in raw:
				if c!='':
					self.cuisines_set.add(c.strip())

		print(self.cuisines_set)
		return {"operation":"cuisine count","date":date.today().strftime("%Y-%m-%d"), "cuisine_count":len(self.cuisines_set)}

	# count of restaturants by cuisine
	def count_rest_by_cuisine(self):
		data = dict()
		data["date"] = date.today().strftime("%Y-%m-%d")
		data["operation"] = "count of restaturants by cuisine"
		query = "select count(*) from restaurant_db where CUISINES like %s"
		print(query)
		for c in self.cuisines_set:
			pattern = '%' + c + '%'
			self.ds.cursor.execute(query,(pattern,))

			result = self.ds.cursor.fetchone()[0]
			data[c] = result

		return data

	# count of restaurants by $ and geo_id
	def get_tag_geo(self):
		self.tag_set = set()
		data_list = []
		self.ds.cursor.execute("select tags from restaurant_db")

		records = self.ds.cursor.fetchall()

		for row in records:
			raw = row[0].replace("[","").replace("]","").replace("'","").split(",")[0]

			
			pattern = "\"%'"+raw+'\'%"'
			# print(pattern)

			self.tag_set.add(pattern)

		for p in self.tag_set:
			data = {}
			query = "select %s, geo_id, count(rest_name) from restaurant_db where tags like %s group by geo_id"%(p,p,)
			# print(query)
			self.ds.cursor.execute(query)
			result = self.ds.cursor.fetchone()
			
			data["operation"] = "count of restaurants by $ and geo_id"
			data["date"] = date.today().strftime("%Y-%m-%d")
			data["tags"] = result[0].replace("'","").replace("%","").replace(",","")
			data["geo_id"] = result[1]
			data["rest_count"] = result[2]
			data_list.append(data)

		return data_list

		# count of restaurants by $ and geo_id
	def get_cuisine_geo(self):
		data_list = []
		for p in self.cuisines_set:
			print(p)
			data = {}
			pattern = "\"%'"+p+'\'%"'
			query = "select %s, geo_id, count(rest_name) from restaurant_db where CUISINES like %s group by geo_id"%(pattern,pattern,)
			print(query)
			self.ds.cursor.execute(query)
			result = self.ds.cursor.fetchone()
			
			data["operation"] = "count of restaurants by $ and geo_id"
			data["date"] = date.today().strftime("%Y-%m-%d")
			data["tags"] = result[0].replace("'","").replace("%","").replace(",","")
			data["geo_id"] = result[1]
			data["rest_count"] = result[2]
			data_list.append(data)

		return data_list

dm = DataMart()

print(dm.get_cuisines_count())
print(dm.count_rest_by_cuisine())
print(dm.get_tag_geo())
print(dm.get_cuisine_geo())
# python3 load_csv_to_db.py ; uvicorn app:app --reload --host 0.0.0.0 --port 8000;