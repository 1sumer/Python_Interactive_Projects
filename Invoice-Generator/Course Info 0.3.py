import tkinter as tk
import datetime
from fpdf import FPDF
import tkinter as tk
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

    # Page footer
    def footer(self):
        # Set position of the footer
        self.set_y(-12)
        # set font
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

# Function to create PDF
def create_pdf():
    # Course information
    name = name_entry.get()
    Address = address_entry.get()
    course_name = course_name_entry.get()
    start_date = datetime.date.today().strftime('%d %B %Y')
    course_duration = course_duration_entry.get()
    course_fee = int(course_fee_entry.get())
    discount = int(discount_entry.get())
    final_fees = course_fee * (100 - discount) / 100
    Gst = int(Gst_entry.get())
    total_fee_to_be_paid = final_fees * (100 + Gst) / 100
    num_emi = int(num_emi_entry.get())
    installment_amount = total_fee_to_be_paid / num_emi
    
    # Calculate monthly installment
    monthly_installment = total_fee_to_be_paid / num_emi

    # Calculate date of each EMI payment
    installment_dates = [start_date]
    for i in range(1, num_emi):
        installment_date = datetime.date.today() + datetime.timedelta(days=30*i)
        installment_dates.append(installment_date.strftime('%d %B %Y'))

    # Connect to MySQL database
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sameer@786",
    database="certisured"
    )
    
        
    # Create a new PDF file using FPDF
    pdf_name = name.replace(" ", "_") + ".pdf"
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Course Details', align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Name: {name}')
    pdf.ln()
    pdf.cell(0, 10, f'Address: {Address}')
    pdf.ln()
    pdf.cell(0, 10, f'Course Name: {course_name}')
    pdf.ln()
    pdf.cell(0, 10, f'Start Date: {start_date}')
    pdf.ln()
    pdf.cell(0, 10, f'Duration: {course_duration}')
    pdf.ln()
    pdf.cell(0, 10, f'Fee: {course_fee}')
    pdf.ln()
    pdf.cell(0, 10, f'Discount: {discount}%')
    pdf.ln()
    pdf.cell(0, 10, f'Final Fees: {final_fees}')
    pdf.ln()
    pdf.cell(0, 10, f'GST: {Gst}%')
    pdf.ln()
    pdf.cell(0, 10, f'Total Fee to be Paid: {total_fee_to_be_paid}')
    pdf.ln()
    pdf.cell(0, 10, f'Number of EMI: {num_emi}')
    pdf.ln()
    pdf.cell(0, 10, f'Monthly Installment Amount: {installment_amount}')
    
    # Print installment details
    pdf.ln()
    pdf.cell(0, 10, 'Installment Details:                                                Signature')
    pdf.ln()
    for i, installment_date in enumerate(installment_dates):
        pdf.cell(0, 10, f'{i+1}. {installment_date}: {installment_amount}')
        pdf.ln(10)
    pdf.ln(20)   
    pdf.cell(0, 10, '          Seal')
    pdf.ln(5)
    
    pdf.cell(0, 10, "_______________________________________________________________________________")
    pdf.ln(5)
    
    pdf.cell(0, 10, "* This is computer generated invoice signature not required")
    pdf.ln(0)
    pdf.output(pdf_name)

    # Check if COURSE table already exists
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES LIKE 'COURSE'")
    table_exists = mycursor.fetchone()
    if table_exists:
        # COURSE table already exists, insert data
        sql = f"INSERT INTO COURSE (NAME, ADDRESS, COURSE_NAME, START_DATE, COURSE_DURATION, COURSE_FEE, DISCOUNT, GST, NUM_EMI) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, Address, course_name, start_date, course_duration, course_fee, discount, Gst, num_emi)
        mycursor.execute(sql, val)
    else:
        # COURSE table does not exist, create table and insert data
        mycursor.execute("CREATE TABLE COURSE (NAME VARCHAR(255), ADDRESS VARCHAR(255), COURSE_NAME VARCHAR(255), START_DATE VARCHAR(255), COURSE_DURATION VARCHAR(255), COURSE_FEE INT, DISCOUNT INT, GST INT, NUM_EMI INT)")
        sql = f"INSERT INTO COURSE (NAME, ADDRESS, COURSE_NAME, START_DATE, COURSE_DURATION, COURSE_FEE, DISCOUNT, GST, NUM_EMI) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, Address, course_name, start_date, course_duration, course_fee, discount, Gst, num_emi)
        mycursor.execute(sql, val)

    # Commit changes to database
    mydb.commit()
    
# Create a new Tkinter window
root = tk.Tk()
root.title("Course Info 0.2")

# maximize the main window
root.state('zoomed')


headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

lf_bg = 'MediumSpringGreen'

tk.Label(root, text="COURSE INFORMATION", font=headlabelfont, bg='SpringGreen').pack(side=tk.TOP, fill=X)

Frame(root, bg=lf_bg)

# Create input fields for course information
name_frame = tk.Frame(root, bg=lf_bg)
name_frame.pack(side=TOP, padx=5, pady=5, fill=X)

name_label = tk.Label(name_frame, text="Name:",width=19, font=labelfont, bg=lf_bg)
name_label.pack(side=LEFT, padx=5, pady=5)

name_entry = tk.Entry(name_frame, width=50, font=entryfont)
name_entry.pack(side=LEFT, padx=5, pady=5, fill=X)


address_frame = tk.Frame(root, bg=lf_bg)
address_frame.pack(side=TOP, padx=5, pady=5, fill=X)

address_label = tk.Label(address_frame, text="Address:",width=19, font=labelfont, bg=lf_bg)
address_label.pack(side=LEFT, padx=5, pady=5)

address_entry = tk.Entry(address_frame, width=50, font=entryfont)
address_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

# course_name_frame label and text area
course_name_frame = Frame(root, bg=lf_bg)
course_name_frame.pack(side=TOP, padx=5, pady=5, fill=X)

course_name_label = tk.Label(course_name_frame, text="Course Name:", width=20, font=labelfont, bg=lf_bg)
course_name_label.pack(side=LEFT)

course_name_entry = tk.Entry(course_name_frame, width=50, font=entryfont)
course_name_entry.pack(side=LEFT, padx=5, pady=5, fill=X)


# course_duration_frame label and text area
course_duration_frame = Frame(root, bg=lf_bg)
course_duration_frame.pack(side=TOP, padx=5, pady=5, fill=X)

course_duration_label = tk.Label(course_duration_frame, text="Course Duration:", width=20, font=labelfont, bg=lf_bg)
course_duration_label.pack(side=LEFT)

course_duration_entry = tk.Entry(course_duration_frame, width=50, font=entryfont)
course_duration_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

# course_fee_frame label and text area
course_fee_frame = Frame(root, bg=lf_bg)
course_fee_frame.pack(side=TOP, padx=5, pady=5, fill=X)

course_fee_label = tk.Label(course_fee_frame, text="Course Fee:", width=20, font=labelfont, bg=lf_bg)
course_fee_label.pack(side=LEFT)

course_fee_entry = tk.Entry(course_fee_frame, width=50, font=entryfont)
course_fee_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

#discount_frame label and text area
discount_frame = Frame(root, bg=lf_bg)
discount_frame.pack(side=TOP, padx=5, pady=5, fill=X)

discount_label = tk.Label(discount_frame, text="Discount:", width=20, font=labelfont, bg=lf_bg)
discount_label.pack(side=LEFT)

discount_entry = tk.Entry(discount_frame,width=50, font=entryfont)
discount_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

#Gst_frame label and text area
Gst_frame = Frame(root, bg=lf_bg)
Gst_frame.pack(side=TOP, padx=5, pady=5, fill=X)

Gst_label = tk.Label(Gst_frame, text="GST:", width=20, font=labelfont, bg=lf_bg)
Gst_label.pack(side=LEFT)

Gst_entry = tk.Entry(Gst_frame, width=50, font=entryfont)
Gst_entry.pack(side=LEFT, padx=5, pady=5, fill=X)

#Gst_frame label and text area
num_emi_frame = Frame(root, bg=lf_bg)
num_emi_frame.pack(side=TOP, padx=5, pady=5, fill=X)

num_emi_label = tk.Label(num_emi_frame, text="Number of EMI:", width=20, font=labelfont, bg=lf_bg)
num_emi_label.pack(side=LEFT)

num_emi_entry = tk.Entry(num_emi_frame, width=50, font=entryfont)
num_emi_entry.pack(side=LEFT, padx=5, pady=5, fill=X)


button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

create_pdf_button = tk.Button(button_frame, text="Create PDF", command=create_pdf, width=15, font=labelfont)
create_pdf_button.grid(row=0, column=0, padx=5, pady=5, sticky=E)


# Clear button
def clear_fields():
    # Clear the sender email, email subject, and email body fields
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    course_name_entry.delete(0, tk.END)
    course_duration_entry.delete(0, tk.END)
    course_fee_entry.delete(0, tk.END)
    discount_entry.delete(0, tk.END)
    Gst_entry.delete(0, tk.END)
    num_emi_entry.delete(0, tk.END)

clear_button = tk.Button(button_frame, text="Clear", command=clear_fields, width=15, font=labelfont)
clear_button.grid(padx=5, pady=5, sticky=E)

root.mainloop()