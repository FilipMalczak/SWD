import yaml
from expression_parser import parse
from decorators import cached
from config import MODEL_PATH

class Model:
    @property
    def formulas(self):
        return self.input + self.internal + self.output

    @property
    def symbols(self):
        return[a['symbol'] for a in self.formulas]

    @cached
    def f(self, *a):
        return all(fact(*a) for fact in self.facts)


def read_model():
    with open(MODEL_PATH, 'r') as f:
        model = yaml.load(f)
    return parse_model(model)

def parse_model(_model):
    model = Model()
    for attr in ['input', 'internal', 'output']:
        setattr(model, attr, _model[attr] if _model[attr] else [])

    model.facts = []
    formulas = model.formulas
    for fact in _model['facts']:
        model.facts.append(parse(fact, model))
    return model



if __name__ == '__main__':
    model = read_model("example_model.yml")
    print(model.formulas)