import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re
import io
import os

# ----------------------------
# Utility Functions
# ----------------------------
def split_number_street(address):
    if not isinstance(address, str):
        return "", ""
    parts = address.split(';')
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    match = re.match(r'^\s*(\d+[\w\-]*)\s+(.*)', address)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "", address.strip()

def map_alba_to_nw(df):
    df = df.fillna("")
    if 'Address' not in df.columns:
        raise ValueError("'Address' column is required in the input data.")

    df['TerritoryID'] = df.get('Territory_ID', "")
    df['TerritoryNumber'] = df.get('Territory_number', "")
    df['Category'] = df.get('Territory_description', "")
    df['CategoryCode'] = ""
    df['TerritoryAddressID'] = df.get('Address_ID', "")
    df['ApartmentNumber'] = df.get('Suite', "")
    df[['Number', 'Street']] = df['Address'].apply(split_number_street).apply(pd.Series)
    df['Suburb'] = df.get('City', "")
    df['PostalCode'] = df.get('Postal_code', "")
    df['State'] = df.get('Province', "")
    df['Name'] = df.get('Name', "")
    df['Phone'] = df.get('Telephone', "")
    df['Type'] = ""
    df['Status'] = df.get('Status', "")
    df['NotHomeAttempt'] = ""
    df['Date1'] = df['Date2'] = df['Date3'] = df['Date4'] = df['Date5'] = ""
    df['Language'] = df.get('Language', "")
    df['Latitude'] = df.get('Latitude', "")
    df['Longitude'] = df.get('Longitude', "")
    df['Notes'] = df.get('Notes', "")
    df['NotesFromPublisher'] = ""
    return df

# ----------------------------
# GUI Functions
# ----------------------------
def load_file():
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not path:
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, content)
        root.title(f"Loaded: {os.path.basename(path)}")
    except Exception as e:
        messagebox.showerror("Error reading file", str(e))

def convert_text_to_csv():
    text = text_widget.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("No Input", "Please load or paste your data.")
        return
    try:
        df = pd.read_csv(io.StringIO(text), sep=None, engine='python', dtype=str).fillna("")
        df = map_alba_to_nw(df)

        required_cols = [
            'TerritoryID','TerritoryNumber','CategoryCode','Category',
            'TerritoryAddressID','ApartmentNumber','Number','Street',
            'Suburb','PostalCode','State','Name','Phone','Type','Status',
            'NotHomeAttempt','Date1','Date2','Date3','Date4','Date5',
            'Language','Latitude','Longitude','Notes','NotesFromPublisher'
        ]
        export_df = df[required_cols]
        
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not save_path:
            return
        export_df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"Saved: {save_path}")
    except Exception as e:
        messagebox.showerror("Conversion Error", str(e))

def clear_textbox():
    text_widget.delete("1.0", tk.END)
    root.title("ALBA to NW Publisher Converter")

# ----------------------------
# GUI Setup
# ----------------------------
root = tk.Tk()
root.title("ALBA to NW Publisher Converter")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

btn_load = tk.Button(frame, text="Load CSV File into Textbox", command=load_file)
btn_load.pack(anchor="w", pady=(0,5))

text_widget = tk.Text(frame, wrap=tk.NONE, height=20, width=100)
text_widget.pack(fill="both", expand=True)

scroll_y = tk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
scroll_x = tk.Scrollbar(frame, orient="horizontal", command=text_widget.xview)
text_widget.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")

btn_convert = tk.Button(frame, text="Convert to NW Publisher Format and Save", command=convert_text_to_csv)
btn_convert.pack(pady=5)

btn_clear = tk.Button(frame, text="Clear Input", command=clear_textbox)
btn_clear.pack(pady=(0,5))

root.mainloop()
