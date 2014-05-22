import yaml
from expression_parser import parse

class Task:
    def __init__(self, type, fact):
        self.type = type
        self.fact = fact


def read_tasks(path, model):
    with open(path, 'r') as f:
        tasks = yaml.load(f)
    return parse_tasks(tasks, model)

def parse_tasks(_tasks, model):
    tasks = []
    for type in ['analysis', 'synthesis']:
        if _tasks[type]:
            for task in _tasks[type]:
                tasks.append(Task(type, parse(task, model)))

    return tasks

if __name__ == '__main__':
    tasks = read_tasks("example_input.yml")
    for task in tasks:
        print(task.type)
        print(task.fact)