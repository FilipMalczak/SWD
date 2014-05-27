import yaml
from swd.config import AND, OR, NOT
from swd.expression_parser import parse

class Task:
    def __init__(self, fact):
        self.fact = fact

def translate_english_to_symbol(sentence, model):
    s = sentence.lower()
    for formula in model.formulas:
        eng_version = formula["eng"].lower()
        symbol_version = formula["symbol"]
        s = s.replace(eng_version, symbol_version)
    for sign in [AND, OR, NOT]:
        eng_version = sign["eng"].lower()
        symbol_version = sign["symbol"]
        s = s.replace(eng_version, symbol_version)
    s = s.split(" ")
    while "" in s:
        s.remove("")
    s = " ".join(s)
    return s


def read_task(path, model):
    with open(path, 'r') as f:
        task = yaml.load(f)
    representation = task["representation"]
    txt = task['task']
    assert representation in ["eng", "symbol"]
    if representation == "eng":
        txt = translate_english_to_symbol(txt, model)
    return Task(parse(txt, model))


if __name__ == '__main__':
    from swd.model_reader import read_model
    model = read_model()
    txt = "Version alpha is finished and not (Version beta is finished)"
    print(translate_english_to_symbol(txt, model))