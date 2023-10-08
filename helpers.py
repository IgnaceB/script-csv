import pandas as pd
import streamlit as st
import json 
import re


class CSV :
	tag = "generic"
	def __init__(self, df) :
		self.df = df
	def process(self):
		pass
	def describe(self):
		print(self.df)
	def model(self):
		pass
	def export(self):
		return self.df.to_csv(index=False, sep=';').encode('utf-8')

class CSV_OD(CSV) :
	def model(self) :
		d = {'Document':[""],
		 'Date de calcul':[""],
		 'Numéro de référence':[""],
		 'Analitique':[""],
		 'Numéro de compte':[""],
		 'Libellé du compte':[""],
		 'Débit':[""],
		 'Crédit':[""],
		 }
		df = pd.DataFrame(data=d, index=[0])
		return df

	def transform_element(self, element, external_data):
		    if element in external_data:
		        return external_data[element]
		    else:
		        return element

	def process(self,input) :
		with open("data.json","r") as data:
   			jsonData = json.load(data)
		model_df=self.model()

		for rows in range(len(self.df.index)):
			model_df.loc[rows]=[None,None,None,None,None,None,None,None]
		
		model_df.loc[0] = [input,self.df.at[0,'Date de calcul'],self.df.at[0,'Numéro de référence'],None,None,None,None,None]
		model_df.loc[:,'Numéro de compte'] = self.df.loc[:,'Numéro de compte']
		model_df.loc[:,'Libellé du compte'] = self.df.loc[:,'Libellé du compte']
		model_df.loc[:,'Débit'] = self.df.loc[:,'Débit']
		model_df.loc[:,'Crédit'] = self.df.loc[:,'Crédit']
		# model_df.loc[:,'Analitique'] = self.df.loc[:,'Analitique']
		dict_analitique={}
		for rows in range(len(self.df.index)):
		
			if str(self.df.at[rows,'Analitique']) != 'nan' :
				cell_value = str(self.df.at[rows,'Analitique'])
				list_analitique = re.findall(r'[^,\s]+',cell_value)
				dict_analitique[rows] = list_analitique
				# model_df.at([rows,'Analitique'])=data[self.df.at([rows,'Analitique'])]
			print(dict_analitique)
				
		transformed_dict={}
		
		for key, value_list in dict_analitique.items() :
			transformed_list=[self.transform_element(element, jsonData) for element in value_list]
			transformed_dict[key] = transformed_list
	
		for key, values in transformed_dict.items() :
			model_df.at[key,'Analitique']=values
		self.df=model_df
		
		return model_df
		

	
