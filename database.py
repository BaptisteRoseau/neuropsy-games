import sqlite3
import logging
import json

from models import Game, CognitiveCategory, CognitiveFunction, Material

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, file: str = "DO_NOT_REMOVE.db"):
        self.con = sqlite3.connect(file)

    def setup(self):
        logger.info("Setting up database")
        with open("database.sql", "r") as f:
            schema = f.read()
            self.con.executescript(schema)
        self.con.commit()

    def add_game(self, game: Game):
        logger.info("Adding game " + game.title)
        self.con.execute(
            """
            INSERT INTO games (
                title, description, cognitive_functions,
                cognitive_categories, materials, image)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                game.title,
                game.description,
                json.dumps(
                    [(func.name, weight) for func, weight in game.functions]
                ),  # Serialize functions
                json.dumps(
                    [(cat.name, weight) for cat, weight in game.categories]
                ),  # Serialize categories
                json.dumps(
                    [material.name for material in game.materials]
                ),  # Serialize materials
                game.image,
            ),
        )
        self.con.commit()

    def update_game(self, game: Game):
        if game.id is None or game.id < 0:
            raise ValueError("Game ID must be a positive number")
        logger.info("Updating game " + game.title)
        self.con.execute(
            """
            UPDATE games
            SET title = ?, description = ?, cognitive_functions = ?, 
                cognitive_categories = ?, materials = ?, image = ?
            WHERE id = ?
            """,
            (
                game.title,
                game.description,
                json.dumps([(func.name, weight) for func, weight in game.functions]),
                json.dumps([(cat.name, weight) for cat, weight in game.categories]),
                json.dumps([material.name for material in game.materials]),
                game.image,
                game.id,
            ),
        )
        self.con.commit()

    def delete_game(self, game_id: int):
        if game_id is None or game_id < 0:
            raise ValueError("Game ID must be a positive number")
        logger.info("Deleting game with id " + str(game_id))
        self.con.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self.con.commit()

    def add_cognitive_category(self, category: CognitiveCategory):
        logger.info("Adding cognitive category" + category.name)
        self.con.execute(
            """
            INSERT INTO cognitive_categories (name)
            VALUES (?)
            """,
            (category.name,),
        )
        self.con.commit()

    def update_cognitive_category(self, category: CognitiveCategory):
        if category.id is None or category.id < 0:
            raise ValueError("Cognitive Category ID must be a positive number")
        logger.info("Updating cognitive category " + category.name)
        self.con.execute(
            """
            UPDATE cognitive_categories
            SET name = ?
            WHERE id = ?
            """,
            (category.name, category.id),
        )
        self.con.commit()

    def delete_cognitive_category(self, category_id: int):
        if category_id is None or category_id < 0:
            raise ValueError("Cognitive Category ID must be a positive number")
        logger.info("Deleting cognitive category with id " + str(category_id))
        self.con.execute(
            "DELETE FROM cognitive_categories WHERE id = ?", (category_id,)
        )
        self.con.commit()

    def add_cognitive_function(self, function: CognitiveFunction):
        logger.info("Adding cognitive function" + function.name)
        self.con.execute(
            """
            INSERT INTO cognitive_functions (name)
            VALUES (?)
            """,
            (function.name,),
        )
        self.con.commit()

    def update_cognitive_function(self, function: CognitiveFunction):
        if function.id is None or function.id < 0:
            raise ValueError("Cognitive Function ID must be a positive number")
        logger.info("Updating cognitive function " + function.name)
        self.con.execute(
            """
            UPDATE cognitive_functions
            SET name = ?
            WHERE id = ?
            """,
            (function.name, function.id),
        )
        self.con.commit()

    def delete_cognitive_function(self, function_id: int):
        if function_id is None or function_id < 0:
            raise ValueError("Cognitive Function ID must be a positive number")
        logger.info("Deleting cognitive function with id " + str(function_id))
        self.con.execute("DELETE FROM cognitive_functions WHERE id = ?", (function_id,))
        self.con.commit()

    def get_game(self, game_id: int = None, game_title: str = None) -> list[Game]:
        logger.info("Getting game")
        if game_id:
            cursor = self.con.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        elif game_title:
            cursor = self.con.execute(
                "SELECT * FROM games WHERE title LIKE ?", (f"%{game_title}%",)
            )
        else:
            raise ValueError("Either game_id or game_title must be provided")

        rows = cursor.fetchall()
        games = []
        for row in rows:
            game = Game(
                id=row[0],
                title=row[1],
                description=row[2],
                materials=[
                    Material[material] for material in json.loads(row[5])
                ],  # Deserialize materials
                categories=[
                    (CognitiveCategory(id=None, name=cat[0]), cat[1])
                    for cat in json.loads(row[4])
                ],  # Deserialize categories
                functions=[
                    (CognitiveFunction(id=None, name=func[0]), func[1])
                    for func in json.loads(row[3])
                ],  # Deserialize functions
                image=row[6],
            )
            games.append(game)
        return games

    def get_cognitive_category(
        self, category_id: int = None, category_name: str = None
    ) -> list[CognitiveCategory]:
        logger.info("Getting cognitive category")
        if category_id:
            cursor = self.con.execute(
                "SELECT * FROM cognitive_categories WHERE id = ?", (category_id,)
            )
        elif category_name:
            cursor = self.con.execute(
                "SELECT * FROM cognitive_categories WHERE name LIKE ?",
                (f"%{category_name}%",),
            )
        else:
            raise ValueError("Either category_id or category_name must be provided")

        rows = cursor.fetchall()
        categories = []
        for row in rows:
            category = CognitiveCategory(id=row[0], name=row[1])
            categories.append(category)
        return categories

    def get_cognitive_function(
        self, function_id: int = None, function_name: str = None
    ) -> list[CognitiveFunction]:
        logger.info("Getting cognitive function")
        if function_id:
            cursor = self.con.execute(
                "SELECT * FROM cognitive_functions WHERE id = ?", (function_id,)
            )
        elif function_name:
            cursor = self.con.execute(
                "SELECT * FROM cognitive_functions WHERE name LIKE ?",
                (f"%{function_name}%",),
            )
        else:
            raise ValueError("Either function_id or function_name must be provided")

        rows = cursor.fetchall()
        functions = []
        for row in rows:
            function = CognitiveFunction(id=row[0], name=row[1])
            functions.append(function)
        return functions

    def get_all_games(self) -> list[Game]:
        logger.info("Getting all games")
        cursor = self.con.execute("SELECT * FROM games")
        rows = cursor.fetchall()
        games = []
        for row in rows:
            game = Game(
                id=row[0],
                title=row[1],
                description=row[2],
                image=row[6],
                categories=[],
                functions=[],
            )
            games.append(game)
        return games

    def get_all_cognitive_categories(self) -> list[CognitiveCategory]:
        logger.info("Getting all cognitive categories")
        cursor = self.con.execute("SELECT * FROM cognitive_categories")
        rows = cursor.fetchall()
        categories = []
        for row in rows:
            category = CognitiveCategory(id=row[0], name=row[1])
            categories.append(category)
        return categories

    def get_all_cognitive_functions(self) -> list[CognitiveFunction]:
        logger.info("Getting all cognitive functions")
        cursor = self.con.execute("SELECT * FROM cognitive_functions")
        rows = cursor.fetchall()
        functions = []
        for row in rows:
            function = CognitiveFunction(id=row[0], name=row[1])
            functions.append(function)
        return functions
