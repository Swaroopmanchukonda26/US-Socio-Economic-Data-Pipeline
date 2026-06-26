# 📊 US Socio-Economic & Incident Analytics Pipeline

An end-to-end data analytics pipeline built in raw Python using Pandas, Seaborn, and Matplotlib to merge, clean, and visualize institutional US Census records alongside unstructured regional incident tracking streams.

## 📈 Core Analytical Insights
* **Data Merging & Cleaning:** Joins separate socio-economic vectors (Poverty indexes, High School Graduation rates, and Median Household Earnings) across matching geographical state keys while handling missing data states securely via `pd.to_numeric(errors='coerce')`.
* **Statistical Visualization:** Generates two-panel comparative regression subplots exploring the relationship between regional structural education markers, local poverty indices, and total incident concentrations.

## 🛠️ Software Stack
* **Language:** Python 3.x
* **Data Engineering Libraries:** Pandas, NumPy
* **Visualization Engine:** Seaborn, Matplotlib (Customized Dark Grid Interface Layout)
