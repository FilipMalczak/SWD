#!/usr/bin/python

# From http://code.activestate.com/recipes/384122/ (via http://stackoverflow.com/questions/932328/python-defining-my-own-operators)
class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)


booleans = [False,True]

# http://stackoverflow.com/questions/16405892/is-there-an-implication-logical-operator-in-python
# http://jacob.jkrall.net/lost-operator/
operators=[
    #(Infix(lambda p,q: False),                  "F"),
    #(Infix(lambda p,q: True),                   "T"),
    (Infix(lambda p,q: p and q),                "&"),
    (Infix(lambda p,q: p or q)           ,      "V"),
    (Infix(lambda p,q: p != q)           ,      "^"),
    (Infix(lambda p,q: ((not p) or not q)),     "nad"),
    (Infix(lambda p,q: ((not p) and not q)),    "nor"),
    (Infix(lambda p,q: ((not p) or q)),         "=>"),
    ]
    
ops = {sym: op for op,sym in operators}

ignored = ['not', '(', ')']


def parse(expression):
    vars = set()
    exsplit = expression.split(" ")
    for index, symbol in enumerate(exsplit):
        if symbol not in ignored:
            if symbol not in ops:
                vars.add(symbol)
            else:
                exsplit[index] = "| ops['" + symbol + "'] |" 
    vars = sorted(list(vars))
    output = "lambda " + ",".join(vars) + ": " + " ".join(exsplit)
    return eval(output)


if __name__ == '__main__':

    ex = "( a1 & a2 ) => a3"
    foo = parse(ex)
    print(foo(True, True, False))

    ex = "( not a1 ) V a2"
    foo = parse(ex)
    print(foo(False, True))

    ex = "( a1 & a2 ) => ( not a1 V a2 )"
    foo = parse(ex)
    print(foo(False, False))