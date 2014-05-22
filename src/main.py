from model_reader import read_model
from task_reader import read_tasks
from solver import Solver
from config import NOT, AND, OR

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
    model = read_model()
    tasks = read_tasks(TASK_PATH, model)
    solver = Solver(model)
    for task in tasks:
        s1, s2, s = solver.solve(task)

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


