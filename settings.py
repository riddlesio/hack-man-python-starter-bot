class Settings:
    def __init__(self, timebank=None, time_per_move=None, player_names=None, your_bot=None, your_botid=None,
                 field_width=None, field_height=None, max_rounds=None):
        self.timebank = timebank
        self.time_per_move = time_per_move
        self.player_names = player_names
        self.your_bot = your_bot
        self.your_botid = your_botid
        self.field_width = field_width
        self.field_height = field_height
        self.max_rounds = max_rounds

    def get_timebank(self):
        return self.timebank

    def get_time_per_move(self):
        return self.time_per_move

    def get_player_names(self):
        return self.player_names

    def get_your_bot(self):
        return self.your_bot

    def get_your_botid(self):
        return self.your_botid

    def get_field_width(self):
        return self.field_width

    def get_field_height(self):
        return self.field_height

    def get_max_rounds(self):
        return self.max_rounds

    def update(self, key, value):
        new_settings = self.__dict__.copy()
        new_settings.update({key: value})
        return Settings(**new_settings)
