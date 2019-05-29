# Scraper

## Environment
### macOS 10.14.4
* Python 3.7
* beautifulsoup4 4.7.1
* urllib3 1.24.1


1. Scraper implementation which extract the population in the United States table from https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population.
2. The table contains 12 columns and 314 rows. 
3. The last column is each city's zipcode from the individual city pages.
4. The type of some specific columns are int and float and rest of them are string.
5. The final table is clean and ready to be uploaded to a BigQuery table. 
