class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1


    def read_score(self):
        with open('score.txt', 'r') as f:
            self.high_score = int(f.read())

    def write_score(self):
        with open('score.txt', 'w') as f:
            f.write(str(self.high_score))

