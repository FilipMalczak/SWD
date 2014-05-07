import yaml
from expression_parser import parse

class Model:
    @property
    def formulas(self):
        return self.input + self.internal + self.output


def read_model(path):
    with open(path, 'r') as f:
        model = yaml.load(f)
    return parse_model(model)

def parse_model(_model):
    model = Model()
    for attr in ['input', 'internal', 'output']:
        setattr(model, attr, _model[attr])
    model.facts = []
    for fact in _model['facts']:
        model.facts.append(parse(fact))
    return model

if __name__ == '__main__':
    model = read_model("example_model.yml")
    print(model.formulas)