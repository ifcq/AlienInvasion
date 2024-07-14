from AlienInvasion.setting import Settings
import json

class Stats:
    def __init__(self, ai_game):
        """Initialize your data structure here."""
        self.settings = Settings()
        self.reset_stats()
        """先搞一个积分统计，后面学会了JSON可以搞个存档"""
        self.score = 0
        self.high_score = self.load_highscore()
        self.level = 1


    def reset_stats(self):
        """在游戏进行中会变化的数值的统计"""
        self.ship_left = self.settings.ship_limit





    def save_highest_score(self, score, filename='highest_score.json'):
        try:
            with open(filename, 'r') as file:
                highest_score_data = json.load(file)
        except FileNotFoundError:
            highest_score_data = {"highest_score": 0}

        if score > highest_score_data["highest_score"]:
            highest_score_data["highest_score"] = score

        with open(filename, 'w') as file:
            json.dump(highest_score_data, file)





    def load_highscore(self,filename='highest_score.json'):
        try:
            with open(filename, 'r') as file:
                highscore_data = json.load(file)
                return highscore_data.get("highest_score", 0)
        except FileNotFoundError:
            return 0
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return 0


