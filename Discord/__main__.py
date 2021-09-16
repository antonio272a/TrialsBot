import discord
from Discord.verify import Verify
from ApiPaladinsSmite.__main__ import Paladins, Smite
from Discord.discordcommands import AdminCommands, DiscordCommands


class Comand:

    """
    PT-BR: Esse arquivo recebe todas as mensagens (objeto discord.message) e trata eles chamando as classes
    dos outros arquivos.
    Essa classe sempre retorna uma string, independente do comando usado, essa string é conferida no arquivo
    principal (trialsbot.py).
    Obs.: Não colocar o método __str__() para retornar diretamente o método _main(), gera conflito na
    conferência dos Id's.

    EN-US: This file receives all the messages (discord.message object) and handles them by calling the classes
    of the other files.
    This class always returns a string, regardless of the command used, this string is checked in the file.
    main (trialsbot.py).
    Note: Do not put the __str__() method to directly return the _main() method, it generates a conflict in the
    Id's conference
    """

    def __init__(self, message):
        self.message_content = message.content
        self.channel_id = message.channel.id
        self.user_id = message.author.id
        self.user_has_acess = Verify.verify_user(self.user_id)
        self.channel_permited = Verify.verify_channel(self.channel_id)
        self.admin_commands = {".addthischannel", ".removethischannel", ".addchannelid", ".removechannelid"}
        self.discord_commands = {".help"}
        self.games = {"smite": Smite(), "paladins": Paladins()}
        self.api_commands = {".id", ".playerid", ".stats", ".replay", ".image", ".teste"}
        self.retorno = self._main()

    def __str__(self):
        return self.retorno

    def _main(self):
        """
        PT-BR: Sequência de if's/elif's é para a conferência de qual tipo de comando
        foi recebido, usando o split para pegar a string do comando.
        Podendo assim usar a verificação adequada.
        Obs.: Essas classes não levantam erros dentro do bot, somente retornam a string do erro, pois
        o mesmo é enviado de volta para o usuário, e não e necessidade de levantar erro, já que ao retornar
        a string, o processo já é parado.

        EN-US: If's/elif's sequence is for checking which type of command was received,
        using split to get the command string. Thus being able to use the proper verification.
        Note: These classes do not raise errors inside the bot, they only return the error string, because
        it is sent back to the user, and there is no need to raise an error, since when returning
        the string, the process stops.
        """
        if self.message_content.split()[0] in self.admin_commands:
            if self.user_has_acess:
                for admin_command in self.admin_commands:
                    if self.message_content.find(admin_command) != -1:
                        self.command = admin_command
                return self._execute_admin_command()
            else:
                return "Erro: Usuário sem permissão"
        elif self.message_content.split()[0] in self.discord_commands:
            return self._execute_discord_command()
        elif (self.message_content.split("-")[0] or self.message_content.split()[0]) in self.api_commands:
            if self.channel_permited:
                if not self._get_command():
                    """
                    PT-BR: Por padrão, o método _get_command() não retorna nada, porém se retornar,
                    vai ser um erro achaddo na execução
                    
                    EN-US: By default, the _get_command() method does not return anything, however if it does,
                    it will be an error found in the execution
                    """
                    return self._execute_api_command()
                else:
                    return self.error_message
            else:
                return "Erro: canal fora da Whitelist"

    def _get_command(self):
        """
        PT-BR: Método criado para verificar se o comando possui a identificação do jogo e para definir qual comando
        será usado.

        EN-US: Method created to check if the command has the game ID and to define which command will be used.
        """
        for game_key in self.games:  # Percorre a lista de jogos instanciados acima
            if self.message_content.find(game_key) != -1:  # Se achar o jogo dentro da mensagem
                self.game = self.games[game_key]  # requisição do jogo guardada dentro da variável game
                break
            else:
                self.game = "Error"  # Se não achar o jogo no comando, a variável fica com Str Error
                self.error_message = "Erro: " \
                                     "Comando incorreto, o comando sempre deve ser acompanhado pelo jogo, detalhes em .help"
        for command in self.api_commands:  # Percorre a lista de comandos
            if self.message_content.find(command) != -1:  # Se achar o comando dentro da mensagem
                if command == ".image":
                    self._set_teams()  # define os times para colagem
                self.command = command
                break
        if self.game == "Error":  # Se o jogo não for encontrado na mensagem, ele retorna um erro pro usuário
            return True

    def _set_teams(self):
        """
        PT-BR: Método usado somente para o comando ".image" para definir os times para a criação da imagem

        EN-US: Method used only for ".image" command to set the teams for the image creation
        """
        try:  # Tenta extrair os times da mensagem
            self.winner_team = self.message_content.split()[2]
            self.loser_team = self.message_content.split()[3]
        except:  # Caso não consiga, define os padrões
            self.winner_team = "WIN"
            self.loser_team = "LOS"

    def _execute_admin_command(self):
        """
        PT-BR: Os comandos que possuem o "try" são os que dependem de um input do usuário, por isso, caso
        o usuário coloque alguma informação errada, o bot pode retornar um aviso.

        EN-US: The commands that have the "try" are those that depend on user input, so if
        the user enters some wrong information, the bot may return a warning.
        """
        if self.command == ".addthischannel":
            return AdminCommands(self.user_id, self.channel_id).add_channel_to_whitelist()
        elif self.command == ".removethischannel":
            return AdminCommands(self.user_id, self.channel_id).remove_channel_from_whitelis()
        elif self.command == ".addchannelid":
            try:
                channel_id = self.message_content.split()[1]
                return AdminCommands(self.user_id, channel_id).add_channel_to_whitelist()
            except:
                return "Algum erro ocorreu, favor conferir a formatação da mensagem"
        elif self.command == ".removechannelid":
            try:
                channel_id = self.message_content.split()[1]
                return AdminCommands(self.user_id, channel_id).remove_channel_from_whitelis()
            except:
                return "Algum erro ocorreu, favor conferir a formatação da mensagem"

    def _execute_discord_command(self):
        if self.message_content.split()[0] == ".help":
            return DiscordCommands().help_command()

    def _execute_api_command(self):
        """
        PT-BR: Para maiores detalhes dos comandos abaixo, acesse o arquivo ./ApiPaladinsSmite/__main__.py
        EN-US: For more details on the commands below, access the file ./ApiPaladinsSmite/__main__.py
        """
        if self.command == ".image":
            self._set_teams()
            return self.game.get_image(self.message_content.split()[1], self.winner_team, self.loser_team)
        elif self.command == ".id":
            return self.game.get_player_id_by_match(self.message_content.split()[1])
        elif self.command == ".playerid":
            retorno = self.game.get_player_id_by_name(self.message_content[self.message_content.find(" "):])
            print(retorno)
            return retorno
        elif self.command == ".replay":
            return self.game.get_replay_status(self.message_content.split()[1])
        elif self.command == ".stats":
            return self.game.get_stats_file(self.message_content.split()[1])

    """
    PT-BR: Os métodos estáticos abaixo são para envio de arquivos (.png ou .txt) no discord, estão aqui só 
    para deixar a sintaxe do arquivo principal mais simples.
    Obs.: Eles só podem ser chamados de dentro de uma função assíncrona, ou seja, não pode ser chamada pela
    própria classe, por isso o próprio arquivo principal chama esses métodos
    
    EN-US: The static methods below are for sending files (.png or .txt) to discord, they are here only
    to make the main file syntax simpler.
    Note: They can only be called from within an asynchronous function, that is, they cannot be called by the
    class itself, so the main file itself calls these methods.
    """
    @staticmethod
    async def send_image(message, imagem):
        with open("./Images/Createdimages/" + imagem + ".png", 'rb') as file:  # Envia arquivo no discord
            await message.channel.send(file=discord.File(file, "Image.png"))

    @staticmethod
    async def send_file(message, filename):
        with open("./Docs/Docs" + filename.capitalize() + "/stats-" + filename + ".txt", 'r') as file:  # Envia arquivo no discord
            await message.channel.send(file=discord.File(file, "stats " + filename + ".txt"))
