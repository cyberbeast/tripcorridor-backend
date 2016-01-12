from refo import Predicate, match, Group, finditer, Question, search
from tagging import Word, Tagger


class Token(Predicate):
    "Object to check for the token of the Word Object in refo regex"
    def __init__(self,tag):
        self.tag = tag
        super(Token,self).__init__(self.match)

    def match(self,word):
        return self.tag == word.token

class Entity(Token):
    "Object to check for the Named Entity in refo regex"
    def match(self, word):
        return self.tag in word.entities

class Lemma(Token):
    "Object to check the lemma of the word in refo regex"
    def match(self, word):
        return self.tag == word.lemma

class Pos(Token):
    "Object to check the Parts of Speech tag of a word"
    def match(self, word):
        return self.tag == word.pos

class Particle(Group):
    "Object to encapsulate the named refo.Group"
    def __init__(self, regex, name):
        super(Particle,self).__init__(regex,name)

class Number(Particle):
    "Object to particulate a number"
    def __init__(self,name):
        regex = Pos('CD') + Question(Pos('.') + Pos('CD'))
        super(Number, self).__init__(regex, name)

class Palindrome(Particle):
    "Object to match ((A+B) | (B+A))"
    def __init__(self,A,B,name = "palindrome"):
        regex = (A + B) | (B + A)
        super(Palindrome, self).__init__(regex, name)

class Date(Particle):
    "Object to model the date"
    def __init__(self,name):
        regex = (Entity('season') + Question(Entity('year'))) \
        | (Entity('month') + Entity('year')) \
        | (Question(Entity('month')) + Entity('year')) \
        | (Entity('month') + Question(Entity('year')))
        super(Date, self).__init__(regex, name)

class Run(Particle):
    "Not to be used anywhere. just for the test"
    def __init__(self,name):
        regex = Lemma('run')
        super(Run, self).__init__(regex,name)


def main():
    word = Word(token="running", lemma="run", pos="VBG",entities=["runningEntity"])
    token = Pos("VBG")
    print [x.span() for x in finditer(Run('A'),[word,Word(token="Japan",pos="NN"),word,word])]
    tagger = Tagger()
    words = tagger.tag("Who 500.92 dollar running behind Bangalore \
        Bengaluru the cars in the night at 2014?")
    print [x.span() for x in finditer(Number("A"),words)]
    print search(Number("A"),words).span("A")

if __name__ == '__main__':
    main()
