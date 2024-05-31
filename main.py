import qrcode
import vobject
import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_vcard(name, phone, email):
    v = vobject.vCard()
    v.add('fn').value = name
    v.add('tel').value = phone
    v.add('email').value = email
    return v.serialize()

def generate_qr_code(data, filename, fill_color="black", back_color="white"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(filename)

def main(csv_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                name = row['Name']
                phone = row['Phone']
                email = row['Email']
                print(f"Processing: {name}, {phone}, {email}")  # Debugging print
                vcard_data = create_vcard(name, phone, email)
                filename = os.path.join(output_dir, f"{name.replace(' ', '_')}.png")
                generate_qr_code(vcard_data, filename, fill_color="blue", back_color="white")
                print(f"Generated QR code for {name} at {filename}")  # Debugging print
            except Exception as e:
                print(f"Error processing row {row}: {e}")

def run_gui():
    root = tk.Tk()
    root.title("QR Code Generator")

    def select_csv_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            csv_entry.delete(0, tk.END)
            csv_entry.insert(0, file_path)

    def select_output_dir():
        directory = filedialog.askdirectory()
        if directory:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, directory)

    def generate_qr_codes():
        csv_file = csv_entry.get()
        output_dir = output_entry.get()
        if not csv_file or not output_dir:
            messagebox.showerror("Error", "Please select both CSV file and output directory.")
            return
        try:
            main(csv_file, output_dir)
            messagebox.showinfo("Success", "QR codes generated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    tk.Label(root, text="CSV File:").grid(row=0, column=0, padx=10, pady=5)
    csv_entry = tk.Entry(root, width=50)
    csv_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=select_csv_file).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=5)
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=select_output_dir).grid(row=1, column=2, padx=10, pady=5)

    tk.Button(root, text="Generate QR Codes", command=generate_qr_codes).grid(row=2, column=1, pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
