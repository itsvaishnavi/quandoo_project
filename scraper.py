# Import essential libraries
from constants import Constants as c
from data_storage import DataStorage_Dataframe
from data_storage import DataStorage_SQL
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

# Scraper class
class Scraper:
	# Constructor requires geo_id parameter
	def __init__(self, geo_id):
		self.geo_id = geo_id

		# list of individual restaurant URL
		self.url_list = []

		# Dictionary format of restaurant details
		self.restaurant_details = {'url': '', 'restaurant_id': '', 'geo_id':'',\
		 'fetch_count' : 0,\
		 'time_of_fetching_data': '', 'total_reviews': 0, 'rating': 0.0, 'rest_name': '', 'address': '', 'telephone': '',\
		 'website': '', 'tags': '', 'CUISINES': '', 'Special_Diets': '',\
		 'Meals': '', 'is_michelin': '', 'menu_link_available': '', 'menu_link': '', 'neighborhood': '', 'restaurant_rank': '',\
		 'Food_Rating':0.0, 'Service_Rating':0.0, 'Value_Rating':0.0, 'Atmosphere_Rating':0.0, 'PRICE_RANGE':'', 'FEATURES':''}

		# Webdriver selenium 
		options = webdriver.ChromeOptions()
		options.add_argument("--headless")
		options.add_argument("--disable-gpu")
		options.add_argument("--no-sandbox")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])

		self.driver = webdriver.Chrome(options=options)

	# Connect to URL
	def start_base_url(self, url):
		self.url = url
		print(self.url)
		self.driver.get(self.url)

	# Get the list of individual restaurant URL
	def get_restaurant_urls(self):
		
		test_ele = self.driver.find_elements(By.CLASS_NAME, "Lwqic.Cj.b")
		
		for item in test_ele:
			# print(item.get_attribute('href'))
			self.url_list.append(item.get_attribute('href'))

		time.sleep(20)


	# Get individual restaurant data from the URL
	def get_restaurant_details(self):
		# Based on the geo_id and restaurant URL
		self.restaurant_details['geo_id'] = self.geo_id
		self.restaurant_details['url'] = self.url
		self.restaurant_details['restaurant_id'] = self.url.split("/")[-1].split("-")[-4]
		self.restaurant_details['time_of_fetching_data'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

		# Get the data using the class name from the html page
		self.restaurant_details["total_reviews"] = int(self.driver.find_element(By.CLASS_NAME, "BMQDV._F.Gv.wSSLS.SwZTJ").find_element(By.CLASS_NAME, "AfQtZ").get_attribute('textContent').split(" ")[0].replace(",",""))

		self.restaurant_details["rating"] = float(self.driver.find_element(By.CLASS_NAME, "UctUV.d.H0").get_attribute('aria-label').split(" ")[0])

		self.restaurant_details["rest_name"] = self.driver.find_element(By.CLASS_NAME, "HjBfq").get_attribute('textContent')
		self.restaurant_details["address"] = self.driver.find_element(By.XPATH, "//*[contains(@href, '#MAPVIEW')]").get_attribute('textContent')
		self.restaurant_details["telephone"] = self.driver.find_element(By.XPATH, "//*[contains(@href, 'tel:')]").get_attribute('textContent')

		try:
			self.restaurant_details["website"] = self.driver.find_element(By.CLASS_NAME, "YnKZo.Ci.Wc._S.C.AYHFM").get_attribute('href')
		except:
			self.restaurant_details["website"] = ''


		tags_element = self.driver.find_elements(By.CLASS_NAME, "dlMOJ")

		self.restaurant_details["tags"] = []

		for t in tags_element:
			self.restaurant_details["tags"].append(t.get_attribute('textContent'))

		self.restaurant_details["tags"] = str(self.restaurant_details["tags"])

		try:
			is_michelin_element = self.driver.find_element(By.CLASS_NAME, "dfbUL.S4.b.H3')]")

		except Exception as e:
			self.restaurant_details["is_michelin"] = "No"

		else:
			self.restaurant_details["is_michelin"] = "Yes"

		try:

			reviews_list = self.driver.find_element(By.CLASS_NAME, "UpQlM")

			count_of_li = len(reviews_list.find_elements(By.XPATH,"./ul/li"))

			for i in range(1, count_of_li+1):
				txt = reviews_list.find_element(By.XPATH,"./ul/li["+str(i)+"]").get_attribute('textContent').split(":")

				self.restaurant_details[txt[0] + "_Rating"] = float(txt[1])

		except:
			pass

		try:
			menu_link_element = self.driver.find_element(By.CLASS_NAME, "DsyBj.cNFrA.AsyOO')]").find_element(By.XPATH, "./a")

		except Exception as e:
			self.restaurant_details["menu_link_available"] = "No"
			self.restaurant_details["menu_link"] = ""

		else:
			self.restaurant_details["menu_link_available"] = "Yes"
			self.restaurant_details["menu_link"] = menu_link_element.get_attribute('href')

		try:
			self.restaurant_details["neighborhood"] = self.driver.find_element(By.CLASS_NAME, "yEWoV.OkcwQ").get_attribute('textContent')
		except:
			pass

		try:
			self.restaurant_details["restaurant_rank"] = self.driver.find_element(By.CLASS_NAME, "DsyBj.cNFrA").find_element(By.XPATH, "./a").get_attribute('textContent')
		except:
			pass
			
		self.restaurant_details["fetch_count"] = 1

		try:

			features_list_ele = self.driver.find_element(By.CLASS_NAME, "OTyAN._S.b")
			features_list_ele.click()

			# print(self.restaurant_details)
			

			super_ele = self.driver.find_element(By.CLASS_NAME, "kqcdz").find_element(By.XPATH, "./div/div/div[2]/div")
			sub_ele = super_ele.find_elements(By.XPATH, "./div")


			total_divs = len(sub_ele)

			# print(total_divs)

			for i in range(1, total_divs+1):

				self.restaurant_details[super_ele.find_element(By.XPATH,"./div["+str(i)+"]/div[contains(@class, 'tbUiL b')]").get_attribute('textContent').replace(' ','_')] = \
				 str([x.strip() for x in super_ele.find_element(By.XPATH,"./div["+str(i)+"]/div[contains(@class, 'SrqKb')]").get_attribute('textContent').split(",")])
		
		except Exception:
			try:
				details_box = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Details')]")

			except:
				pass

			else:
				col = details_box.find_elements(By.XPATH, "//*[contains(@class, 'ui_column  ')]")

				for l in col:
					try:
						t_div = l.find_elements(By.XPATH, "./div")

						for i in range(1, len(t_div)+1):
							self.restaurant_details[l.find_element(By.XPATH,"./div["+str(i)+"]/div[contains(@class, 'CtTod Wf b')]").get_attribute('textContent').replace(' ','_')] = \
				 str([x.strip() for x in l.find_element(By.XPATH,"./div["+str(i)+"]/div[contains(@class, 'AGRBq')]").get_attribute('textContent').split(",")])

					except:
						pass


		print(self.restaurant_details)
		

		# time.sleep(120)

	def parse_base_url(self, geo_id):
		self.get_restaurant_urls()
		
		# Offset value is 30 (information from the tripadvisor.com web page)
		step = 30 

		# i indicates the page number
		# We are fetching the urls from first 3 pages hence running the while loop from 1 to 3
		i = 1

		nxt_url = c().next_page_url.format(geo_id)
		
		while i<=3:

			print(i)			
			self.driver.get(nxt_url+str(step))
			self.get_restaurant_urls()

			# Incrementing the step by 30
			step += 30

			# Incrementing the page number
			i = i+1

	def close_driver(self):
		self.driver.close()

# This class uses the functions from Scraper class. We are writing this class to scrape all data.
class Scrape_All_Data:
	def __init__(self, geo_id):
		self.geo_id = geo_id
		pass

	def scrape_all_data(self):
		s = Scraper(self.geo_id)
		ds = DataStorage_SQL()
		dd = DataStorage_Dataframe()

		url = c().base_url.format(self.geo_id)
		print(url)
		s.start_base_url(url)
		try:
			s.parse_base_url(self.geo_id)
		except Exception as e:
			print(e)
			pass

		time.sleep(5)


		print("URL list length::",len(s.url_list))

		for url in s.url_list:
			try: 
				s.start_base_url(url)
				s.get_restaurant_details()
				
				ds.insert_data(**s.restaurant_details)
				print("Record inserted successfully...")
			
				dd.add_record(**s.restaurant_details)
				
				# s.close_driver()

			except Exception as e:
				print(e,"::::", url)
				pass

		dd.create_dataframe()
		dd.store_as_csv()

# scrape_All_Data = Scrape_All_Data(geo_id)

# Scrape restaurant data for requested geo_id
# scrape_All_Data.scrape_all_data("186338")