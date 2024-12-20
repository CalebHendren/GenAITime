import csv
import matplotlib.pyplot as plt
from collections import Counter

input_file = "openalex_biology_generative_ai_filtered.csv"

years = []

with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        year = row.get("Year", "")
        if year.isdigit():
            years.append(int(year))

# Count how many papers per year
year_counts = Counter(years)

# Sort by year
sorted_years = sorted(year_counts.keys())
counts = [year_counts[y] for y in sorted_years]

# Plot the counts by year
plt.figure(figsize=(10, 6))
bars = plt.bar(sorted_years, counts, color="steelblue", edgecolor="black")

# Add the exact number of publications above each bar
for bar, count in zip(bars, counts):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, str(count),
             ha='center', va='bottom', fontsize=10)

# Customize the plot
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.title("Number of Publications by Year")
plt.xticks(sorted_years, rotation=45)

# Add a footer to indicate the data source
plt.text(0.5, -0.15, "Data Source: OpenAlex", fontsize=10, color="gray",
         ha='center', va='top', transform=plt.gca().transAxes)

# Adjust layout to prevent overlapping elements
plt.tight_layout()

# Save the plot as a PNG file
output_image = "publications_by_year.png"
plt.savefig(output_image, dpi=300, bbox_inches="tight")

# Show the plot
plt.show()

print(f"Plot saved as {output_image}")
