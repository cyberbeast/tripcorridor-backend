class Extractor:
	"""
		Abstract class that extracts various values and
		entities. Entities are supplied by the Supplier() object.
	"""
	def __init__(self):
		pass

class Supplier:
	"""
		An object that supplies values of Entities from the 
		database. It includes entities like Country, State,
		District, Category of a destination, MajorDestination,
		Amenity in hotel etc.
	"""
	def __init__(self):
		pass

class Killer(object):
	"""docstring for Killer"""
	def __init__(self, arg):
		super(Killer, self).__init__()
		self.arg = arg
		
		