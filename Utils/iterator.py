class DocIterator:
    """
    PT-BR: Classe usada para evitar MemoryError ao conferir os Id's dos canais/usuários.

    EN-US: Class used to avoid MemoryError when checking channel/user id's.

    Reference: https://stackoverflow.com/questions/19151/build-a-basic-python-iterator
    """
    def __init__(self, arquivo, item):
        self.arquivo = open(arquivo, "r")
        self.item = str(item)
        self.linha_atual = ""

    def __iter__(self):
        return self

    def __next__(self):
        self.linha_atual = self.arquivo.readline()
        while self.linha_atual and not self.linha_atual.startswith(self.item):
            self.linha_atual = self.arquivo.readline()
        if self.linha_atual:
            return True
        raise StopIteration


class LineRemove:
    """
    PT-BR: Classe usada para evitar MemoryError ao excluir uma linha específica de um documento sem saber sua posição

    EN-US: Class used to avoid MemoryError when deleting a specific line from a document without knowing its position

    Reference: https://stackoverflow.com/questions/19151/build-a-basic-python-iterator
    """
    def __init__(self, arquivo, item):
        self.arquivo = open(arquivo, "r")
        self.item = str(item)
        self.linha_atual = ""

    def __iter__(self):
        return self

    def __next__(self):
        self.linha_atual = self.arquivo.readline()
        while self.linha_atual:
            self.linha_atual = self.arquivo.readline()
            if self.linha_atual.startswith(self.item):
                return False
            else:
                return self.linha_atual
        raise StopIteration
