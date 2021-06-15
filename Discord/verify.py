from Utils.iterator import DocIterator


class Verify:
    """
    PT-BR: Classe criada para verificar os id's de canal e usuário, usando a classe "DocIterator" para evitar o problema
    de MemoryError, a classe só possui métodos estáticos pois na hora da criação da mesma, a sintaxe para chamada
    ficou mais flexível, porém pode ser mudado em breve.
    Para maiores detalhes sobre a classe  DocIterator, acesse o arquivo Iterator.py

    EN-US: Class created to check channel and user id's, using "DocIterator" class to avoid MemoryError,
    the class only has static methods because when it was created, the syntax for calling
    has become more flexible, but may be changed soon.
    For more details about the DocIterator class, access the Iterator.py file
    """

    @staticmethod
    def verify_channel(channel_id):
        response = False
        for loop in DocIterator("./Docs/DocsDiscord/Whitelists/channel_whitelist.txt", str(channel_id)):
            if loop:  # Se retornar True (id presente no doc)
                response = True
                break
        return response

    @staticmethod
    def verify_user(user_id):
        response = False
        for loop in DocIterator("./Docs/DocsDiscord/Whitelists/user_id_whitelist.txt", str(user_id)):
            if loop:  # Se retornar True (id presente no doc)
                response = True
                break
        return response
