from Utils.iterator import DocIterator


class Verify:

    @staticmethod
    def verify_channel(channel_id):
        response = False
        for loop in DocIterator("./Docs/DocsDiscord/Whitelists/channel_whitelist.txt", str(channel_id)):
            if loop:  # Se retornar True (id presente no doc)
                response = True
                break
        return response

    @staticmethod
    def verify_user(channel_id):
        response = False
        for loop in DocIterator("./Docs/DocsDiscord/Whitelists/user_id_whitelist.txt", str(channel_id)):  # Percorre os Id's
            if loop:  # Se retornar True (id presente no doc)
                response = True
                break
        return response
