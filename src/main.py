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

def format_fact(final_set):
    return (OR+"\n").join(
        "(" + \
            AND.join(
                (
                    ( "" if alpha else (NOT) ) + \
                    ("au%s" % i )
                )
                for i, alpha in enumerate(alphas)
            ) +\
        ")"
        for alphas in final_set
    )

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
    print(format_fact(sorted(list(s))))


