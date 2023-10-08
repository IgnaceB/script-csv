import streamlit as st
import pandas as pd
import helpers as helpers


st.markdown("# Convertisseur CSV  ")
st.sidebar.markdown("# Convertisseur CSV ")


upload = st.file_uploader("upload file", type={"csv"})

if upload is not None:
	upload_df = pd.read_csv(upload, sep=';' , encoding='latin-1')
	st.write(upload_df)



options=["Import des comptes"]

option = st.selectbox(
    'Which csv are you uploading?',
     options)



if upload is not None :
	if option=="Import des comptes":
		
		try :

			csv= helpers.CSV_OD(upload_df)
			document = st.text_input("numero de document")
			model = csv.process(document)
			st.write(model)
		
			if document :
				
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
			st.write(helpers.CSV_OD(upload_df).model())

		