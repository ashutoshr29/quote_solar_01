import streamlit as st
import fitz
from babel.numbers import format_currency
import io

def format_inr(amount):
    return format_currency(amount, 'INR', locale='en_IN').replace("₹", "Rs ").strip()

def edit_pdf(input_pdf, quote_no, prepared_by, client_name, location, capacity, date, kwrate, gstrate, subsidy):
    doc = fitz.open(input_pdf)
    total_pages = len(doc)

    # Page 0
    page_0 = doc[0]
    page_0.insert_text((440, 217), str(capacity)+" KW", fontsize=22, color=(0, 0, 0))
    page_0.insert_text((100, 325), str(client_name), fontsize=22, color=(0, 0, 0))

    for i in range(1,total_pages):
        doc[i].insert_text((235, 52), str(client_name), fontsize=12, color=(0, 0, 0))
        doc[i].insert_text((215, 76), str(location), fontsize=12, color=(0, 0, 0))
        doc[i].insert_text((250, 100), str(capacity)+" KW", fontsize=12, color=(0, 0, 0))
        doc[i].insert_text((460, 52), str(prepared_by), fontsize=12, color=(0, 0, 0))
        doc[i].insert_text((475, 76), str(quote_no), fontsize=12, color=(0, 0, 0))
        doc[i].insert_text((420, 100), str(date), fontsize=12, color=(0, 0, 0))
    
    # Page 03
    basic_syst_cost = float(capacity) * float(kwrate) * 1000
    total_gst = float(basic_syst_cost) * (float(gstrate)/100)
    total_amount = float(basic_syst_cost) + float(total_gst)
    total_investment = float(total_amount) - float(subsidy)

    page_3 = doc[2]
    page_3.insert_text((280, 350), str(capacity), fontsize=20, color=(0, 0, 0))
    page_3.insert_text((380, 350), str(kwrate), fontsize=20, color=(0, 0, 0))
    page_3.insert_text((450, 350), format_inr(basic_syst_cost), fontsize=15, color=(0, 0, 0))
    page_3.insert_text((450, 400), format_inr(basic_syst_cost), fontsize=12, color=(0, 0, 0))
    page_3.insert_text((410, 417), str(gstrate)+"%", fontsize=11, color=(0, 0, 0))
    page_3.insert_text((450, 420), format_inr(total_gst), fontsize=12, color=(0, 0, 0))
    page_3.insert_text((450, 440), format_inr(total_amount), fontsize=12, color=(0, 0, 0))
    page_3.insert_text((450, 460), format_inr(subsidy), fontsize=12, color=(0, 0, 0))
    page_3.insert_text((450, 480), format_inr(total_investment), fontsize=12, color=(0, 0, 0))


    output_stream = io.BytesIO()
    doc.save(output_stream)  # Save modified PDF to memory
    output_stream.seek(0)
    return output_stream


st.title("Quotation Generator")

capacity = st.text_input("Project Capacity (KWp)")
kwrate = st.text_input("Rate per Wp")
gstrate = st.text_input("GST Rate %")
subsidy = st.text_input("Subsidy (INR)")

if st.button("Calculate"):
    basic_syst_cost = float(capacity) * float(kwrate) * 1000
    total_gst = float(basic_syst_cost) * (float(gstrate)/100)
    total_amount = float(basic_syst_cost) + float(total_gst)
    total_investment = float(total_amount) - float(subsidy)

    st.markdown(f"Basic System Cost: {format_inr(basic_syst_cost)}")
    st.markdown(f"GST: {format_inr(total_gst)}")
    st.markdown(f"Total Amount: {format_inr(total_amount)}")
    st.markdown(f"Subsidy: {format_inr(subsidy)}")
    st.markdown(f"Total Investement: {format_inr(total_investment)}")

quote_no = st.text_input("quote_no")
prepared_by = st.text_input("prepared_by")
client_name = st.text_input("client_name")
location = st.text_input("location")
date = st.text_input("date")

input_pdf = "sample01.pdf"

if st.button("Generate Quotation"):
    pdf_file = edit_pdf(input_pdf, quote_no, prepared_by, client_name, location, capacity, date, kwrate, gstrate, subsidy)
    st.download_button("Download Quotation", pdf_file, file_name=f"{quote_no}.pdf", mime="application/pdf")