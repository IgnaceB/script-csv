import streamlit as st
import pandas as pd
import helpers as helpers

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

upload = st.file_uploader("upload file", type={"csv"})

if upload is not None:
	upload_df = pd.read_csv(upload)
	st.write(upload_df)


options=["OD","ITEMS"]

option = st.selectbox(
    'Which csv are you uploading?',
     options)

'You selected: ', option


if upload is not None :
	if option=="OD"
		csv= helpers.CSV_OD(upload_df)
	csv.process()
	st.download_button(
	   "Press to Download",
	   csv.export(),
	   "file.csv",
	   "text/csv",
	   key='download-csv'
	)