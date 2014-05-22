import yaml
from expression_parser import parse

class Task:
    def __init__(self, fact):
        self.fact = fact


def read_task(path, model):
    with open(path, 'r') as f:
        task = yaml.load(f)
    return Task(parse(task['task'], model))


if __name__ == '__main__':
    tasks = read_task("example_input.yml")
    for task in tasks:
        print(task.fact)