from config import AND, NOT, ONEZERO, CSV_PATH

class CSVPrinter:


    def __init__(self, model):
        self.model = model
        self.file = None

    def __enter__(self):
        if not self.file:
            self.file = open(CSV_PATH, 'w')
            self.write_header()
        return self

    def __exit__(self, type, value, tb):
        self.file.close()
        self.file = None

    def write(self, row):
        print(";".join(ONEZERO[x] for x in row), file=self.file)

    def write_header(self):
        header = ";".join(
            self.model.formulas + \
            ["F%i" % i for i in range(len(self.model.facts))] + \
            [ "Fy", "F", "Fy"+AND+"F", NOT+"Fy"+AND+"F" ])
        print(header, file=self.file)



