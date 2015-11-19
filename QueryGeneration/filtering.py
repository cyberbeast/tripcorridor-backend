from parsing import Token, Entity, Pos, Number, Lemma, Palindrome, Date
from tagging import Tagger
import refo
from refo import Question, Group
from utils import Timer
from regex import Regex

timer = Timer('Time to tag and filter: ')

class DateSeason(object):
	"Object to contain the date and season data"
	def __init__(self):
		self.month = None
		self.year = None
		self.season = None
		self.day = None
		self.week = None
		self.date = None

	def __repr__(self):
		return """
	<DateSeason
		Month:{0}
		Year:{1}
		Season:{2}
	>
		""".format(self.month,self.year,self.season)

	def __str__(self):
		return repr(self)

class Filter(object):
	"Class to build filter for budget, time, and distance"
	def __init__(self, filter_type, regexes):
		for name in "unit min max exact".split():
			object.__setattr__(self,name,None)
		self.type = filter_type
		self.regexes = regexes
		self.done = False

	def apply(self, sentence):
		for regex in self.regexes:
			regex.interpret(self, sentence)
			if self.done:
				break

	def __repr__(self):
		string = """
<Filter
	type:{0}
	unit:{1}
	min:{2}
	max:{3}
	exact:{4}
>
		"""
		return string.format(self.type,self.unit,self.min,self.max,self.exact)

	def __str__(self):
		return repr(self)

class BetweenNumberAndNumberDistance(Regex):
	def __init__(self):
		regex = ((Token('in') + Token('range') + Question(Token('of'))) | \
			Token('between')) + Number('Min') + Question(Entity('distance_unit')) \
			+ (Token('and') | Token('to'))+ Number('Max') \
			+ Group(Entity('distance_unit'),'Unit')
		super(BetweenNumberAndNumberDistance, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex,sentence)
		if match:
			ir.done = True
			ir.min = get_number(match, sentence, 'Min')
			ir.max = get_number(match, sentence, 'Max')
			ir.unit = get_unit(match, sentence, 'Unit')

class UnderNumberDistance(Regex):
	def __init__(self):
		regex = (Token('under') | Token('below') | Token('before') | \
		 	Token('within'))  + Number('Max') + Group(Entity('distance_unit'),'Unit')
		super(UnderNumberDistance, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex, sentence)
		if match:
			ir.done = True
			ir.max = get_number(match, sentence, 'Max')
			ir.unit = get_unit(match, sentence, 'Unit')

class OverNumberDistance(Regex):
	def __init__(self):
		regex = ((Token('over')|Token('above')|Token('after')) + Number('Min') \
			+ Entity('distance_unit')) | (Token('from') + Number('Min') \
			+ Group(Entity('distance_unit'),'Unit') + Token('onwards'))
		super(OverNumberDistance, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex, sentence)
		if match:
			ir.done = True
			ir.min = get_number(match, sentence, 'Min')
			ir.unit = get_unit(match, sentence, 'Unit')

class ExactNumberDistance(Regex):
	def __init__(self):
		regex = (Token('at') | Token('around') | Token('about') | \
			Token('exactly') | Token('nearly') ) + Number('Exact') \
				+ Group(Entity('distance_unit'),'Unit')
		super(ExactNumberDistance, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex, sentence)
		if match:
			ir.done = True
			ir.exact = get_number(match, sentence, 'Exact')
			ir.unit = get_unit(match, sentence, 'Unit')

class BetweenNumberAndNumberCurrency(Regex):
	def __init__(self):
		regex = ((Token('in') + Token('range') + Question(Token('of'))) | \
			Token('between')) + Palindrome(Number('Min'), \
			Question(Entity('currency'))) \
			+ (Token('and') | Token('to')) \
			+ Palindrome(Number('Max'), Group(Entity('currency'),'Currency'))
		super(BetweenNumberAndNumberCurrency, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex,sentence)
		if match:
			ir.done = True
			ir.min = get_number(match, sentence, 'Min')
			ir.max = get_number(match, sentence, 'Max')
			ir.unit = get_currency(match, sentence, 'Currency')

class UnderNumberCurrency(Regex):
	def __init__(self):
		regex = (Token('under') | Token('below') | Token('before') | \
		 	Token('within'))  + Number('Max') + Group(Entity('currency'),'Currency')
		super(UnderNumberCurrency, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex, sentence)
		if match:
			ir.done = True
			ir.max = get_number(match, sentence, 'Max')
			ir.unit = get_currency(match, sentence, 'Currency')

class OverNumberCurrency(Regex):
	def __init__(self):
		regex = ((Token('over')|Token('above')|Token('after')) + Number('Min') \
			+ Entity('currency')) | (Token('from') + Number('Min') \
			+ Group(Entity('currency'),'Currency') + Token('onwards'))
		super(OverNumberCurrency, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex, sentence)
		if match:
			ir.done = True
			ir.min = get_number(match, sentence, 'Min')
			ir.unit = get_currency(match, sentence, 'Currency')

class ExactNumberCurrency(Regex):
	def __init__(self):
		regex = (Token('at') | Token('around') | Token('about') | \
			Token('exactly') | Token('nearly') ) + Number('Exact') \
				+ Group(Entity('currency'),'Currency')
		super(ExactNumberCurrency, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex, sentence)
		if match:
			ir.done = True
			ir.exact = get_number(match, sentence, 'Exact')
			ir.unit = get_currency(match, sentence, 'Currency')

class FromDateToDate(Regex):
	def __init__(self):
		regex = Lemma('from') + Date('start') + Lemma('to') + Date('stop')
		super(FromDateToDate, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex,sentence)
		if match:
			ir.done = True
			ir.min = get_date(match, sentence, 'start')
			ir.max = get_date(match, sentence, 'stop')

class FromDateOnwards(Regex):
	def __init__(self):
		regex = Lemma('from') + Date('start') + Token('onwards')
		super(FromDateOnwards, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex,sentence)
		if match:
			ir.done = True
			ir.min = get_date(match, sentence, 'start')

class BetweenDateAndDate(Regex):
	def __init__(self):
		regex = Lemma('between') + Date('start') + Lemma('and') + Date('stop')
		super(BetweenDateAndDate, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex,sentence)
		if match:
			ir.done = True
			ir.min = get_date(match, sentence, 'start')
			ir.max = get_date(match, sentence, 'stop')

class InDate(Regex):
	def __init__(self):
		regex = (Lemma('in') | Token('during'))  + Date('exact')
		super(InDate, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex,sentence)
		if match:
			ir.done = True
			ir.exact = get_date(match, sentence, 'exact')

class AfterDate(Regex):
	def __init__(self):
		regex = Token('after') + Date('start')
		super(AfterDate, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex, sentence)
		if match:
			ir.done = True
			ir.min = get_date(match, sentence, 'start')

class BeforeDate(Regex):
	def __init__(self):
		regex = Token('before') + Date('stop')
		super(BeforeDate, self).__init__(regex)

	def interpret(self, ir, sentence):
		match = refo.search(self.regex, sentence)
		if match:
			ir.done = True
			ir.max = get_date(match, sentence, 'stop')

def get_number(match, sentence, name):
	i, j = match.span(name)
	ret  = float("".join([x.token for x in sentence[i:j]]))
	if int(ret) == ret:
		ret = int(ret)
	return ret

def get_unit(match, sentence, name):
	i, j = match.span(name)
	unit = sentence[i:j][0]
	if unit.lemma in ["kilometer", "km"]:
		return "km"
	elif unit.lemma == "mile":
		return "mile"
	else:
		return "unknown"

def get_currency(match, sentence, name):
	i, j = match.span(name)
	currency = sentence[i:j][0]
	return currency.lemma

def get_date(match, sentence, name):
	date_season = DateSeason()
	date_season.month = get_month(match, sentence, name)
	date_season.year = get_year(match, sentence, name)
	date_season.season = get_season(match, sentence, name)
	return date_season

def get_season(match, sentence, name):
	i, j = match.span(name)
	season = sentence[i:j]
	match = refo.search(Group(Entity('season'),'s'),season)
	if match:
		i, j = match.span('s')
		season = season[i:j][0]
		return season.token

def get_month(match, sentence, name):
	i, j = match.span(name)
	month = sentence[i:j]
	match = refo.search(Group(Entity('month'),'m'),month)
	if match:
		i, j = match.span('m')
		month = month[i:j][0]
		return month.token

def get_year(match, sentence, name):
	i, j = match.span(name)
	year = sentence[i:j]
	match = refo.search(Group(Entity('year'),'y'),year)
	if match:
		i, j = match.span('y')
		year = year[i:j][0]
		return year.token

sentences = [
	"Find site between 500 and 1000 kms from Bangalore",
	"Sites under 200 miles",
	"places in range 100 to 745.4 km",
	"hotel from 555 kilometers onwards at Finland",
	"Locate hotel at 10 miles from Kashi"
]

sentences2 = [
	"hotels under 200 rupees",
	"spots in Bangalore in range of dollar 200 to 500", #Not yet supported
	"spots in Bangalore in range of 200 to 500 dollar",
	"resort at 234 euros in Finland"
]

sentences3 = [
	"during june 2016",
	"in october",
	"in 2022",
	"after july",
	"before september 2020",
	"between summer and autumn",
	"from 2015 onwards",
	"from june 2014 to winter 2015"
]
def main():
	tagger = Tagger()
	for sentence in sentences:
		print "query: ", sentence
		sentence = tagger.tag(sentence.lower())
		distance_filter = Filter(filter_type = "distance",
			regexes = [
				BetweenNumberAndNumberDistance(),
				UnderNumberDistance(),
				OverNumberDistance(),
				ExactNumberDistance()
			]
		)
		distance_filter.apply(sentence)
		print distance_filter
		print '-' * 80

def main2():
	tagger = Tagger()
	for sentence in sentences2:
		print "query: ", sentence
		sentence = tagger.tag(sentence.lower())
		budget_filter = Filter(filter_type = "budget",
			regexes = [
				BetweenNumberAndNumberCurrency(),
				UnderNumberCurrency(),
				OverNumberCurrency(),
				ExactNumberCurrency()
			]
		)
		budget_filter.apply(sentence)
		print budget_filter
		print '-' * 80

def main3():
	tagger = Tagger()
	for sentence in sentences3:
		print "query: ", sentence
		sentence = tagger.tag(sentence.lower())
		time_filter = Filter(filter_type = "time",
			regexes = [
				FromDateToDate(),
				FromDateOnwards(),
				BetweenDateAndDate(),
				InDate(),
				AfterDate(),
				BeforeDate()
			]
		)
		time_filter.apply(sentence)
	
		print time_filter
		print '-' * 80

def get_filters():
	budget_filter = Filter(filter_type = "budget",
		regexes = [
			BetweenNumberAndNumberCurrency(),
			UnderNumberCurrency(),
			OverNumberCurrency(),
			ExactNumberCurrency()
		]
	)
	distance_filter = Filter(filter_type = "distance",
		regexes = [
			BetweenNumberAndNumberDistance(),
			UnderNumberDistance(),
			OverNumberDistance(),
			ExactNumberDistance()
		]
	)
	time_filter = Filter(filter_type = "time",
		regexes = [
			FromDateToDate(),
			FromDateOnwards(),
			BetweenDateAndDate(),
			InDate(),
			AfterDate(),
			BeforeDate()
		]
	)
	return budget_filter, distance_filter, time_filter

def generate_filtered_data(query, tagged = False, verbose = False, timeit = False):
	if verbose: print 'Query: ', query
	if not tagged:
		if verbose: print 'tagging...'
		tagger = Tagger()
		if timeit: timer.start()
		query = tagger.tag(query.lower())
	if verbose: print 'filter...'
	filtered_data = []
	for my_filter in get_filters():
		my_filter.apply(query)
		if verbose: print my_filter
		filtered_data.append(my_filter)
	if timeit: timer.stop()
	if verbose: print timer.message()
	return filtered_data


def demo():
	print '<' * 10 + 'Distance filters demo' + '>' * 10
	main()
	print '<' * 10 + 'Budget filters demo' + '>' * 10
	main2()
	print '<' * 10 + 'Date and Season filters demo' + '>' * 10
	main3()

def demo2():
	myquery = """
	find all place in bangalore, under 2000 dollar, in range of 200 to 500 kms,
	to visit after december 2016.
	"""
	generate_filtered_data(myquery, verbose = True, timeit = True)

if __name__ == '__main__':
	#demo()
	demo2()
