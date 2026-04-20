# Banking Customer Segmentation Analysis

## Project Overview
This project analyzes synthetic banking data to identify customer segments using K-Means, Hierarchical, and DBSCAN clustering.

## Key Insights
- **Data Cleaning:** Handled outliers in loan/transaction amounts using 99th percentile capping.
- **Feature Engineering:** Created Ratios (Debt-to-Income, Spend-to-Income) to better capture customer personas.
- **Dimensionality Reduction:** Used PCA to visualize high-dimensional financial data in 2D.

## How to Run
1. Clone this repo.
2. Create a virtual environment: `python -m venv venv`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the Jupyter Notebook: `01_banking_analysis.ipynb`.