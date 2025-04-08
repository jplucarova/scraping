import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time
import argparse
#pd.set_option('display.max_columns', None)

def get_tab(url):
	# Initialize an empty DataFrame to store the results
	df_fin = pd.DataFrame()
	# Loop through the pages
	i = 1
	# Loop through the pages until the DataFrame is empty
	while True:
		url_i = url + str(i)
		print(url_i)
		i += 1
		try:
			# send a GET request to the URL
			response = requests.get(url_i)
			response.raise_for_status()  # check if the request was successful
		except requests.exceptions.RequestException as err:
			print(f"Error fetching the webpage: {err}")
			return None
		try:
			# Parse the HTML content with BeautifulSoup
			soup = BeautifulSoup(response.content, "html.parser")

			# Find the specific table by its class name
			tables = soup.find_all("table", {"class": "pd"})
			if not tables:
				print("No tables found with the specified class name.")
				return None

			table = tables[0]  # Assuming you want the first table

			# Convert the table to a pandas DataFrame
			df = pd.read_html(StringIO(str(table)))[0]
			#print(df.columns)
			# Drop the major header row
			df.columns = df.columns.droplevel(0)
			#print(df.columns)
			#for i in df.columns:
				#print(i)
		except Exception as err:
			print(f"Error parsing the webpage: {err}")
			return None
		try:
			# Clean the DataFrame
			# Flatten the MultiIndex columns if they exist
			# Check if the DataFrame has a MultiIndex for columns
			if isinstance(df.columns, pd.MultiIndex):
				# Flatten the MultiIndex columns and filter out None values
				new_columns = [' '.join(filter(None, map(str, col))) for col in df.columns]
				#print(new_columns)
				# Remove duplicate column names
				final_columns = []
				for col in new_columns:
					# Split the column name into words (a list of strings), whitespace is the default delimiter
					words = col.split()
					# create a set from the list "words" to remove duplicates, sort by indexes of the words list, join the words with whitespace as separator
					#unique_words = " ".join(sorted(set(words), key=words.index))
					# Remove duplicates by creating a dictionary using the list words as keys, list it, join the words with whitespace as separator
					unique_words = " ".join(list(dict.fromkeys(words)))
					final_columns.append(unique_words)
				# Assign the new column names to the DataFrame
				df.columns = final_columns
			# Reset the index to clean up the DataFrame
			df = df.reset_index(drop=True)
			# Remove any rows with 'další' or 'předchozí' in the first column
			df = df[~df.map(lambda x: isinstance(x, str) and ("další" in x or "předchozí" in x)).any(axis=1)]
			# Drop the row number 20
			#df = df.drop(index=20)
			# Remove any empty columns
			df = df.dropna(axis=1, how='all')
			#for i in df.columns:
			#	print(i)
			#return df
			#print(df.iloc[[0],[0, 1, 2]])  # Display the first few rows and columns of the DataFrame
		except Exception as err:
			print(f"Error cleaning the DataFrame: {err}")
			return None
		# Check if the DataFrame is empty
		if df.empty:
			break
		# Append the DataFrame to the final DataFrame
		try:
			df_fin = pd.concat([df_fin, df], ignore_index=True)
		except Exception as err:
			print(f"Error appending DataFrame: {err}")
			return None
	# Reset the index of the final DataFrame
	df_fin = df_fin.reset_index(drop=True)
	return df_fin
	time.sleep(1)  # Sleep for 1 second to avoid overwhelming the server

#if __name__ == "__main__":
#	k_df = get_tab("https://www.kurzy.cz/podilove-fondy/jtam/jt-opportunity-czk/statistiky/cela-historie/?page=")

#	if k_df is not None:
#		# Save the DataFrame to a CSV file with headers.
#		file_name = "jt"
#		k_df.to_csv(f"{file_name}.csv", index=False)
#		print(f"Data saved to '{file_name}.csv'.")
#argparse.ArgumentParser(description="Extract and save data from a webpage.") url from argument, set output file as argument
def save_output(df, output_path):
	if output_path.endswith('.csv'):
		df.to_csv(output_path, index=False)
	elif output_path.endswith('.json'):
		df.to_json(output_path, orient='records', lines=True)
	elif output_path.endswith('.xls') or output_path.endswith('.xlsx'):
		df.to_excel(output_path, index=False)
	else:
		raise ValueError("Unsupported file format. Use .csv, .json, .xls(x)")

def main():
	parser = argparse.ArgumentParser(description="Web scraper using requests")
	parser.add_argument("url", help="URL to scrape from")
	parser.add_argument("-o", "--output", help="Optional: Output file name with extension (.csv, .json, .xls, .xlsx)")

	args = parser.parse_args()

	df = get_tab(args.url)
	if df.empty:
			print("No data scraped.")
	elif args.output:
		save_output(df, args.output)
		print(f"Scraped data saved to {args.output}")
	else:
		print("No output file specified. Here's the DataFrame:\n")
		print(df)

if __name__ == "__main__":
	main()