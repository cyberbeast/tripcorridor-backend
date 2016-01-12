import refo
from regex import Regex
from parsing import Token, Entity, Pos, Number, Lemma, Date
from refo import Question, Group

class Selector(object):
    """
    Object to model intermediate representation for the selector used to
    generate selection queries statements.
    """
    def __init__(self):
        self.intent = None
        self.what = None
        self.where = None
        self.property = None    
        self.regexes = [
                POIsInMajorDestination(),
                HotelsInPlace(),
                POIsInState(),
            ]
        self.done = False

    def apply(self, sentence):
        for regex in self.regexes:
            print "Applying: ", regex
            regex.interpret(self, sentence)
            if self.done:
                print "Done with: ", regex
                break

    def __repr__(self):
        string = """
<Selector
    intent:{0}
    what:{1}
    where:{2}
    property:{3}
>
        """
        return string.format(self.intent,self.what,self.where,self.property)

    def __str__(self):
        return repr(self)

class HotelsInPlace(Regex):
    def __init__(self):
        regex = Question(Token('list') | Token('find')) + Lemma('hotel') + Pos('IN') + \
            Group(Entity('district')|Entity('state'),'Place')
        super(HotelsInPlace, self).__init__(regex)

    def interpret(self, ir, sentence):
        match = refo.search(self.regex,sentence)
        if match:
            ir.done = True
            ir.intent = "to list"
            ir.what = "hotels"
            ir.where = get_entity(match,sentence,"Place")

class POIsInMajorDestination(Regex):
    def __init__(self):
        regex = Question(Token('list') | Token('find')) + (Lemma('place') \
             | (Question(Lemma('tour')) + Lemma('site')) ) + Pos('IN') + \
            Group(Entity('district'),'MajorDestination')
        super(POIsInMajorDestination, self).__init__(regex)

    def interpret(self, ir, sentence):
        match = refo.search(self.regex,sentence)
        if match:
            ir.done = True
            ir.intent = "to list"
            ir.what = "points of interest in major destination"
            ir.where = get_entity(match,sentence,'MajorDestination')

class POIsInState(Regex):
    def __init__(self):
        regex = Question(Token('list') | Token('find')) + (Lemma('place') \
             | (Question(Lemma('tour')) + Lemma('site')) ) + Pos('IN') + \
            Group(Entity('state'),'State')
        super(POIsInState, self).__init__(regex)

    def interpret(self, ir, sentence):
        match = refo.search(self.regex,sentence)
        if match:
            ir.done = True
            ir.intent = "to list"
            ir.what = "points of interest in state"
            ir.where = get_entity(match,sentence,'State')

def get_entity(match, sentence, name):
    i, j = match.span(name)
    entity = sentence[i:j][0]
    return entity.token.capitalize()





queries2 = ['list tourist sites in Bidar']

queries = ["Hotels at Bangalore",
"List hotels in Bangalore",
"Mysore",
"Find tourist sites at Karnataka",
"list sites is Mysore",]
    
def  main():
    pass

if __name__ == '__main__':
    main()