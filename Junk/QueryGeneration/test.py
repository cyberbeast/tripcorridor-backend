import nltk


sent = "Tell me some hotels in Bangalore and Delhi Mysore".lower()

chunks = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)), binary = True)

probable_named_entity = []

chunks.draw()


for chunk in chunks:
	if isinstance(chunk,nltk.tree.Tree): # and chunk.label() == "NE":
		#print chunk, type(chunk)
		elem = []
		for node in chunk:
			print node, type(node)
			elem.append(node[0])
		elem = " ".join(elem)
		if elem:
			probable_named_entity.append(elem)

print probable_named_entity