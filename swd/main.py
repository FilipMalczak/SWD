"""
Python MLA

Usage:
  run_swd.py [<task_file>] [-v]
  run_swd.py -h | --help

Options:
  -h --help     Show this screen.
  -v --verbose  Print more information on screen
"""
import os

from docopt import docopt

from swd.model_reader import read_model
from swd.task_reader import read_task
from swd.solver import Solver
from swd.config import NOT, AND, OR
from swd.translator import Translator
from swd.quine_mccluskey import QuineMcCluskey


def format_fact(final_set, model):
    return (OR['symbol']+"\n").join(
        "(" + \
            AND['symbol'].join(
                (
                    ( "" if alpha else (NOT['symbol']) ) + \
                    #("au%s" % i )
                    (model.input[i]['symbol'])
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
                foo.append(NOT['symbol'] + model.input[i]['symbol'])
            elif alpha == '1':
                foo.append(model.input[i]['symbol'])
        result.append('(' + AND['symbol'].join(foo) + ')')
    return (OR['symbol']+"\n").join(result)

def print_sets(s1, s2, s):
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




def main(args):
    old_cwd = os.getcwd()
    new_cwd = os.path.dirname(__file__)
    os.chdir(new_cwd)
    arguments = docopt(__doc__, args[1:])
    TASK_PATH = arguments['<task_file>']
    if not TASK_PATH:
        TASK_PATH = "./data/example_eng_input.yml"
    model = read_model()
    task = read_task(TASK_PATH, model)
    solver = Solver(model)
    s1, s2, s = solver.solve(task)

    if arguments['--verbose']:
        print_sets(s1, s2, s)

    print("Fu")
    print(format_fact(sorted(list(s)), model))

    print("="*40)
    qm = QuineMcCluskey()
    ones = []
    for _s in s:
        ones.append(''.join(['1' if b else '0' for b in _s]))
    ones_decimal = [int(b, 2) for b in ones]
    simplified = qm.simplify(ones_decimal)
    print("Simplified Fu")
    if arguments['--verbose']:
        print(simplified)
    formatted = format_simplified_fact(simplified, model)
    print(formatted)
    translator = Translator(model)
    translated = translator.to_natural(formatted)
    print(translated)
    os.chdir(old_cwd)



