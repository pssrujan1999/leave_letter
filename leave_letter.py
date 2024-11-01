
import streamlit as st
from fpdf import FPDF
from datetime import date

# Function to generate PDF
def generate_pdf(name, designation, school, from_date, to_date, reason):
    pdf = FPDF()
    pdf.add_page()
    
    # Title and Address
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Leave Application", ln=True, align="C")
    pdf.ln(10)
    
    # Date
    today = date.today()
    pdf.cell(200, 10, f"Date: {today.strftime('%B %d, %Y')}", ln=True)
    pdf.ln(10)
    
    # To
    pdf.cell(200, 10, "To,", ln=True)
    pdf.cell(200, 10, "The Headmaster, ", ln=True)
    pdf.cell(200, 10, school, ln=True)
    pdf.ln(10)
    
    # Subject and Content
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Subject: Leave Application", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"Respected Sir,\nI am writing to request leave from {from_date} to {to_date} due to {reason}. I kindly request you to grant me leave for these days, and I assure you to resume my duties promptly after my absence.\n\nThank you for considering my request.")

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Yours faithfully, ", ln=True)
    pdf.cell(200, 10, f"{name}", ln=True)
    pdf.cell(200, 10, f"{designation}", ln=True)
    pdf.cell(200, 10, f"{school}", ln=True)
    pdf.ln(10)    
    return pdf

# Streamlit UI
st.title("Leave Application Generator")

name = st.text_input("Name", "ABC")
designation = st.text_input("Designation", "XYZ")
school = st.text_input("School", "ABC School")
from_date = st.date_input("From Date")
to_date = st.date_input("To Date")
reason = st.text_area("Reason for Leave", "Specify your reason here")

if st.button("Generate PDF"):
    pdf = generate_pdf(name, designation, school, from_date.strftime("%B %d, %Y"), to_date.strftime("%B %d, %Y"), reason)
    
    # Save PDF to a temporary file
    pdf_file = "leave_application.pdf"
    pdf.output(pdf_file)
    
    # Provide download link for PDF
    with open(pdf_file, "rb") as f:
        st.download_button("Download Leave Application PDF", f, file_name=pdf_file)
