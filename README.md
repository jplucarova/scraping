Scraping script to get data from "Výkonnost a historie výkonnosti, statistiky" table for various funds at kurzy.cz. 

# Usage
<pre> 
# Install and source your venv

# Get the data
python kurzy.py https://www.kurzy.cz/podilove-fondy/path_to_a_specific_fund/statistiky/cela-historie/ # Output pandas DataFrame

-o OUTPUT, --output OUTPUT
                        Optional: Output file name with extension (.csv, .json, .xls, .xlsx)

# Example
python kurzy.py https://www.kurzy.cz/podilove-fondy/jtam/jt-opportunity-czk/statistiky/cela-historie/ --output jt.csv</pre>
