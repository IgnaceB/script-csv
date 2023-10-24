import streamlit as st
import pandas as pd
import helpers as helpers
import re
import pyarrow as pa
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import openpyxl
import xml.dom.minidom

st.set_page_config(
	page_title="Convertisseur Excel"
	)

upload = st.file_uploader("upload file", type={"xlsx"})


if upload is not None:
	upload_df = pd.read_excel(upload)

	excelDf = helpers.EXCEL_XML(upload_df,upload)
	excelDf.preprocess()
	st.write(excelDf.describe())


options=["","Export to XML"]

option = st.selectbox(
    'Which excel are you uploading ?',
     options)



if upload is not None :
	if option=='Export to XML' :
		date = st.date_input("date de création du document")
		if date :  
			excelDf.convert_to_xml(date)
			try:
				st.download_button(
				"Télécharger le fichier XML",
				excelDf.export(),
				f"{excelDf.name()}.xml",
				"xml",
				key='download-xml'
					)
			except Exception as e:
				st.warning(f"erreur : {e}), veuillez contacter le webmaster")
				raise e