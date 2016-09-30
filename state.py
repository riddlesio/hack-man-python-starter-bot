class State:
    def __init__(self, field=None, round=0, players=None):

        if players is None:
            players = {}

        self.field = field
        self.round = round
        self.players = players

    def get_field(self):
        return self.field

    def get_round(self):
        return self.round

    def get_players(self):
        return self.players

    def update(self, key, value):
        new_settings = self.__dict__.copy()
        new_settings.update({key: value})
        return State(**new_settings)
