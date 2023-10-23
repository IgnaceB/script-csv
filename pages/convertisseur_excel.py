import streamlit as st
import pandas as pd
import helpers as helpers
import re

st.set_page_config(
	page_title="Convertisseur Excel"
	)

upload = st.file_uploader("upload file", type={"xlsx"})


if upload is not None:
	upload_df = pd.read_excel(upload)
	upload_df.sort_values(by=['concatenation interne'])
	st.write(upload_df)


options=["","Export to XML"]

option = st.selectbox(
    'Which excel are you uploading ?',
     options)



if upload is not None :
	if option=='Export to XML' :
		try:
			csv=helpers.CSV_XML(upload_df, upload)
			st.write(csv)
			st.download_button(
				"Press to Download",
				   csv.export(),
				   f"{csv.name()}.xml",
				   "xml",
				   key='download-csv', 
				)
		except Exception as e:
			st.warning(f"erreur : {e}), veuillez contacter le webmaster")
			raise e