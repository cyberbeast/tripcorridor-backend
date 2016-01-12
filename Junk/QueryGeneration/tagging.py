import nltk, json, time
from utils import Logger, Timer
import settings

logger = Logger("tagger_test.txt")
timer = Timer("Time to tag: ")


class EntityTagger(object):
	"""
		Named Entity Recognition.
		Tag the Word object to one of the categories in *entities.json*
	"""
	def __init__(self,filename):
		with open(filename,'r') as data:
			data = json.load(data)
			for key, value in data.iteritems():
				self.__setattr__(key,value)

	def NER(self, token):
		ner = []
		categories = "country state district subdistrict year season \
		month day currency distance_unit".split()
		for name in categories:
			entity_set = set(getattr(self,name,u"-"))
			if entity_set != u"-":
				if token.lower() in entity_set:
					ner.append(name)
		return ner


class Word(object):
	"""
		Container for the words in the query.
		Just an objectified dictionary.
	"""
	def __init__(self, token, lemma=None, pos=None, entities=[]):
		self.entities = entities
		self.lemma = lemma
		self.pos = pos
		self.token = token

	def __setattr__(self, name, value):
		if name in u"token lemma pos entities".split():
			object.__setattr__(self, name, value)

	def __unicode__(self):
		attrs = (getattr(self, name, u"--") for name in u"token lemma pos entities".split())
		return u"|".join(str(x) for x in attrs)

	def __repr__(self):
		return unicode(self)


class Tagger:
	"""
		Takes care of:
		1. Tokenization
		2. POS Tagging
		3. Lemmatization
		4. NER Tagging
	"""
	def __init__(self):
		nltk.data.path = settings.NLTK_DATA_PATH
		from nltk.corpus import wordnet
		self.wordnet = wordnet
		self._penn_to_morphy_tag = {
				u'NN': wordnet.NOUN,
				u'JJ': wordnet.ADJ,
				u'VB': wordnet.VERB,
				u'RB': wordnet.ADV,
			}
		self.entity_tagger = EntityTagger("entities.json")
		self.PENN_TAGSET = set(u"$ `` '' ( ) , -- . : CC CD DT EX FW IN "
			"JJ JJR JJS LS MD NN NNP NNPS NNS PDT POS PRP PRP$ RB RBR RBS"
			"RP SYM TO UH VB VBD VBG VBN VBP VBZ WDT WP WP$ WRB".split())

	def penn_to_morphy_tag(self,tag):
		for penn, morphy in self._penn_to_morphy_tag.iteritems():
			if tag.startswith(penn):
				return morphy
		return None

	def tag(self,string):
		tokens = nltk.wordpunct_tokenize(string)
		tags = nltk.pos_tag(tokens)

		words = []
		for token, pos in tags:
			
			#print "token: ", token
			word = Word(token)
			word.pos = pos.split("|")[0].decode("ascii")

			
			#print "pos: ", word.pos, type(word.pos)

			mtag = self.penn_to_morphy_tag(word.pos)
			lemma = self.wordnet.morphy(word.token, pos=mtag)

			#print "lemma: ", lemma, type(lemma)

			if isinstance(lemma, str):
				lemma = lemma.decode("ascii")
			word.lemma = lemma
			
			if word.lemma is None:
				word.lemma = word.token.lower()
			
			if word.pos in ["NNP","NN"]:			
				word.entities = self.entity_tagger.NER(word.token)
			
			#print word.token, word.entities
			#print word #print ""

			words.append(word)

		for word in words:
			if word.pos not in self.PENN_TAGSET:
				logger.dump("Tagger emmited a non-penn "
							   "POS tag {!r}".format(word.pos))
		return words


if __name__ == '__main__':
	tagger = Tagger()
	timer.start()
	words = tagger.tag("Tell me some hotels in Bangalore and Delhi Mysore".lower())
	timer.stop()
	logger.dump(words)
	logger.dump(timer.message())
	entity_tagger = EntityTagger("entities.json")
	logger.dump("Entities are: ")
	logger.dump(entity_tagger.country)
