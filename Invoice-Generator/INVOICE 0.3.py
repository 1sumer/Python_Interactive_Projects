import tkinter as tk
import datetime
from fpdf import FPDF
from tkinter import messagebox
from tkinter import *
import csv
import os
import mysql.connector

class PDF(FPDF):
    def header(self):
        # Logo
        self.image(r"C:\\Users\\syed mubarak pasha\\OneDrive\\Documents\\Python\\Assignment\\PDF\\Certisured.jpeg", 5, 12, 30)
        # font
        self.set_font('Times', 'B', 26)
        # Padding
        self.cell(80)
        # Title
        self.cell(30, 10, 'CESTISURED', border=False, ln=1, align='C')
        
        self.set_font('Times', 'B', 15)
        self.cell(0, 10, 'Analogica Software Development Pvt Ltd.', border=False, ln=1, align='C')
        
        self.set_font('Times', '', 14)
        self.cell(0, 10, 'Bhashyam Circle, 3rd Block, Rajajinagar, Bangalore , 560010.', border=False, ln=1, align='C')
        self.ln(2)
        
        self.set_font('Times', '', 12)
        self.cell(0, 10, 'Ph: 9606698866  Email: hello@certisured.com', border=False, ln=1, align='C')
        # Line break
        self.ln(2)
        
    def footer(self):
        # set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('Times', 'I', 8)
        # add page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
        


def create_table(pdf, item_no, description, quantity, unit_price, total_price):
    pdf.cell(20, 10, 'Item No.', 1)
    pdf.cell(90, 10, 'Description', 1)
    pdf.cell(20, 10, 'Quantity', 1)
    pdf.cell(30, 10, 'Unit Price', 1)
    pdf.cell(30, 10, 'Total Price', 1)
    pdf.ln()

    # add entries to table
    for i in range(len(item_no)):
        pdf.cell(20, 10, item_no[i], 1)
        pdf.cell(90, 10, description[i], 1)
        pdf.cell(20, 10, quantity[i], 1)
        pdf.cell(30, 10, unit_price[i], 1)
        pdf.cell(30, 10, total_price[i], 1)
        pdf.ln()
 
def create_pdf():
    invoice_no = invoice_no_entry.get() 
    name = name_entry.get()
    address = address_entry.get()
    city = city_entry.get()
    phone = phone_entry.get()
    email = email_entry.get() 
    mode_of_payment= mode_of_payment_entry.get()
      
    n = int(n_entry.get())

    # initialize empty lists for the table entries
    item_no = []
    description = []
    quantity = []
    unit_price = []
    total_price = []

    # get the table entries from the user
    for i in range(n):
        item_no.append(str(i+1))
        description.append(str(desc_entry[i].get()))
        quantity.append(qyt_entry[i].get())
        unit_price.append(price_entry[i].get())
        total_price.append(str(float(quantity[i])*float(unit_price[i])))

    sub_total = sum(float(price) for price in total_price if price and price != '.')
    cgst = sub_total * 0.09  # assuming 9% CGST
    sgst = sub_total * 0.09 
    grand_total = sum(map(float, [sub_total, cgst, sgst]))
    
    # Connect to MySQL database
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sameer@786",
    database="certisured"
    )

    # Create table to store invoice data
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS invoices (id INT AUTO_INCREMENT PRIMARY KEY, invoice_no VARCHAR(255), name VARCHAR(255), address VARCHAR(255), city VARCHAR(255), phone VARCHAR(255), email VARCHAR(255), item_no VARCHAR(255), description VARCHAR(255), quantity VARCHAR(255), unit_price VARCHAR(255), total_price VARCHAR(255), mode_of_payment VARCHAR(255))")
    
    pdf = PDF()

    # add a page
    pdf.add_page()

    pdf.set_font('Times', 'B', 15)
    pdf.cell(0, 10, 'Invoice', align='C')
    pdf.ln()

    pdf.set_font('Times', '', 12)
    date = datetime.date.today()
    pdf.cell(0, 10, f'GSTIN: 29AASCA5089J1ZU                                                                                        Invoice No: {invoice_no}', align='L')
    pdf.ln(8)
    pdf.cell(0, 10, f'Date: {date}', align='R')
    pdf.ln(8)
    pdf.cell(0, 10, f'Customer Name: {name}')
    pdf.ln(8)
    pdf.cell(0, 10, f'Address: {address}')
    pdf.ln(8)
    pdf.cell(0, 10, f'City: {city}')
    pdf.ln(8)
    pdf.cell(0, 10, f'Phone: {phone}')
    pdf.ln(8)
    pdf.cell(0, 10, f'Email: {email}')
    pdf.ln(12)

    create_table(pdf, item_no, description, quantity, unit_price, total_price)
    
    # set style and size of font
    pdf.cell(160, 10, '', 0, 1)
    pdf.ln(-5)
    pdf.cell(30, 10, 'Sub Total:', 1, 0, 'C')
    pdf.cell(30, 10, '{:.2f}'.format(sub_total), 1, 1)
    pdf.cell(30, 10, 'CGST (9%):', 1, 0, 'C')
    pdf.cell(30, 10, '{:.2f}'.format(cgst), 1, 1)
    pdf.cell(30, 10, 'SGST (9%):', 1, 0, 'C')
    pdf.cell(30, 10, '{:.2f}'.format(sgst), 1, 1)
    pdf.cell(30, 10, 'Grand Total:', 1, 0, 'C')
    pdf.cell(30, 10, '{:.2f}'.format(grand_total), 1, 1)
    pdf.ln(4)
    if mode_of_payment == 'Cash':
        pdf.cell(0, 10, 'Pay To:-')
        pdf.ln(8)
        pdf.cell(0, 10, 'Analogica Software Development Pvt Ltd.')
        pdf.ln(10)
    else:
        pdf.cell(0, 10, f'Payment Method: {mode_of_payment}')
        pdf.ln(10)
        pdf.cell(0, 10, 'Pay To:-')
        pdf.ln(8)
        pdf.cell(0, 10, 'Analogica Software Development Pvt Ltd.')
        pdf.ln(8)
        pdf.cell(0, 10, 'Current A/c: 029605007484')
        pdf.ln(8)
        pdf.cell(0, 10, 'IFSC CODE: ICIC0000296')
        pdf.ln(10)

    pdf.cell(0, 10, '                                                                                                                                    Seal')
    pdf.ln(5)   
    pdf.cell(0, 10, "_______________________________________________________________________________________")
    pdf.ln(5)
        
    pdf.cell(0, 10, "* This is computer generated invoice signature not required ")
    pdf.ln(0)

    pdf_name = name.replace(" ", "_") + ".pdf"

    # Output the PDF with the modified file name
    pdf.output(pdf_name, 'F')
    
    # Insert invoice data into MySQL database
    mycursor = mydb.cursor()
    sql = "INSERT INTO invoices (invoice_no, name, address, city, phone, email, item_no, description, quantity, unit_price, total_price, mode_of_payment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for i in range(n):
        val = (invoice_no, name, address, city, phone, email, item_no[i], description[i], quantity[i], unit_price[i], total_price[i], mode_of_payment)
        mycursor.execute(sql, val)
    mydb.commit()
    

# Create a new Tkinter window
root = tk.Tk()
root.title("Invoice 0.2")

# maximize the main window
root.state('zoomed')

headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

lf_bg = 'MediumSpringGreen'

tk.Label(root, text="INVOICE", font=headlabelfont, bg='SpringGreen').pack(side=tk.TOP, fill=X)

Frame(root, bg=lf_bg)

# course_duration_frame label and text area
invoice_no_frame = Frame(root, bg=lf_bg)
invoice_no_frame.pack(side=TOP, padx=5, pady=5, fill=X)

invoice_no_label = tk.Label(invoice_no_frame, text="Invoice No:", width=20, font=labelfont, bg=lf_bg)
invoice_no_label.pack(side=LEFT)

invoice_no_entry = tk.Entry(invoice_no_frame, width=50, font=entryfont)
invoice_no_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

# name_frame label and text area
name_frame = tk.Frame(root, bg=lf_bg)
name_frame.pack(side=TOP, padx=5, pady=5, fill=X)

name_label = tk.Label(name_frame, text="Name:",width=19, font=labelfont, bg=lf_bg)
name_label.pack(side=LEFT, padx=5, pady=5)

name_entry = tk.Entry(name_frame, width=50, font=entryfont)
name_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

# address_frame label and text area
address_frame = tk.Frame(root, bg=lf_bg)
address_frame.pack(side=TOP, padx=5, pady=5, fill=X)

address_label = tk.Label(address_frame, text="Address:",width=19, font=labelfont, bg=lf_bg)
address_label.pack(side=LEFT, padx=5, pady=5)

address_entry = tk.Entry(address_frame, width=50, font=entryfont)
address_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

#Gst_frame label and text area
city_frame = Frame(root, bg=lf_bg)
city_frame.pack(side=TOP, padx=5, pady=5, fill=X)

city_label = tk.Label(city_frame, text="City:", width=20, font=labelfont, bg=lf_bg)
city_label.pack(side=LEFT)

city_entry = tk.Entry(city_frame, width=50, font=entryfont)
city_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

#Gst_frame label and text area
phone_frame = Frame(root, bg=lf_bg)
phone_frame.pack(side=TOP, padx=5, pady=5, fill=X)

phone_label = tk.Label(phone_frame, text="Phone No:", width=20, font=labelfont, bg=lf_bg)
phone_label.pack(side=LEFT)

phone_entry = tk.Entry(phone_frame, width=50, font=entryfont)
phone_entry.pack(side=LEFT, padx=5, pady=5, fill=X)


email_frame = Frame(root, bg=lf_bg)
email_frame.pack(side=TOP, padx=5, pady=5, fill=X)

email_label = tk.Label(email_frame, text="Email ID:", width=20, font=labelfont, bg=lf_bg)
email_label.pack(side=LEFT)

email_entry = tk.Entry(email_frame, width=50, font=entryfont)
email_entry.pack(side=LEFT, padx=5, pady=5, fill=X)


# Create input fields for course information
n_frame = tk.Frame(root, bg=lf_bg)
n_frame.pack(side=TOP, padx=5, pady=5, fill=X)

n_label = tk.Label(n_frame, text="N:",width=19, font=labelfont, bg=lf_bg)
n_label.pack(side=LEFT, padx=5, pady=5)

n_entry = tk.Entry(n_frame, width=50, font=entryfont)
n_entry.pack(side=LEFT, padx=5, pady=5, fill=X)


desc_frame = tk.Frame(root, bg=lf_bg)
desc_frame.pack(side=TOP, padx=5, pady=5, fill=X)

desc_label = tk.Label(desc_frame, text="Description:",width=19, font=labelfont, bg=lf_bg)
desc_label.pack(side=LEFT, padx=5, pady=5)

desc_entry = []
for i in range(2):  # create 5 description entry fields
    desc = tk.Entry(desc_frame, width=50, font=entryfont)
    desc.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X)
    desc_entry.append(desc)

# qyt_frame label and text area
qyt_frame = Frame(root, bg=lf_bg)
qyt_frame.pack(side=TOP, padx=5, pady=5, fill=X)

qyt_label = tk.Label(qyt_frame, text="Quantity:", width=20, font=labelfont, bg=lf_bg)
qyt_label.pack(side=LEFT)

qyt_entry = []
for i in range(2):  # create 5 quantity entry fields
    qyt = tk.Entry(qyt_frame, width=50, font=entryfont)
    qyt.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X)
    qyt_entry.append(qyt)

# price_frame label and text area
price_frame = Frame(root, bg=lf_bg)
price_frame.pack(side=TOP, padx=5, pady=5, fill=X)

price_label = tk.Label(price_frame, text="Price:",width=20, font=labelfont, bg=lf_bg)
price_label.pack(side=LEFT)

price_entry = []
for i in range(2):  # create 5 price entry fields
    price = tk.Entry(price_frame, width=50, font=entryfont)
    price.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X)
    price_entry.append(price)


mode_of_payment_frame = Frame(root, bg=lf_bg)
mode_of_payment_frame.pack(side=TOP, padx=5, pady=5, fill=X)

mode_of_payment_label = tk.Label(mode_of_payment_frame, text="Payment Method:", width=20, font=labelfont, bg=lf_bg)
mode_of_payment_label.pack(side=LEFT)

mode_of_payment_entry = tk.Entry(mode_of_payment_frame, width=50, font=entryfont)
mode_of_payment_entry.pack(side=LEFT, padx=5, pady=5, fill=X)


button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

create_pdf_button = tk.Button(button_frame, text="Create Invoice", command=create_pdf, width=15, font=labelfont)
create_pdf_button.grid(row=0, column=0, padx=5, pady=5, sticky=E)

# Clear button
def clear_fields():
    # Clear the sender email, email subject, and email body fields
    invoice_no_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    n_entry.delete(0, tk.END)
    
    for desc in desc_entry:
        desc.delete(0, tk.END)
        
    for qyt in qyt_entry:
        qyt.delete(0, tk.END)
        
    for price in price_entry:
        price.delete(0, tk.END)
        
    mode_of_payment_entry.delete(0, tk.END)
    

clear_button = tk.Button(button_frame, text="Clear", command=clear_fields, width=15, font=labelfont)
clear_button.grid(padx=5, pady=5, sticky=E)

root.mainloop()