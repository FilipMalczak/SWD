from config import AND, NOT, OR

class Translator:

    def __init__(self, model):
        self.model = model

    def to_natural(self, fact):
        fact = fact.replace('(', '').replace(')','')
        out = []
        for symbol in fact.split(' '):
            out.append(self._to_natural(symbol))
        return ' '.join(out).capitalize()


    def _to_natural(self, symbol):
        negated = NOT['symbol'] in symbol
        if negated:
            symbol = symbol.replace(NOT['symbol'], "")
        out = None
        for a in self.model.formulas:
            if a['symbol'].strip() == symbol:
                out = a['eng']
                break
        if not out:
            for s in [AND, OR]:
                if s['symbol'].strip() == symbol:
                    out = s['eng']
                    break
        if negated:
            out = NOT['eng'], out
        return out
