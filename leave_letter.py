import streamlit as st
from fpdf import FPDF
from datetime import date
from cryptography.fernet import Fernet
import tempfile

# Function to decrypt the signature file in memory
def decrypt_signature(encryption_key):
    try:
        fernet = Fernet(encryption_key.encode())  # Convert string key to bytes
        with open("encrypted_signature.bin", "rb") as enc_file:
            encrypted_data = enc_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        st.error("Invalid password for the signature file.")
        return None

# Function to generate PDF
def generate_pdf(name, designation, school, from_date, to_date, reason, signature_data=None):
    pdf = FPDF()
    pdf.add_page()
    
    # Title and Address
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Leave Application", ln=True, align="C")
    pdf.ln(10)
    
    # Date
    today = date.today()
    pdf.cell(200, 10, f"Date: {today.strftime('%B %d, %Y')}", ln=True)
    
    # To
    pdf.cell(200, 10, "To,", ln=True)
    pdf.cell(200, 10, "The Headmaster,", ln=True)
    pdf.cell(200, 10, school, ln=True)
    pdf.ln(10)
    
    # Subject and Content
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Subject: Application for leave", ln=True)
    
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"Respected Sir,\nI am writing to request leave from {from_date} to {to_date} due to {reason}. Kindly grant me leave for the above mentioned period. Thank you for the consideration.")
    pdf.ln(10)
    
    # "Yours sincerely" and Optional Signature
    pdf.cell(200, 10, "Yours sincerely,", ln=True)
    pdf.ln(5)

    
    # Closing Details Aligned to the Right
    pdf.cell(200, 10, name)
    # Add Signature if Decrypted Data is Provided
    if signature_data:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(signature_data)
            tmp_file_path = tmp_file.name
        pdf.image(tmp_file_path, x=140, y=pdf.get_y(), w=40)  # Right-align signature
    pdf.cell(200, 10, designation, ln=True)
    pdf.cell(200, 10, school, ln=True)
    pdf.ln(10)    

    return pdf

# Streamlit UI
st.title("Leave Application Generator")

name = st.text_input("Name", "D Neerajamma")
designation = st.text_input("Designation", "SA Telugu")
school = st.text_input("School", "GHS, Gandhinagar, MBNR")
from_date = st.date_input("From Date")
to_date = st.date_input("To Date")
reason = st.text_area("Reason for Leave", "")

# Password input for decryption
encryption_key = st.text_input("Enter Password for Signature File", type="password")

if st.button("Generate PDF"):
    # Try to decrypt the signature with provided password
    signature_data = decrypt_signature(encryption_key) if encryption_key else None
    
    # Generate PDF with or without signature
    pdf = generate_pdf(name, designation, school, from_date.strftime("%B %d, %Y"), to_date.strftime("%B %d, %Y"), reason, signature_data)
    
    # Save PDF to a temporary file
    pdf_file = "leave_application.pdf"
    pdf.output(pdf_file)
    
    # Provide download link for PDF
    with open(pdf_file, "rb") as f:
        st.download_button("Download Leave Application PDF", f, file_name=pdf_file)
