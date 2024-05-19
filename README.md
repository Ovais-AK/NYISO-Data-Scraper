# NYISO Data Scraper

Version: 0.1

Prototype to retrieve historical data from the New York Independent System Operator (NYISO). Data sourced from the public portal of the NYISO's Market Information System (MIS), available at http://mis.nyiso.com/public/

Current version retrieves (a) hourly day-ahead market (DAM) locational based marginal prices (LMBPs) by (i) zone and (ii) generator, and (b) real-time market (RT) LBMPs at 5-minute increments by zone, between 1999 and 2024. Running the notebook creates a 'data' folder to save three separate csv files (ai, aii, and b) on the local machine. 

To run the scraper:
1. Clone the repository to your local machine.
2. Use requirements.txt and pip to create the virtual environment (venv).
3. Run the NYISO prices notebook using venv as the kernel.

Note: Running the entire notebook may take up to an hour.



