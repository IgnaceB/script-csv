import pandas as pd
import streamlit as st
import json 
import re
import lxml
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import openpyxl
import xml.dom.minidom

def removedoc(document):
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
		# upload json
		with open("data.json","r") as data:
   			jsonData = json.load(data)
		model_df=self.model()

		# définis les champs unique de la première ligne 
		model_df.loc[0] = [input,self.df.at[0,'Numéro de référence'],self.df.at[0,'Date de calcul'],None,None,None,None,None]
		# définis les champs copié/collé des autres lignes

		# récupère les valeurs de la clé analytique et stock dans dict_analitique key = rows
		dict_analitique={}
		for rows in range(len(self.df.index)):
			model_df.at[rows,'Ecriture comptable / Lignes analytiques / Compte analytique']=None
			if str(self.df.at[rows,'Analitique']) != 'nan' :
				cell_value = str(self.df.at[rows,'Analitique'])
				list_analitique = re.findall(r'[^,\s]+',cell_value)
				# adaptation : insertion de la transformation d'objet dans le dict_analitique
				transformed_object={f'"{self.match_element(element, jsonData)}"' : 100.00 for element in list_analitique }
				dict_analitique[rows] = transformed_object
	
		for key, values in dict_analitique.items() :
		# transforme les '' en ""
			my_updated_string = re.sub(r"'", '', str(values))

			model_df.at[key,'Ecriture comptable / Lignes analytiques / Compte analytique']=my_updated_string
		
		# définis les champs copié/collé des autres lignes	
		model_df['Ecriture comptable / Compte'] = self.df['Numéro de compte']
		model_df['Ecriture comptable / libellé'] = self.df['Libellé du compte']
		model_df['Ecriture comptable / Débit'] = self.df['Débit']
		model_df['Ecriture comptable / Crédit'] = self.df['Crédit']
		


		# change le dataframe de l'object pour le dataframe du modèle
		self.df=model_df
		
		return model_df
		

	
class EXCEL_XML :
	tag = "generic"
	def __init__(self,df, upload) :
		self.upload = upload
		self.df = df
	def preprocess(self):
		df=self.df
		self.df['InternalNumber'] = df['InternalNumber'].astype(str)
		self.df['ContractNumber'] = df['ContractNumber']
		self.df['Date'] = df['Date'].astype(str)
		self.df['NumberOfHours'] = pd.to_numeric(df['NumberOfHours'], errors='coerce')
		self.df=df.dropna()
		return self.df
	def process(self):
		pass
	def describe(self):
		return self.df
	def model(self):
		pass
	def name(self):
		return re.sub(r'.xlsx','',str(self.upload.name))
	def export(self):
		decode_xml = tostring(self.root, encoding="utf-8").decode()
		xml_fromString = xml.dom.minidom.parseString(decode_xml)
		pretty_xml = xml_fromString.toprettyxml()
		return pretty_xml


class EXCEL_STUDENTS_XML(EXCEL_XML):
	def convert_to_xml(self, input):
	# Créer un élément racine XML
		root = Element("RegisterTime")
		creation_date = SubElement(root, "CreationDate")
		creation_date.text = str(input)

		# Créer un élément "ContractEntries"
		contract_entries = SubElement(root, "ContractEntries")

		allStudentsObjects={}

		# Parcourir les données du DataFrame

		for index, row in self.df.iterrows():
			key = str(row['InternalNumber'])+str(row['ContractNumber'])

			if key not in allStudentsObjects:
				allStudentsObjects[key] = {
				"internal_number": row['InternalNumber'],
				"contract_number": int(row['ContractNumber']),
				"presta": {
				    row['Date']: {
				        "date": [row['Date']],
				        "payment_code": [row['PaymentCode']],
				        "number_of_hours": [row['NumberOfHours']],
				        "cost_center_code": [row['CostCenterCode']]
				    }
				},
				"salary_code": "0000",
				}
			else:
				if row['Date'] not in allStudentsObjects[key]['presta']:
					allStudentsObjects[key]['presta'][row['Date']] = {
					"date": [row['Date']],
					"payment_code": [row['PaymentCode']],
					"number_of_hours": [row['NumberOfHours']],
					"cost_center_code": [row['CostCenterCode']]
					}
				else:
					allStudentsObjects[key]['presta'][row['Date']]['payment_code'].append(row['PaymentCode'])
					allStudentsObjects[key]['presta'][row['Date']]['number_of_hours'].append(row['NumberOfHours'])
					allStudentsObjects[key]['presta'][row['Date']]['cost_center_code'].append(row['CostCenterCode'])


		
		for key, student_data in allStudentsObjects.items():
			contract_entry = SubElement(contract_entries, "ContractEntry")

			# Create the ContractLogicalKey element
			contract_logical_key = SubElement(contract_entry, "ContractLogicalKey")
			office_code = SubElement(contract_logical_key, "OfficeCode")
			office_code.text = "612"
			functional_number = SubElement(contract_logical_key, "FunctionalNumber")
			functional_number.text = "164"
			internal_number_element = SubElement(contract_logical_key, "InternalNumber")
			internal_number_element.text = str(student_data["internal_number"])
			contract_number_element = SubElement(contract_logical_key, "ContractNumber")
			contract_number_element.text = str(student_data["contract_number"])

			date_entries = SubElement(contract_entry, "DateEntries")

			for date, presta_data in student_data["presta"].items():
				date_entry = SubElement(date_entries, "DateEntry")
				date_element = SubElement(date_entry, "Date")
				date_element.text = date

				calendars = SubElement(date_entry, "Calendars")
				for index in range(len(presta_data['payment_code'])) :
					calendar = SubElement(calendars, "Calendar")
					combined_salary_code = SubElement(calendar, "CombinedSalaryCode")
					salary_code_element = SubElement(combined_salary_code, "SalaryCode")
					salary_code_element.text = "0000"
					payment_code_element = SubElement(calendar, "PaymentCode")
					payment_code_element.text = str(presta_data["payment_code"][index])
					number_of_hours_element = SubElement(calendar, "NumberOfHours")
					number_of_hours_element.text = str(presta_data["number_of_hours"][index])

				cost_centers = SubElement(date_entry, "CostCenters")
				for index in range(len(presta_data['payment_code'])) :
					cost_center = SubElement(cost_centers, "CostCenter")
					cost_center_code = SubElement(cost_center, "CostCenterCode")
					cost_center_code.text=str(presta_data["cost_center_code"][index])
					number_of_hours_element = SubElement(cost_center, "NumberOfHours")
					number_of_hours_element.text = str(presta_data["number_of_hours"][index])

		self.root = root
		return root

class EXCEL_EMPLOYEES_XML(EXCEL_XML):
	def convert_to_xml(self, input):
	# Créer un élément racine XML
		root = Element("RegisterTime")
		creation_date = SubElement(root, "CreationDate")
		creation_date.text = str(input)

		# Créer un élément "ContractEntries"
		contract_entries = SubElement(root, "ContractEntries")

		allStudentsObjects={}

		# Parcourir les données du DataFrame

		for index, row in self.df.iterrows():
			key = str(row['InternalNumber'])+str(row['ContractNumber'])

			if key not in allStudentsObjects:
				allStudentsObjects[key] = {
				"internal_number": row['InternalNumber'],
				"contract_number": int(row['ContractNumber']),
				"presta": {
				    row['Date']: {
				        "date": [row['Date']],
				        "payment_code": [''],
				        "number_of_hours": [row['NumberOfHours']],
				        "cost_center_code": [row['CostCenterCode']],
				        "salary_code" : [row['SalaryCode']],
						"salary_subcode" : [row['SalarySubCode']],
						"numerator" : [row['Numerator']],
				    }
				},
				"salary_code": "0000",
				}
			else:
				if row['Date'] not in allStudentsObjects[key]['presta']:
					allStudentsObjects[key]['presta'][row['Date']] = {
					"date": [row['Date']],
					"payment_code": [''],
					"number_of_hours": [row['NumberOfHours']],
					"cost_center_code": [row['CostCenterCode']],
					"salary_code" : [row['SalaryCode']],
					"salary_subcode" : [row['SalarySubCode']],
					"numerator" : [row['Numerator']],
					}
				else:
					allStudentsObjects[key]['presta'][row['Date']]['payment_code'].append('')
					allStudentsObjects[key]['presta'][row['Date']]['number_of_hours'].append(row['NumberOfHours'])
					allStudentsObjects[key]['presta'][row['Date']]['cost_center_code'].append(row['CostCenterCode'])
					allStudentsObjects[key]['presta'][row['Date']]['salary_code'].append(row['SalaryCode'])
					allStudentsObjects[key]['presta'][row['Date']]['salary_subcode'].append(row['SalarySubCode'])
					allStudentsObjects[key]['presta'][row['Date']]['numerator'].append(row['Numerator'])


		
		for key, student_data in allStudentsObjects.items():
			contract_entry = SubElement(contract_entries, "ContractEntry")

			# Create the ContractLogicalKey element
			contract_logical_key = SubElement(contract_entry, "ContractLogicalKey")
			office_code = SubElement(contract_logical_key, "OfficeCode")
			office_code.text = "612"
			functional_number = SubElement(contract_logical_key, "FunctionalNumber")
			functional_number.text = "164"
			internal_number_element = SubElement(contract_logical_key, "InternalNumber")
			internal_number_element.text = str(student_data["internal_number"])
			contract_number_element = SubElement(contract_logical_key, "ContractNumber")
			contract_number_element.text = str(student_data["contract_number"])

			date_entries = SubElement(contract_entry, "DateEntries")

			for date, presta_data in student_data["presta"].items():
				date_entry = SubElement(date_entries, "DateEntry")
				date_element = SubElement(date_entry, "Date")
				date_element.text = date

				calendars = SubElement(date_entry, "Calendars")
				for index in range(len(presta_data['payment_code'])) :
					calendar = SubElement(calendars, "Calendar")
					combined_salary_code = SubElement(calendar, "CombinedSalaryCode")
					salary_code_element = SubElement(combined_salary_code, "SalaryCode")
					salary_code_element.text = "0000"
					payment_code_element = SubElement(calendar, "PaymentCode")
					payment_code_element.text = str(presta_data["payment_code"][index])
					number_of_hours_element = SubElement(calendar, "NumberOfHours")
					number_of_hours_element.text = str(presta_data["number_of_hours"][index])
				
				salary_components = SubElement(date_entry,"SalaryComponents")
				for index in range(len(presta_data['payment_code'])) :
					salary_component = SubElement(salary_components, "SalaryComponent")
					combined_salary_code = SubElement(salary_component, "CombinedSalaryCode")
					salary_code = SubElement(combined_salary_code,"SalaryCode")
					salary_code.text=str(presta_data["salary_code"][index])
					salary_sub_code = SubElement(combined_salary_code,"SalarySubCode")
					salary_sub_code.text=str(presta_data["salary_subcode"][index])
					factors = SubElement(salary_component, "Factors")
					factor = SubElement(factors, "Factor")
					number = SubElement(factor, "Number")
					number.text='1'
					numerator = SubElement(factor, "Numerator")
					numerator.text = str(presta_data["numerator"][index])
				
				cost_centers = SubElement(date_entry, "CostCenters")
				for index in range(len(presta_data['payment_code'])) :
					cost_center = SubElement(cost_centers, "CostCenter")
					cost_center_code = SubElement(cost_center, "CostCenterCode")
					cost_center_code.text=str(presta_data["cost_center_code"][index])
					number_of_hours_element = SubElement(cost_center, "NumberOfHours")
					number_of_hours_element.text = str(presta_data["number_of_hours"][index])

		self.root = root
		return root