# MP1 Data Pipeline

For this project, I built a Python program that takes in a CSV file, cleans the data, and saves the results to a new file. It uses a YAML file to decide which cleaning steps to run. Before cleaning, it checks that the required columns exist and removes rows with invalid numbers. It can also remove duplicates, handle missing values, and filter outliers using IQR or Z-score. I split the code into different files inside the src folder to keep everything organized. The pipeline also uses logging to show what's happening and help identify errors.

## How to Run

python pipeline.py --input fixtures/sample.csv --output output/clean.csv --config config/config.yaml --verbose

## Example Output

When I ran the pipeline with sample.csv, it started with 5 rows and ended with 5 rows because none needed to be removed.

The cleaned data was saved to output/clean.csv.
