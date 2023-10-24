import streamlit as st
import pandas as pd
import helpers as helpers
import re
# import openpyxl
# import streamlit_authenticator as stauth


st.set_page_config(
	page_title="Convertisseur CSV"
	)

upload = st.file_uploader("upload file", type={"csv"})


if upload is not None:
	upload_df = pd.read_csv(upload, sep=';' , encoding='latin-1')
	st.write(upload_df)


# options=["","Import des comptes","Export to XML"]
options=["","Import des comptes"]


option = st.selectbox(
    'Which csv are you uploading ?',
     options)



if upload is not None :
	if option=="Import des comptes":
		
		try :

			csv= helpers.CSV_OD(upload_df, upload)
			document = st.text_input("numero de document")
			# model = csv.process(document)
			# st.write(model)
		
			if document :
				model = csv.process(document)
				st.write(model)
				st.download_button(
				   "Press to Download",
				   csv.export(),
				   f"{document}.csv",
				   "text/csv",
				   key='download-csv', 
				)
			else : 
				st.warning("Veuillez entrer un numéro de document")
		except Exception as e :
			print(e)
			st.warning(f"mauvais format de csv (erreur : {e}), veuillez vous référez au modèle ci-dessous")
			st.write(helpers.CSV_OD(upload_df,upload).model())
	elif option=='Export to XML' :
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
		