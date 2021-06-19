from discord.ext import commands


class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__()

        self.no_category = "Без категории"
        self.dm_help = None
        self.dm_help_threshold = 250

    def add_bot_commands_formatting(self, bot_commands, heading):
        if bot_commands:
            joined = '\u0060\u002C\u2002\u0060'.join(c.name for c in bot_commands)
            self.paginator.add_line('__**%s**__:' % heading)
            self.paginator.add_line('\u0060{0}\u0060'.format(joined))
            self.paginator.add_line('')

    def get_opening_note(self):
        return "Используйте `{0}{1} [command]` для получения информации о команде .\n" \
               "Вы также можете использовать `{0}{1} [category]` для получения информации о категории." \
            .format(self.clean_prefix, self.invoked_with)

    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)
