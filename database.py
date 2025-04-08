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
            raise DuplicateError(f"A unique constraint was violated: {e}") from e
        except sqlite3.Error as e:
            raise DatabaseError(f"An error occurred with the database: {e}") from e

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

        # Update games to remove references to the deleted category
        cursor = self.con.execute("SELECT id, cognitive_categories FROM games")
        for game_id, categories_json in cursor.fetchall():
            if categories_json:
                categories = json.loads(categories_json)
                updated_categories = [
                    (cat_id, weight)
                    for cat_id, weight in categories
                    if cat_id != category_id
                ]
                self.con.execute(
                    "UPDATE games SET cognitive_categories = ? WHERE id = ?",
                    (json.dumps(updated_categories), game_id),
                )

        # Delete the cognitive category
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

        # Update games to remove references to the deleted function
        cursor = self.con.execute("SELECT id, cognitive_functions FROM games")
        for game_id, functions_json in cursor.fetchall():
            if functions_json:
                functions = json.loads(functions_json)
                updated_functions = [
                    (func_id, weight)
                    for func_id, weight in functions
                    if func_id != function_id
                ]
                self.con.execute(
                    "UPDATE games SET cognitive_functions = ? WHERE id = ?",
                    (json.dumps(updated_functions), game_id),
                )

        # Delete the cognitive function
        self.con.execute("DELETE FROM cognitive_functions WHERE id = ?", (function_id,))
        self.con.commit()

    @handle_sqlite_exceptions
    def get_game(self, game_id: int = None, game_title: str = None) -> Game:
        logger.info("Getting game")
        if game_id:
            cursor = self.con.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        elif game_title:
            cursor = self.con.execute(
                "SELECT * FROM games WHERE title = ?", (game_title,)
            )
        else:
            raise ValueError("Either game_id or game_title must be provided")

        row = cursor.fetchone()
        if not row:
            raise NotFoundError(
                f"Game with ID {game_id} or title {game_title} not found."
            )

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

        return game

    @handle_sqlite_exceptions
    def get_cognitive_category(
        self, category_id: int = None, category_name: str = None
    ) -> CognitiveCategory:
        logger.info("Getting cognitive category")
        if category_id:
            cursor = self.con.execute(
                "SELECT * FROM cognitive_categories WHERE id = ?", (category_id,)
            )
        elif category_name:
            cursor = self.con.execute(
                "SELECT * FROM cognitive_categories WHERE name = ?",
                (category_name,),
            )
        else:
            raise ValueError("Either category_id or category_name must be provided")

        row = cursor.fetchone()
        if not row:
            raise NotFoundError(
                f"Cognitive category with ID {category_id} or name {category_name} not found."
            )

        category = CognitiveCategory(id=row[0], name=row[1])
        return category

    @handle_sqlite_exceptions
    def get_cognitive_function(
        self, function_id: int = None, function_name: str = None
    ) -> CognitiveFunction:
        logger.info("Getting cognitive function")
        if function_id:
            cursor = self.con.execute(
                "SELECT * FROM cognitive_functions WHERE id = ?", (function_id,)
            )
        elif function_name:
            cursor = self.con.execute(
                "SELECT * FROM cognitive_functions WHERE name = ?",
                (function_name,),
            )
        else:
            raise ValueError("Either function_id or function_name must be provided")

        row = cursor.fetchone()
        if not row:
            raise NotFoundError(
                f"Cognitive function with ID {function_id} or name {function_name} not found."
            )

        function = CognitiveFunction(id=row[0], name=row[1])
        return function

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

    @handle_sqlite_exceptions
    def get_games_with_filters(
        self,
        game_title: str = None,
        cognitive_categories_ids: list[int] = None,
        cognitive_functions_ids: list[int] = None,
        materials: list[Material] = None,
    ) -> list[Game]:
        if cognitive_categories_ids is None:
            cognitive_categories_ids = []
        if cognitive_functions_ids is None:
            cognitive_functions_ids = []
        if materials is None:
            materials = []

        logger.info("Fetching games with filters")
        query = "SELECT * FROM games WHERE 1=1"
        params = []

        # Filter by game title
        if game_title:
            query += " AND title LIKE ?"
            params.append(f"%{game_title}%")

        # Filter by cognitive categories
        if cognitive_categories_ids:
            query += (
                " AND ("
                + " OR ".join(["json_each.value = ?"] * len(cognitive_categories_ids))
                + ")"
            )
            params.extend(cognitive_categories_ids)
            query = f"""
                {query}
                AND EXISTS (
                    SELECT 1 FROM json_each(games.cognitive_categories)
                    WHERE json_each.value IN ({','.join(['?'] * len(cognitive_categories_ids))})
                )
            """

        # Filter by cognitive functions
        if cognitive_functions_ids:
            query += (
                " AND ("
                + " OR ".join(["json_each.value = ?"] * len(cognitive_functions_ids))
                + ")"
            )
            params.extend(cognitive_functions_ids)
            query = f"""
                {query}
                AND EXISTS (
                    SELECT 1 FROM json_each(games.cognitive_functions)
                    WHERE json_each.value IN ({','.join(['?'] * len(cognitive_functions_ids))})
                )
            """

        # Filter by materials
        if materials:
            material_names = [material.name for material in materials]
            query += (
                " AND ("
                + " OR ".join(["json_each.value = ?"] * len(material_names))
                + ")"
            )
            params.extend(material_names)
            query = f"""
                {query}
                AND EXISTS (
                    SELECT 1 FROM json_each(games.materials)
                    WHERE json_each.value IN ({','.join(['?'] * len(material_names))})
                )
            """

        cursor = self.con.execute(query, params)
        rows = cursor.fetchall()
        games = []
        for row in rows:
            game = Game(
                id=row[0],
                title=row[1],
                description=row[2],
                materials=[
                    Material[material] for material in json.loads(row[5] or "[]")
                ],
                categories=[
                    (self.get_cognitive_category_by_id(cat[0]), cat[1])
                    for cat in json.loads(row[4] or "[]")
                ],
                functions=[
                    (self.get_cognitive_function_by_id(func[0]), func[1])
                    for func in json.loads(row[3] or "[]")
                ],
                image=row[6],
            )
            games.append(game)
        return games
