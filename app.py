# Import essential libraries
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scraper import Scrape_All_Data
from data_storage import DataStorage_SQL

app = FastAPI()

# Base endpoint
@app.get("/")
def hello():
	return "Hello Quandoo!"


# scrape_data endpoint (required parameter: geo_id)
@app.get('/scrape_data/{geo_id}')
def get_avg_ride_duration(geo_id):
	# Create the object of Scrape_All_Data (takes geo_id as parameter)
	scrape_All_Data = Scrape_All_Data(geo_id)

	# Scrape restaurant data for requested geo_id
	scrape_All_Data.scrape_all_data()

	return "Method processing finished. Please check /retreive_data/{geo_id} api endpoint."


# retreive_data endpoint (required_parameter: geo_id)
@app.get('/retreive_data/{geo_id}')
def get_avg_ride_duration(geo_id):
	# Connect to SQL db using DataStorage_SQL class
	ds = DataStorage_SQL()

	# Fetch the records of requested geo_id
	records = ds.fetch_data_by_geo_id(geo_id)

	# HTML table format

	table_html = "<table border='1'><tr><th>url</th><th>restaurant_id </th><th>fetch_count </th><th>time_of_fetching_data </th><th>rating float </th><th>rest_name </th><th>address </th><th>telephone </th><th>website </th><th>tags </th><th>CUISINES </th><th>Special_Diets </th><th>Meals </th><th>is_michelin </th><th>menu_link_available </th><th>neighborhood </th><th>restaurant_rank </th><th>Food_Rating </th><th>Value_Rating </th><th>Service_Rating </th><th>Atmosphere_Rating </th><th>PRICE_RANGE </th><th>FEATURES </th><th>total_reviews </th><th>menu_link</th></tr>"

	for row in records:
		table_html += "<tr>"

		for cell in row:
			table_html += f"<td>{cell}</td>"
		table_html += "</tr>"

	table_html += "</table>"
	# Return HTML response
	return HTMLResponse(content=table_html)