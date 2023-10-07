import streamlit as st
import pandas as pd
# import helpers.py as helpers

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")



spectra = st.file_uploader("upload file", type={"csv"})

# def modify_OD(df) :
# 	df2 = df.iloc[:,0]
# 	return df2

if spectra is not None:
	spectra_df = pd.read_csv(spectra)
	st.write(spectra_df)
	
	


df = pd.DataFrame({
    'first column': ["OD", "ITEMS"],
    })

option = st.selectbox(
    'Which csv are you uploading?',
     df['first column'])

'You selected: ', option




if spectra is not None and option=="OD":

	selected_column= modify_OD(spectra_df)

	def convert_df(df):
   		return df.to_csv(index=False).encode('utf-8')

	csv = convert_df(selected_column) 

	st.download_button(
	   "Press to Download",
	   csv,
	   "file.csv",
	   "text/csv",
	   key='download-csv'
	)