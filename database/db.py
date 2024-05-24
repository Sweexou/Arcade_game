import sqlite3

DB_NAME = './database/ArcadeDB.db'
#DB_NAME = './ArcadeDB.db'

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_tables()
        

    def create_tables(self):
        # Create the tables if they don't exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS classe (
            id INTEGER PRIMARY KEY,
            grade TEXT,
            max_hp INTEGER,
            speed INTEGER,
            damage INTEGER,
            cd_shoot INTEGER,
            cd_dash INTEGER
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS score (
            id INTEGER PRIMARY KEY,
            id_player INTEGER REFERENCES player(id_player),
            score INTEGER,
            classe TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            id_player INTEGER PRIMARY KEY,
            username TEXT,
            Assassin INTEGER,
            Sniper INTEGER,
            Soldat INTEGER,
            Tank INTEGER
        )
        """)

        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def insert_classe(self, grade, max_hp, speed, damage, cd_shoot, cd_dash):
        query = """
        INSERT INTO classe (grade, max_hp, speed, damage, cd_shoot, cd_dash)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (grade, max_hp, speed, damage, cd_shoot, cd_dash))
        self.conn.commit()

    def insert_score(self, id_player, score, classe):
        query = """
        INSERT INTO score (id_player, score, classe)
        VALUES (?, ?, ?)
        """
        self.cursor.execute(query, (id_player, score, classe))
        self.conn.commit()

    def insert_player(self, username, Assassin=0, Sniper=0, Soldat=0, Tank=0):
        query = """
        INSERT INTO player (username, Assassin, Sniper, Soldat, Tank)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (username, Assassin, Sniper, Soldat, Tank))
        self.conn.commit()

    def update_classe(self, grade, max_hp, speed, damage, cd_shoot, cd_dash, id):
        query = """
        UPDATE classe
        SET grade=?, max_hp=?, speed=?, damage=?, cd_shoot=?, cd_dash=?
        WHERE id=?
        """
        self.cursor.execute(query, (grade, max_hp, speed, damage, cd_shoot, cd_dash, id))
        self.conn.commit()

    def update_score(self, id_player, score):
        query = """
        UPDATE score
        SET score=?
        WHERE id_player=?
        """
        self.cursor.execute(query, (score, id_player))
        self.conn.commit()

    def update_player(self, username, Assassin, Sniper, Soldat, Tank, id_player):
        query = """
        UPDATE player
        SET username=?, Assassin=?, Sniper=?, Soldat=?, Tank=?
        WHERE id_player=?
        """
        self.cursor.execute(query, (username, Assassin, Sniper, Soldat, Tank, id_player))
        self.conn.commit()

    def delete_classe(self, id):
        query = "DELETE FROM classe WHERE id=?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def delete_score_by_id_player(self, id_player):
        query = "DELETE FROM score WHERE id_player=?"
        self.cursor.execute(query, (id_player,))
        self.conn.commit()

    def delete_player(self, id_player):
        query = "DELETE FROM player WHERE id_player=?"
        self.cursor.execute(query, (id_player,))
        self.conn.commit()

    def get_classe(self, id):
        query = "SELECT * FROM classe WHERE id=?"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()
    
    def get_classe_by_name(self, id):
        query = "SELECT * FROM classe WHERE grade=?"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def get_score_by_id_player(self, id_player):
        query = "SELECT score FROM score WHERE id_player=?"
        self.cursor.execute(query, (id_player,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Return the first (and only) score value
        else:
            return None  # Return None if no score is found

    def get_player(self, id_player):
        query = "SELECT * FROM player WHERE id_player=?"
        self.cursor.execute(query, (id_player,))
        return self.cursor.fetchone()

    def get_top_players(self, limit=7):
        query = """
        SELECT p.username, s.classe, SUM(s.score) AS total_score
        FROM player p
        JOIN score s ON p.id_player = s.id_player
        GROUP BY p.id_player, s.classe
        ORDER BY total_score DESC
        LIMIT ?
        """
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()
    
    def get_id_player_by_username(self, username):
        self.cursor.execute("SELECT id_player FROM player WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if row:
            return row[0] 
        else:
            return None 
        
        
db = Database()
print(db.get_player(1))
db.close()
