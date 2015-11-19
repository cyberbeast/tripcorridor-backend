import refo # dummy import used in example class A

class Regex(object):
    "Virtual class to implement regex and extract information on match"
    def __init__(self, regex):
        self.regex = regex

    def interpret(self, ir, sentence):
        raise NotImplementedError("Regex *interpret* method has to be implemented")


class A(Regex):
    "An Example class that implements Regex"
    def __init__(self):
        regex = "" # need to construct using REfO syntax
        super(A, self).__init__(regex)

    def interpret(self, ir, sentence):
        match = refo.search(self.regex,sentence)
        if match:
            ir.done = True
            # build your selector or filter attributes 