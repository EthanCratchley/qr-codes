import pandas as pd
import qrcode
import os
from tkinter import Tk, Label, Button, filedialog, messagebox, StringVar, Entry

class QRCodeGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Bulk QR Code Generator")
        master.geometry("500x300")  # Set the size of the window

        self.label = Label(master, text="Bulk QR Code Generator")
        self.label.pack(pady=10)

        self.csv_button = Button(master, text="Select CSV File", command=self.select_csv)
        self.csv_button.pack(pady=5)

        self.export_label = Label(master, text="Export Directory:")
        self.export_label.pack(pady=5)

        self.export_directory = StringVar()
        self.export_entry = Entry(master, textvariable=self.export_directory, width=40)
        self.export_entry.pack(pady=5)

        self.export_button = Button(master, text="Select Export Directory", command=self.select_export_directory)
        self.export_button.pack(pady=5)

        self.generate_button = Button(master, text="Generate QR Codes", command=self.generate_qr_codes)
        self.generate_button.pack(pady=10)

    def select_csv(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.csv_file = file_path
            messagebox.showinfo("Selected File", f"Selected CSV file: {file_path}")

    def select_export_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.export_directory.set(directory)

    def generate_qr_codes(self):
        if not hasattr(self, 'csv_file'):
            messagebox.showerror("Error", "No CSV file selected")
            return

        if not self.export_directory.get():
            messagebox.showerror("Error", "No export directory selected")
            return
        
        try:
            data = pd.read_csv(self.csv_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file: {e}")
            return

        required_columns = {'Name', 'Phone', 'Email'}
        if not required_columns.issubset(data.columns):
            messagebox.showerror("Error", f"CSV file must contain the following columns: {', '.join(required_columns)}")
            return

        export_path = self.export_directory.get()
        for index, row in data.iterrows():
            name = row['Name']
            phone = row['Phone']
            email = row['Email']
            qr_data = f"""
BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL:{phone}
EMAIL:{email}
END:VCARD
"""
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            img_path = os.path.join(export_path, f"{name}_qr_code.png")
            img.save(img_path)

        messagebox.showinfo("Success", "QR Codes generated successfully")

if __name__ == "__main__":
    root = Tk()
    qr_code_generator = QRCodeGenerator(root)
    root.mainloop()
