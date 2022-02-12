from Utils.iterator import DocIterator


def verify_channel(channel_id):
    response = False
    for loop in DocIterator("./Docs/DocsDiscord/Whitelists/channel_whitelist.txt", str(channel_id)):
        if loop:  # Se retornar True (id presente no doc)
            response = True
            break
    return response


def verify_user(user_id):
    response = False
    for loop in DocIterator("./Docs/DocsDiscord/Whitelists/user_id_whitelist.txt", str(user_id)):
        if loop:  # Se retornar True (id presente no doc)
            response = True
            break
    return response
