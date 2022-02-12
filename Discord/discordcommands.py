from Discord.verify import *
from Utils.iterator import LineRemove

channel_whitelist = "./Docs/DocsDiscord/Whitelists/channel_whitelist.txt"
user_whitelist = "./Docs/DocsDiscord/Whitelists/user_id_whitelist.txt"


def add_channel_to_whitelist(channel_id):
    """
    PT-BR: Confere se o canal está listado, caso não esteja, abre o arquivo como modo "a" e adicona o canal
    e uma quebra de linha.

    EN-US: Check if the channel is listed, if not, open the file as "a" mode and add the channel
    and a line break.
    """
    channel_whitelisted = verify_channel(channel_id)
    if not channel_whitelisted:
        with open(channel_whitelist, "a") as whitelist_doc:
            whitelist_doc.write(str(channel_id) + "\n")
        return "Canal adicionado com sucesso"
    else:
        return "Canal já presente na whitelist"


def remove_channel_from_whitelist(channel_id):
    """
    PT-BR: Confere se o canal está listado, caso esteja, utiliza a classe LineRemove (criada para evitar problemas
    de MemoryError) para excluir somente o canal desejado, maiores detalhes sobre a classe no arquivo iterator.py

    EN-US: Check if the channel is listed, if it is, use the LineRemove class(created to avoid MemoryError problems)
    to remove only the desired channel, more details about the class in the iterator.py file
    """
    channel_whitelisted = verify_channel(channel_id)
    if channel_whitelisted:
        with open(channel_whitelist, "w") as whitelist_doc:
            for channel in LineRemove(channel_whitelist, channel_id):
                if channel:
                    whitelist_doc.write(channel)
        whitelist_doc.close()
        return "Canal removido com sucesso"
    else:
        return "Canal não presente na Whitelist"
