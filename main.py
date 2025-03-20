import streamlit as st
import fitz
from babel.numbers import format_currency
import io
import math
import datetime

st.set_page_config(page_title="Solar Quotation", page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)

st.sidebar.markdown("# System Details")

if "panel_input" not in st.session_state:
    st.session_state.panel_input = 6

if "actual_cap" not in st.session_state:
    st.session_state.actual_cap = 3.27

if "inverter_value" not in st.session_state:
    st.session_state.inverter_value = "3"

def format_inr(amount):
    return format_currency(amount, 'INR', locale='en_IN').replace("₹", "Rs ").strip()

def edit_pdf(input_pdf, capacity, kwrate, gstrate, subsidy, panel_wp, no_panel, inverter, quote_no, prepared_by, client_name, location, date):

    if not input_pdf:
        st.toast('Sample PDF Error')
        return
          
    if not capacity or not kwrate or not gstrate or not subsidy or not panel_wp:
        st.toast('Enter Capacity/ Rate/ Gst/ Subsidy/ Panel')
        return

    if not no_panel or not inverter or not quote_no or not prepared_by or not client_name or not location or not date:
        st.toast('Data is missing')
        return

    try:
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
        
        page_5 = doc[4]
        page_5.insert_text((210, 242), str(no_panel)+ " Nos", fontsize=11, color=(0, 0, 0))
        page_5.insert_text((340, 242), str(panel_wp)+ "wp", fontsize=11, color=(0, 0, 0))
        page_5.insert_text((340, 284), str(inverter)+ " KW", fontsize=11, color=(0, 0, 0))

        output_stream = io.BytesIO()
        doc.save(output_stream)  # Save modified PDF to memory
        output_stream.seek(0)
        return output_stream
    except:
        st.toast('Create Pdf Error')



def calc_fun():
    try:
        basic_syst_cost = float(capacity) * float(kwrate) * 1000
        total_gst = float(basic_syst_cost) * (float(gstrate)/100)
        total_amount = float(basic_syst_cost) + float(total_gst)
        total_investment = float(total_amount) - float(subsidy)
        st.session_state.inverter_value = math.floor(float(capacity))
        
        st.sidebar.markdown(f"Basic System Cost: {format_inr(basic_syst_cost)}")
        st.sidebar.markdown(f"GST: {format_inr(total_gst)}")
        st.sidebar.markdown(f"Total Amount: {format_inr(total_amount)}")
        st.sidebar.markdown(f"Subsidy: {format_inr(subsidy)}")
        st.sidebar.markdown(f"Total Investement: {format_inr(total_investment)}")
        st.sidebar.markdown(f"No of Panels: {st.session_state.panel_input}")
        st.sidebar.markdown(f"Capacity: {st.session_state.actual_cap}")
        st.sidebar.markdown(f"Inverter: {(st.session_state.inverter_value)} KW")

        st.toast("System Details Generate!")
    except:
        st.toast('Calculation Error')


def panel_changed():
    try:
        actual_capacity = int(panel_wp) * st.session_state.panel_input / 1000
        st.session_state.actual_cap = actual_capacity
        st.toast(f"Panels change to {st.session_state.panel_input}")

    except:
        st.toast('No of Panel change Error')

st.markdown("## Quotation Generator")

a_col1, a_col2, a_col3, a_col4, a_col5, a_col6 = st.columns([1, 1, 1, 1, 1, 1])

panel_wp = a_col1.text_input("Panel (W)","545")
no_panel = a_col2.number_input("No of Panels", min_value=1, max_value=100, step=1, key="panel_input", on_change=panel_changed)
capacity = a_col3.text_input("Capacity (KWp)", value=st.session_state.actual_cap)
kwrate = a_col4.text_input("Rate per Wp","60")
gstrate = a_col5.text_input("GST Rate %","13.8")
subsidy = a_col6.text_input("Subsidy","78000")


st.button("Calculate", on_click= calc_fun, use_container_width=True)


b_col1, b_col2, b_col3 = st.columns([1, 1, 1])
inverter = b_col1.text_input("Inverter (KW)", value = st.session_state.inverter_value)
quote_no = b_col2.text_input("quote_no")
prepared_by = b_col3.text_input("prepared_by","Nikhil Pisal")

c_col1, c_col2, c_col3 = st.columns([1, 1, 1])
client_name = c_col1.text_input("client_name")
location = c_col2.text_input("location","Pune")

default_date = datetime.date.today()
formatted_date = default_date.strftime("%d-%m-%Y")
# date = c_col3.date_input("Select a date:", value=default_date, format="DD-MM-YYYY")
date = c_col3.text_input("Date",value=formatted_date)

input_pdf = "sample01.pdf"

if st.button("Generate Quotation", use_container_width=True):
    pdf_file = edit_pdf(input_pdf, capacity, kwrate, gstrate, subsidy, panel_wp, no_panel, inverter, quote_no, prepared_by, client_name, location, date)
    if pdf_file:
        st.download_button("Download Quotation", pdf_file, file_name=f"{quote_no}.pdf", mime="application/pdf")
    else:
        st.toast('PDF File Error')
