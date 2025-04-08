import sqlite3
import logging
import json
from functools import wraps

from models import Game, CognitiveCategory, CognitiveFunction, Material

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Custom exception for database errors."""

    pass


class DuplicateError(DatabaseError):
    """The entry already exists and a unique constraint has been violated."""

    pass


class NotFoundError(DatabaseError):
    """The entry already exists and a unique constraint has been violated."""

    pass


def handle_sqlite_exceptions(func):
    """Decorator to handle sqlite3 exceptions and convert them to custom exceptions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            raise DuplicateError("A unique constraint was violated.") from e
        except sqlite3.Error as e:
            raise DatabaseError("An error occurred with the database.") from e

    return wrapper


class Database:
    def __init__(self, file: str = "DO_NOT_REMOVE.db"):
        self.con = sqlite3.connect(file)

    @handle_sqlite_exceptions
    def setup(self):
        logger.info("Setting up database")
        with open("database.sql", "r") as f:
            schema = f.read()
            self.con.executescript(schema)
        self.con.commit()

    @handle_sqlite_exceptions
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
                    [(func.id, weight) for func, weight in game.functions]
                ),  # Serialize function IDs
                json.dumps(
                    [(cat.id, weight) for cat, weight in game.categories]
                ),  # Serialize category IDs
                json.dumps(
                    [material.name for material in game.materials]
                ),  # Serialize materials
                game.image,
            ),
        )
        self.con.commit()

    @handle_sqlite_exceptions
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
                json.dumps([(func.id, weight) for func, weight in game.functions]),
                json.dumps([(cat.id, weight) for cat, weight in game.categories]),
                json.dumps([material.name for material in game.materials]),
                game.image,
                game.id,
            ),
        )
        self.con.commit()

    @handle_sqlite_exceptions
    def delete_game(self, game_id: int):
        if game_id is None or game_id < 0:
            raise ValueError("Game ID must be a positive number")
        logger.info("Deleting game with id " + str(game_id))
        self.con.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self.con.commit()

    @handle_sqlite_exceptions
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

    @handle_sqlite_exceptions
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

    @handle_sqlite_exceptions
    def delete_cognitive_category(self, category_id: int):
        if category_id is None or category_id < 0:
            raise ValueError("Cognitive Category ID must be a positive number")
        logger.info("Deleting cognitive category with id " + str(category_id))
        self.con.execute(
            "DELETE FROM cognitive_categories WHERE id = ?", (category_id,)
        )
        self.con.commit()

    @handle_sqlite_exceptions
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

    @handle_sqlite_exceptions
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

    @handle_sqlite_exceptions
    def delete_cognitive_function(self, function_id: int):
        if function_id is None or function_id < 0:
            raise ValueError("Cognitive Function ID must be a positive number")
        logger.info("Deleting cognitive function with id " + str(function_id))
        self.con.execute("DELETE FROM cognitive_functions WHERE id = ?", (function_id,))
        self.con.commit()

    @handle_sqlite_exceptions
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
                    Material[material] for material in json.loads(row[5] or "[]")
                ],  # Handle None or empty string for materials
                categories=[
                    (self.get_cognitive_category_by_id(cat[0]), cat[1])
                    for cat in json.loads(row[4] or "[]")
                ],  # Deserialize category IDs
                functions=[
                    (self.get_cognitive_function_by_id(func[0]), func[1])
                    for func in json.loads(row[3] or "[]")
                ],  # Deserialize function IDs
                image=row[6],
            )
            games.append(game)
        return games

    @handle_sqlite_exceptions
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

    @handle_sqlite_exceptions
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

    @handle_sqlite_exceptions
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

    @handle_sqlite_exceptions
    def get_all_cognitive_categories(self) -> list[CognitiveCategory]:
        logger.info("Getting all cognitive categories")
        cursor = self.con.execute("SELECT * FROM cognitive_categories")
        rows = cursor.fetchall()
        categories = []
        for row in rows:
            category = CognitiveCategory(id=row[0], name=row[1])
            categories.append(category)
        return categories

    @handle_sqlite_exceptions
    def get_all_cognitive_functions(self) -> list[CognitiveFunction]:
        logger.info("Getting all cognitive functions")
        cursor = self.con.execute("SELECT * FROM cognitive_functions")
        rows = cursor.fetchall()
        functions = []
        for row in rows:
            function = CognitiveFunction(id=row[0], name=row[1])
            functions.append(function)
        return functions

    @handle_sqlite_exceptions
    def get_cognitive_category_by_id(self, category_id: int) -> CognitiveCategory:
        cursor = self.con.execute(
            "SELECT * FROM cognitive_categories WHERE id = ?", (category_id,)
        )
        result = cursor.fetchone()
        if result is None:
            raise NotFoundError(f"Cognitive category with ID {category_id} not found.")
        return CognitiveCategory(id=result[0], name=result[1])

    @handle_sqlite_exceptions
    def get_cognitive_function_by_id(self, function_id: int) -> CognitiveFunction:
        cursor = self.con.execute(
            "SELECT * FROM cognitive_functions WHERE id = ?", (function_id,)
        )
        result = cursor.fetchone()
        if result is None:
            raise NotFoundError(f"Cognitive function with ID {function_id} not found.")
        return CognitiveFunction(id=result[0], name=result[1])
