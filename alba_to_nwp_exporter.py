import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import re

def split_number_street(address):
    """
    Extract house number and street name from ALBA address.
    Handles formats like '1646;W 12th St' and '123 Main St'.
    """
    if not isinstance(address, str):
        return "", ""
    # Split on ';' if present
    parts = address.split(';')
    if len(parts) == 2:
        number = parts[0].strip()
        street = parts[1].strip()
        return number, street
    # Fallback to regex
    match = re.match(r'^\s*(\d+[\w\-]*)\s+(.*)', address)
    if match:
        number = match.group(1).strip()
        street = match.group(2).strip()
        return number, street
    return "", address.strip()

def convert_for_nw_publisher():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        df = pd.read_csv(file_path, dtype=str).fillna("")

        # Map ALBA columns to NW Publisher columns
        df['TerritoryID'] = df.get('Territory_ID', "")
        df['TerritoryNumber'] = df.get('Territory_number', "")
        df['Category'] = df.get('Territory_description', "")
        df['CategoryCode'] = ""  # Set if you have a mapping
        df['TerritoryAddressID'] = df.get('Address_ID', "")
        df['ApartmentNumber'] = df.get('Suite', "")
        # Address split
        df[['Number', 'Street']] = df['Address'].apply(split_number_street).apply(pd.Series)
        df['Suburb'] = df.get('City', "")
        df['PostalCode'] = df.get('Postal_code', "")
        df['State'] = df.get('Province', "")
        df['Name'] = df.get('Name', "")
        df['Phone'] = df.get('Telephone', "")
        df['Type'] = ""
        df['Status'] = df.get('Status', "")
        df['NotHomeAttempt'] = ""
        df['Date1'] = ""
        df['Date2'] = ""
        df['Date3'] = ""
        df['Date4'] = ""
        df['Date5'] = ""
        df['Language'] = df.get('Language', "")
        df['Latitude'] = df.get('Latitude', "")
        df['Longitude'] = df.get('Longitude', "")
        df['Notes'] = df.get('Notes', "")
        df['NotesFromPublisher'] = ""

        required_cols = [
            'TerritoryID', 'TerritoryNumber', 'CategoryCode', 'Category', 'TerritoryAddressID',
            'ApartmentNumber', 'Number', 'Street', 'Suburb', 'PostalCode', 'State',
            'Name', 'Phone', 'Type', 'Status', 'NotHomeAttempt',
            'Date1', 'Date2', 'Date3', 'Date4', 'Date5', 'Language',
            'Latitude', 'Longitude', 'Notes', 'NotesFromPublisher'
        ]
        export_df = df[required_cols]
        save_path = os.path.splitext(file_path)[0] + "_nw_import.csv"
        export_df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"File converted successfully:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("ALBA to NW Publisher Import CSV")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

convert_button = tk.Button(frame, text="Convert ALBA CSV for NW Publisher", command=convert_for_nw_publisher, width=40)
convert_button.pack(pady=10)

root.mainloop()
