import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Function to open file picker
def select_file():
    root = tk.Tk()
    root.withdraw()
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

# Define output file path
output_file = input_file.replace(".csv", "_cleaned.csv")

# Load CSV
df = pd.read_csv(input_file, delimiter=";", dtype=str)

# Clean column headers
df.columns = df.columns.str.strip()

# Convert "Amount" to numeric
if "Amount" in df.columns:
    df["Amount"] = df["Amount"].str.replace(",", ".").astype(float)

    # Change "Merchant Name" where Amount is negative
    df.loc[df["Amount"] < 0, "Merchant Name"] = "VIPPS MOBILEPAY AS"
else:
    print("⚠️ No 'Amount' column found, skipping amount processing.")

# Convert date columns if present
for col in ["Date", "Transfer Date", "Transfer Reference Date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], format="%d.%m.%Y", errors="coerce").dt.strftime("%Y-%m-%d")

# Save cleaned file
df.to_csv(output_file, sep=";", index=False, encoding="utf-8")

print(f"✅ Cleaned file saved as: {output_file}")
