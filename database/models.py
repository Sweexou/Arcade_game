# models.py

class Classe:
    def __init__(self, grade, max_hp, speed, damage, cd_shoot, cd_dash):
        self.grade = grade
        self.max_hp = max_hp
        self.speed = speed
        self.damage = damage
        self.cd_shoot = cd_shoot
        self.cd_dash = cd_dash

class Score:
    def __init__(self, id_player, score, classe):
        self.id_player = id_player
        self.score = score
        self.classe = classe

class Player:
    def __init__(self, username, Assassin, Sniper, Soldat, Tank):
        self.username = username
        self.Assassin = Assassin
        self.Sniper = Sniper
        self.Soldat = Soldat
        self.Tank = Tank
