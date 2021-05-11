class DocIterator:
    def __init__(self, arquivo, item):
        self.arquivo = open(arquivo, "r")
        self.item = item
        self.linha_atual = ""
        self.response = False

    def __iter__(self):
        return self

    def __next__(self):
        self.linha_atual = self.arquivo.readline()
        while self.linha_atual and not self.linha_atual.startswith(str(self.item)):
            self.linha_atual = self.arquivo.readline()
        if self.linha_atual:
            self.response = True
            return self.response
        raise StopIteration

