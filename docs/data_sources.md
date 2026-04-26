# Data Sources

## Current Data Source

The project currently uses Taiwan agricultural market data collected for Taipei Second Market.

Primary raw file:

- `data/raw/taiwan_main_fruits_taipei2_2017_to_present.csv`

Standardized dataset:

- `data/processed/market_fruit_dataset_en.csv`

## Where The Data Comes From

Source endpoint:

- `https://data.moa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx`

Relevant fields used by the project:

- trade date
- crop name
- market code
- market name
- high / middle / low / average price
- transaction volume

## How The Data Is Collected

The project includes a dedicated download script:

- `scripts/download_taiwan_main_data_taipei2.py`

That script:

- queries the MOA open-data endpoint
- filters to Taipei Second Market
- keeps the main fruit categories used by the project
- writes the raw result to `data/raw/`

## How The Standardized Dataset Is Built

After downloading raw data, run:

```bash
conda run -n fruit python scripts/build_market_dataset.py
```

This script:

- maps crop names into a stable fruit-category schema
- converts ROC dates to Gregorian dates
- standardizes numeric columns and units
- writes `data/processed/market_fruit_dataset_en.csv`
- writes `outputs/reports/dataset_summary.md`

## Current Scope

The current dataset covers:

- market: Taipei Second Market
- categories: apple, banana, orange, grape, pear
- frequency after modeling prep: weekly

## Notes

- `data/raw/archive.zip` is a historical early-stage sample and is not part of the current primary workflow.
- The raw-source script and standardized-dataset script should be rerun together when refreshing data.
