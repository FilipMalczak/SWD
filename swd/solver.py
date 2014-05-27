from swd.csv_printer import CSVPrinter
from itertools import product

class Solver:

    def __init__(self, model):
        self.model = model

    def solve(self, task):
        s1 = set()
        s2 = set()
        boolean = [True, False]

        with CSVPrinter(self.model) as printer:
            for alphas in product( * ( [ boolean ] * (len(self.model.formulas))) ):
                row = list(alphas)
                row += [ fact(*alphas) for fact in self.model.facts ]
                row.append(task.fact(*alphas))
                row.append(self.model.f(*alphas))
                row.append(task.fact(*alphas) and self.model.f(*alphas))
                row.append((not task.fact(*alphas)) and self.model.f(*alphas))
                printer.write(row)
                if row[-2]:
                    s1.add(self.input_value(*alphas))
                if row[-1]:
                    s2.add(self.input_value(*alphas))
        sout = s1.difference(s2)
        return s1, s2, sout

    def input_value(self, *a):
            return a[:len(self.model.input)]
