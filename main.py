import qrcode
import vobject
import csv
import os

def create_vcard(name, phone, email):
    v = vobject.vCard()
    v.add('fn').value = name
    v.add('tel').value = phone
    v.add('email').value = email
    return v.serialize()

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)

def main(csv_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            phone = row['Phone']
            email = row['Email']
            vcard_data = create_vcard(name, phone, email)
            filename = os.path.join(output_dir, f"{name}.png")
            generate_qr_code(vcard_data, filename)

if __name__ == "__main__":
    csv_file = 'codes.csv'  # Replace with your CSV file path
    output_dir = 'qrcodes'
    main(csv_file, output_dir)
