from character import Character

class CharacterManager:
    def __init__(self):
        self.characters = []

    def create_character(self, grade, hp_max=100, ms=5, dmg=25, cd_reload=0.25, cd_dash=5):
        new_character = Character(grade, hp_max, ms, dmg, cd_reload, cd_dash)
        self.characters.append(new_character)
        return new_character

    def get_character(self, index):
        if 0 <= index < len(self.characters):
            return self.characters[index]
        else:
            return None

    def get_all_characters(self):
        return self.characters

    def update_character(self, index, grade=None, hp_max=None, ms=None, dmg=None, cd_reload=None, cd_dash=None):
        if 0 <= index < len(self.characters):
            character = self.characters[index]
            if grade is not None:
                character.grade = grade
            if hp_max is not None:
                character.hp_max = hp_max
                character.hp = hp_max
            if ms is not None:
                character.ms = ms
            if dmg is not None:
                character.dmg = dmg
            if cd_reload is not None:
                character.cd_shoot = cd_reload
            if cd_dash is not None:
                character.cd_dash = cd_dash
            return character
        else:
            return None

    def delete_character(self, index):
        if 0 <= index < len(self.characters):
            return self.characters.pop(index)
        else:
            return None