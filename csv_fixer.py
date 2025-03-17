import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Function to open file picker
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_path

# Select file
input_file = select_file()
if not input_file:
    print("No file selected. Exiting...")
    exit()

# Define output file path (same directory, with 'cleaned_' prefix)
output_file = input_file.replace(".csv", "_cleaned.csv")

# Load the CSV file with correct delimiter
df = pd.read_csv(input_file, delimiter=";", dtype=str)

# Convert "Summa" to numeric, replacing commas with dots for correct parsing
df["Summa"] = df["Summa"].str.replace(",", ".").astype(float)

# Change "Asiakkaan nimi" to "VIPPS MOBILEPAY AS" where "Summa" is negative
df.loc[df["Summa"] < 0, "Asiakkaan nimi"] = "VIPPS MOBILEPAY AS"

# Convert date columns to standard YYYY-MM-DD format
date_columns = ["Päivä", "Myyntipäivä", "Tilityspäivä"]
for col in date_columns:
    df[col] = pd.to_datetime(df[col], format="%d-%m-%Y", errors="coerce").dt.strftime("%Y-%m-%d")

# Save the cleaned file with UTF-8 encoding
df.to_csv(output_file, sep=";", index=False, encoding="utf-8")

print(f"✅ Cleaned file saved as: {output_file}")
