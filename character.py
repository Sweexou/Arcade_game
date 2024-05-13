class Character:

    def __init__(self, username, grade, hp_max=100, ms=20, dmg=0, nb_bullets=0, cd_reload=10, regen=10, cd_dash=10, lives=3):

        self.username = username
        self.grade = grade
        self.hp_max = hp_max
        self.hp = hp_max
        self.ms = ms
        self.dmg = dmg
        self.nb_bullets = nb_bullets
        self.cd_reload = cd_reload
        self.regen = regen
        self.cd_dash = cd_dash
        self.lives = lives
