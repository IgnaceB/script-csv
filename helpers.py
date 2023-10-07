class CSV :
	tag = "generic"
	def __init__(self, df) :
		self.df = df
	def process(self):
		pass
	def describe(self):
		print(self.df)
	def export(self):
		return self.df.to_csv(index=False).encode('utf-8')

class CSV_OD(CSV) :
	
	def process(self) :
		self.df=self.df.iloc[:,0]

	
		