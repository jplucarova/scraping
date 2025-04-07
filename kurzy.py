import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
#pd.set_option('display.max_columns', None)

def get_tab(url):
	# Initialize an empty DataFrame to store the results
	df_fin = pd.DataFrame()
	# Loop through the pages
	for i in range(53,57):
		url_i = url + str(i)
		print(url_i)
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

if __name__ == "__main__":
	k_df = get_tab("https://www.kurzy.cz/podilove-fondy/jtam/jt-opportunity-czk/statistiky/cela-historie/?page=")

	if k_df is not None:
		print("Successfully extracted the table!")
		#print(k_df.columns)  # Display the column names
		# Check the emty columns
		#print(k_df['Unnamed: 4_level_1 Unnamed: 4_level_2']) # Removed
		# Save the DataFrame to a CSV file with headers.
		file_name = "jt"
		k_df.to_csv(f"{file_name}.csv", index=False)
		print(f"Data saved to '{file_name}.csv'.")
		#print(k_df.iloc[[0,1,2,3],[0, 1, 2]])  # Display the first few rows and columns of the DataFrame
		#for i in range(3):
			#print(k_df.iloc[[i]])