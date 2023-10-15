import pandas as pd
import streamlit as st
import json 
import re
import lxml

def removedoc(document):
	print("carentre")
	document=None

class CSV :
	tag = "generic"
	def __init__(self,df, upload) :
		self.upload = upload
		self.df = df
	def process(self):
		pass
	def describe(self):
		return self.df
	def model(self):
		pass
	def export(self):
		return self.df.to_csv(index=False, sep=';').encode('latin-1')
	def name(self):
		return re.sub(r'.csv','',str(self.upload.name))

class CSV_XML(CSV) :
	def export(self) :
		self.df.columns=[col.replace(" ","_") for col in self.df.columns]
		return self.df.to_xml(index=False)


class CSV_OD(CSV) :
	# definit le modele du document final
	def model(self) :
		d = {'Numéro':[""],
		 'Référence':[""],
		 'Date':[""],
		 'Ecriture comptable / Compte':[""],
		 'Ecriture comptable / libellé':[""],
		 'Ecriture comptable / Débit':[""],
		 'Ecriture comptable / Crédit':[""],
		 'Ecriture comptable / Lignes analytiques / Compte analytique':[""],

		 }
		df = pd.DataFrame(data=d, index=[0])
		return df
	# match les éléments avec les data contenue dans les .json
	def match_element(self, element, external_data):
		    if element in external_data:
		        return external_data[element]
		    else:
		        return element

    # transforme le dataframe reçu en copiant les valeurs dans le dataframe model
	def process(self,input) :
		print(self.df)
		# upload json
		with open("data.json","r") as data:
   			jsonData = json.load(data)
		model_df=self.model()

		# remplit le model avec le nombre de colonnes du dataframe 
		for rows in range(len(self.df.index)):
			model_df.loc[rows]=[None,None,None,None,None,None,None,None]
		
		# définis les champs unique de la première ligne
		model_df.loc[0] = [input,self.df.at[0,'Date de calcul'],self.df.at[0,'Numéro de référence'],None,None,None,None,None]
		
		# définis les champs copié/collé des autres lignes
		model_df.loc[:,'Ecriture comptable / Compte'] = self.df.loc[:,'Numéro de compte']
		model_df.loc[:,'Ecriture comptable / libellé'] = self.df.loc[:,'Libellé du compte']
		model_df.loc[:,'Ecriture comptable / Débit'] = self.df.loc[:,'Débit']
		model_df.loc[:,'Ecriture comptable / Crédit'] = self.df.loc[:,'Crédit']

		# récupère les valeurs de la clé analytique et stock dans dict_analitique key = rows
		dict_analitique={}
		for rows in range(len(self.df.index)):
		
			if str(self.df.at[rows,'Analitique']) != 'nan' :
				cell_value = str(self.df.at[rows,'Analitique'])
				list_analitique = re.findall(r'[^,\s]+',cell_value)
				dict_analitique[rows] = list_analitique
			# print(dict_analitique)
				
		transformed_dict={}
		
		# transforme les valeurs avec le dictionnaire data.json et stock dans transformed_dict key=rows
		for key, value_list in dict_analitique.items() :
			transformed_object={f'"{self.match_element(element, jsonData)}"' : 100.00 for element in value_list }

			transformed_dict[key] = transformed_object
			
	
		# insert les valeurs dans le model sur base de key=rows du transformed_dict
		for key, values in transformed_dict.items() :
		# transforme les '' en ""
			my_updated_string = re.sub(r"'", '', str(values))

			model_df.at[key,'Ecriture comptable / Lignes analytiques / Compte analytique']=my_updated_string

		


		# change le dataframe de l'object pour le dataframe du modèle
		self.df=model_df
		
		return model_df
		

	
