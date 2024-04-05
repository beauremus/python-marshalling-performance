#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("performance_data.csv")

# Iterate over unique function names and plot their performance data
for func_name in df["Function"].unique():
    func_df = df[df["Function"] == func_name]
    plt.errorbar(
        func_df["Iterations per Run"],
        func_df["Average Time (seconds)"],
        yerr=func_df["Standard Deviation (seconds)"],
        label=func_name,
        marker="o",
    )

# Set labels and title
plt.xlabel("Iterations per Run")
plt.ylabel("Average Time (seconds)")
plt.title("Performance of Functions")
plt.legend()
plt.grid(True)

# Set y-axis to logarithmic scale
plt.xscale("log")
plt.yscale("log")

# Show plot
plt.show()
