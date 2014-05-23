"""
Python MLA

Usage:
  main.py [<task_file>] [-v]
  main.py -h | --help

Options:
  -h --help     Show this screen.
  -v --verbose  Print more information on screen
"""

from model_reader import read_model
from task_reader import read_task
from solver import Solver
from config import NOT, AND, OR
from docopt import docopt

def format_fact(final_set, model):
    return (OR+"\n").join(
        "(" + \
            AND.join(
                (
                    ( "" if alpha else (NOT) ) + \
                    #("au%s" % i )
                    (model.input[i])
                )
                for i, alpha in enumerate(alphas)
            ) +\
        ")"
        for alphas in final_set
    )

def format_simplified_fact(simplified, model):
    result = []
    for alphas in simplified:
        foo = []
        for i, alpha in enumerate(alphas):
            if alpha == '0':
                foo.append(NOT + model.input[i])
            elif alpha == '1':
                foo.append(model.input[i])
        result.append('(' + AND.join(foo) + ')')
    return (OR+"\n").join(result)




TASK_PATH = 'example_input.yml'

if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['<task_file>']:
        TASK_PATH = arguments['<task_file>']

    model = read_model()
    task = read_task(TASK_PATH, model)
    solver = Solver(model)
    s1, s2, s = solver.solve(task)

    if arguments['--verbose']:
        print("S1")
        for _s in sorted(list(s1)):
            print(_s)
        print("="*40)

        print("S2")
        for _s in sorted(list(s2)):
            print(_s)
        print("="*40)

        print("S")
        for _s in sorted(list(s)):
            print(_s)
        print("="*40)

    print("Fu")
    print(format_fact(sorted(list(s)), model))

    print("="*40)

    #https://pypi.python.org/pypi/quine_mccluskey/0.2
    from quine_mccluskey.qm import QuineMcCluskey

    qm = QuineMcCluskey()
    ones = []
    for _s in s:
        ones.append(''.join(['1' if b else '0' for b in _s]))
    ones_decimal = [int(b, 2) for b in ones]
    simplified = qm.simplify(ones_decimal)
    print("Simplified Fu")
    print(simplified)
    print(format_simplified_fact(simplified, model))


