#!/usr/bin/python

from swd.decorators import cached
from swd.config import NOT

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


# http://stackoverflow.com/questions/16405892/is-there-an-implication-logical-operator-in-python
# http://jacob.jkrall.net/lost-operator/
operators=[
    #(Infix(lambda p,q: False),                  "F"),
    #(Infix(lambda p,q: True),                   "T"),
    (Infix(cached(lambda p,q: p and q)),                                  "^"),
    (Infix(cached(lambda p,q: p or q))           ,                        "V"),
    #(Infix(cached(lambda p,q: p != q))           ,                        "^"),
    (Infix(cached(lambda p,q: ((not p) or not q))),                     "nad"),
    (Infix(cached(lambda p,q: ((not p) and not q))),                    "nor"),
    (Infix(cached(lambda p,q: ((not p) or q))),                          "=>"),
    (Infix(cached(lambda p,q: ((not p) and (not q)) or (p and q))),     "<=>")
    ]
    
ops = {sym: op for op,sym in operators}

ignored = ['not', '(', ')']

def get_token_stream(expression):
    # make sure that parentheses and negation is separated with space from other tokens, and not is understood by python
    expression = expression.replace(NOT["symbol"], 'not ').replace("(", " ( ").replace(")", " ) ")
    exsplit = expression.split(" ")
    #remove empty token candidates
    while "" in exsplit:
        exsplit.remove("")
    # enforce negation priority with parentheses
    idx = 0
    while idx<len(exsplit):
        token = exsplit[idx]
        if token == "not":
            insert_point = idx+2
            if exsplit[idx+1] == "(":
                counter = 1
                while counter:
                    if exsplit[insert_point] == "(":
                        counter += 1
                    elif exsplit[insert_point] == ")":
                        counter -= 1
                    insert_point += 1
            exsplit = exsplit[:idx] + [ "(" ] + exsplit[idx:insert_point] + [")"] + exsplit[insert_point:]
            idx += 1
        idx += 1
    return exsplit

def parse(expression, model):
    '''
    Creates a function from a logical expression.
    In the expression you have to separate every token by a space and
    specify calculation orders by using braces ()
    Available operators:
    ^ - and
    V - or
    => - implication
    <=> - if and only if
    nor - nor
    nad - nand
    not - not
    Example inputs:
    ( a1 ^ a2 ) => a3
    ( not a1 ) V a2
    ( a1 ^ a2 ) => ( ( not a1 ) V a2 )
    @expression: String containing a logical expression created according to
                mentioned rules
    @returns: function with as many arguments, as there were variables in the
                expression sorted alphabetically
    '''
    exsplit = get_token_stream(expression)
    for index, symbol in enumerate(exsplit):
        if symbol not in ignored and symbol in ops:
            exsplit[index] = "| ops['" + symbol + "'] |"
    output = "lambda " + ",".join(model.symbols) + ": " + " ".join(exsplit)
    foo = eval(output)
    return cached(foo)


if __name__ == '__main__':

    #ex = "a1 <=> a2"
    #foo = parse(ex)
    #print(foo(True, True))
    #
    #ex = "a1 <=> a2"
    #foo = parse(ex)
    #print(foo(False, True))
    #
    #ex = "a1 <=> a2"
    #foo = parse(ex)
    #print(foo(False, False))
    get_token_stream("a ^ ~ b")
    get_token_stream("~ a ^ b")
    get_token_stream("~(a ^ b) v c ^ (~ d v e) ")
    get_token_stream("~(a ^ b) v c ^ (~(a ^(b v c)) d v e) ")