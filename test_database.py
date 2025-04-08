import unittest
import os
from database import Database, NotFoundError
from models import Game, CognitiveCategory, CognitiveFunction, Material


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_file = "test_temp.db"
        self.db = Database(file=self.db_file)
        self.db.setup()

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_add_and_get_cognitive_category(self):
        category = CognitiveCategory(name="Memory")
        self.db.add_cognitive_category(category)

        categories = self.db.get_cognitive_category(category_name="Memory")
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].name, "Memory")

    def test_add_and_get_cognitive_function(self):
        function = CognitiveFunction(name="Attention")
        self.db.add_cognitive_function(function)

        functions = self.db.get_cognitive_function(function_name="Attention")
        self.assertEqual(len(functions), 1)
        self.assertEqual(functions[0].name, "Attention")

    def test_add_and_get_game_with_image(self):
        category = CognitiveCategory(name="Memory")
        function = CognitiveFunction(name="Attention")
        self.db.add_cognitive_category(category)
        self.db.add_cognitive_function(function)

        category_id = self.db.get_cognitive_category(category_name="Memory")[0].id
        function_id = self.db.get_cognitive_function(function_name="Attention")[0].id

        game = Game(
            title="Game with Image",
            description="A game with an image",
            image="image_path.png",
            materials=[Material.VISUAL, Material.VERBAL],
            categories=[(CognitiveCategory(id=category_id, name="Memory"), 5)],
            functions=[(CognitiveFunction(id=function_id, name="Attention"), 3)],
        )
        self.db.add_game(game)

        games = self.db.get_game(game_title="Game with Image")
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Game with Image")
        self.assertEqual(games[0].image, "image_path.png")

    def test_add_and_get_game_without_image(self):
        category = CognitiveCategory(name="Memory")
        function = CognitiveFunction(name="Attention")
        self.db.add_cognitive_category(category)
        self.db.add_cognitive_function(function)

        category_id = self.db.get_cognitive_category(category_name="Memory")[0].id
        function_id = self.db.get_cognitive_function(function_name="Attention")[0].id

        game = Game(
            title="Game without Image",
            description="A game without an image",
            image=None,
            materials=[Material.TACTILE],
            categories=[(CognitiveCategory(id=category_id, name="Memory"), 5)],
            functions=[(CognitiveFunction(id=function_id, name="Attention"), 3)],
        )
        self.db.add_game(game)

        games = self.db.get_game(game_title="Game without Image")
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Game without Image")
        self.assertIsNone(games[0].image)

    def test_get_game_without_id_or_title(self):
        with self.assertRaises(ValueError):
            self.db.get_game()

    def test_get_cognitive_category_without_id_or_name(self):
        with self.assertRaises(ValueError):
            self.db.get_cognitive_category()

    def test_get_cognitive_function_without_id_or_name(self):
        with self.assertRaises(ValueError):
            self.db.get_cognitive_function()

    def test_get_all_cognitive_categories(self):
        category1 = CognitiveCategory(name="Memory")
        category2 = CognitiveCategory(id=2, name="Language")
        self.db.add_cognitive_category(category1)
        self.db.add_cognitive_category(category2)

        categories = self.db.get_all_cognitive_categories()
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0].name, "Memory")
        self.assertEqual(categories[1].name, "Language")

    def test_get_all_cognitive_functions(self):
        function1 = CognitiveFunction(name="Attention")
        function2 = CognitiveFunction(id=2, name="Perception")
        self.db.add_cognitive_function(function1)
        self.db.add_cognitive_function(function2)

        functions = self.db.get_all_cognitive_functions()
        self.assertEqual(len(functions), 2)
        self.assertEqual(functions[0].name, "Attention")
        self.assertEqual(functions[1].name, "Perception")

    def test_get_all_games(self):
        category = CognitiveCategory(name="Memory")
        function = CognitiveFunction(name="Attention")
        game1 = Game(
            title="Game 1",
            description="First game",
            image="image1.png",
            materials=[Material.AUDITORY],
            categories=[(category, 5)],
            functions=[(function, 3)],
        )
        game2 = Game(
            title="Game 2",
            description="Second game",
            image="image2.png",
            materials=[Material.VISUAL, Material.TACTILE],
            categories=[(category, 4)],
            functions=[(function, 2)],
        )
        self.db.add_game(game1)
        self.db.add_game(game2)

        games = self.db.get_all_games()
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0].title, "Game 1")
        self.assertEqual(games[1].title, "Game 2")

    def test_update_and_delete_cognitive_category(self):
        category = CognitiveCategory(name="Memory")
        self.db.add_cognitive_category(category)

        categories = self.db.get_cognitive_category(category_name="Memory")
        category = categories[0]
        category.name = "Updated Memory"
        self.db.update_cognitive_category(category)

        updated_categories = self.db.get_cognitive_category(
            category_name="Updated Memory"
        )
        self.assertEqual(len(updated_categories), 1)
        self.assertEqual(updated_categories[0].name, "Updated Memory")

        self.db.delete_cognitive_category(category.id)
        deleted_categories = self.db.get_cognitive_category(
            category_name="Updated Memory"
        )
        self.assertEqual(len(deleted_categories), 0)

    def test_update_and_delete_cognitive_function(self):
        function = CognitiveFunction(name="Attention")
        self.db.add_cognitive_function(function)

        functions = self.db.get_cognitive_function(function_name="Attention")
        function = functions[0]
        function.name = "Updated Attention"
        self.db.update_cognitive_function(function)

        updated_functions = self.db.get_cognitive_function(
            function_name="Updated Attention"
        )
        self.assertEqual(len(updated_functions), 1)
        self.assertEqual(updated_functions[0].name, "Updated Attention")

        self.db.delete_cognitive_function(function.id)
        deleted_functions = self.db.get_cognitive_function(
            function_name="Updated Attention"
        )
        self.assertEqual(len(deleted_functions), 0)

    def test_update_and_delete_game(self):
        game = Game(
            title="Game to Update",
            description="A game to be updated",
            image="image_path.png",
            materials=[Material.VISUAL],
            categories=[],
            functions=[],
        )
        self.db.add_game(game)

        games = self.db.get_game(game_title="Game to Update")
        game = games[0]
        game.title = "Updated Game"
        game.description = "Updated description"
        self.db.update_game(game)

        updated_games = self.db.get_game(game_title="Updated Game")
        self.assertEqual(len(updated_games), 1)
        self.assertEqual(updated_games[0].title, "Updated Game")
        self.assertEqual(updated_games[0].description, "Updated description")

        self.db.delete_game(game.id)
        deleted_games = self.db.get_game(game_title="Updated Game")
        self.assertEqual(len(deleted_games), 0)

    def test_update_game_invalid_id(self):
        category = CognitiveCategory(name="Memory")
        function = CognitiveFunction(name="Attention")
        game = Game(
            id=None,
            title="Invalid Game",
            description="Invalid game description",
            image="image_path.png",
            materials=[Material.VISUAL],
            categories=[(category, 5)],
            functions=[(function, 3)],
        )
        with self.assertRaises(ValueError) as context:
            self.db.update_game(game)
        self.assertEqual(str(context.exception), "Game ID must be a positive number")

    def test_delete_game_invalid_id(self):
        with self.assertRaises(ValueError) as context:
            self.db.delete_game(-1)
        self.assertEqual(str(context.exception), "Game ID must be a positive number")

    def test_update_cognitive_category_invalid_id(self):
        category = CognitiveCategory(id=None, name="Invalid Category")
        with self.assertRaises(ValueError) as context:
            self.db.update_cognitive_category(category)
        self.assertEqual(
            str(context.exception), "Cognitive Category ID must be a positive number"
        )

    def test_delete_cognitive_category_invalid_id(self):
        with self.assertRaises(ValueError) as context:
            self.db.delete_cognitive_category(-1)
        self.assertEqual(
            str(context.exception), "Cognitive Category ID must be a positive number"
        )

    def test_update_cognitive_function_invalid_id(self):
        function = CognitiveFunction(id=None, name="Invalid Function")
        with self.assertRaises(ValueError) as context:
            self.db.update_cognitive_function(function)
        self.assertEqual(
            str(context.exception), "Cognitive Function ID must be a positive number"
        )

    def test_delete_cognitive_function_invalid_id(self):
        with self.assertRaises(ValueError) as context:
            self.db.delete_cognitive_function(-1)
        self.assertEqual(
            str(context.exception), "Cognitive Function ID must be a positive number"
        )

    def test_get_game_with_empty_fields(self):
        game = Game(
            title="Game with Empty Fields",
            description="A game with empty fields",
            image=None,
            materials=[],
            categories=[],
            functions=[],
        )
        self.db.add_game(game)

        games = self.db.get_game(game_title="Game with Empty Fields")
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Game with Empty Fields")
        self.assertEqual(games[0].materials, [])
        self.assertEqual(games[0].categories, [])
        self.assertEqual(games[0].functions, [])

    def test_get_game_no_matches(self):
        games = self.db.get_game(game_title="Nonexistent Game")
        self.assertEqual(len(games), 0)

    def test_get_cognitive_category_by_id(self):
        # Case: Category exists
        category = CognitiveCategory(name="Memory")
        self.db.add_cognitive_category(category)

        categories = self.db.get_cognitive_category(category_name="Memory")
        category_id = categories[0].id

        fetched_category = self.db.get_cognitive_category_by_id(category_id)
        self.assertEqual(fetched_category.id, category_id)
        self.assertEqual(fetched_category.name, "Memory")

        # Case: Category does not exist
        with self.assertRaises(NotFoundError) as context:
            self.db.get_cognitive_category_by_id(999)
        self.assertEqual(
            str(context.exception), "Cognitive category with ID 999 not found."
        )

    def test_get_cognitive_function_by_id(self):
        # Case: Function exists
        function = CognitiveFunction(name="Attention")
        self.db.add_cognitive_function(function)

        functions = self.db.get_cognitive_function(function_name="Attention")
        function_id = functions[0].id

        fetched_function = self.db.get_cognitive_function_by_id(function_id)
        self.assertEqual(fetched_function.id, function_id)
        self.assertEqual(fetched_function.name, "Attention")

        # Case: Function does not exist
        with self.assertRaises(NotFoundError) as context:
            self.db.get_cognitive_function_by_id(999)
        self.assertEqual(
            str(context.exception), "Cognitive function with ID 999 not found."
        )

    def test_delete_cognitive_category_updates_games(self):
        category1 = CognitiveCategory(name="Memory")
        category2 = CognitiveCategory(name="Language")
        self.db.add_cognitive_category(category1)
        self.db.add_cognitive_category(category2)

        category1_id = self.db.get_cognitive_category(category_name="Memory")[0].id
        category2_id = self.db.get_cognitive_category(category_name="Language")[0].id

        game = Game(
            title="Game with Categories",
            description="A game with categories",
            image=None,
            materials=[],
            categories=[(CognitiveCategory(id=category1_id, name="Memory"), 5), 
                        (CognitiveCategory(id=category2_id, name="Language"), 3)],
            functions=[],
        )
        self.db.add_game(game)

        self.db.delete_cognitive_category(category1_id)

        games = self.db.get_game(game_title="Game with Categories")
        self.assertEqual(len(games), 1)
        self.assertEqual(len(games[0].categories), 1)
        self.assertEqual(games[0].categories[0][0].id, category2_id)

    def test_delete_cognitive_function_updates_games(self):
        function1 = CognitiveFunction(name="Attention")
        function2 = CognitiveFunction(name="Perception")
        self.db.add_cognitive_function(function1)
        self.db.add_cognitive_function(function2)

        function1_id = self.db.get_cognitive_function(function_name="Attention")[0].id
        function2_id = self.db.get_cognitive_function(function_name="Perception")[0].id

        game = Game(
            title="Game with Functions",
            description="A game with functions",
            image=None,
            materials=[],
            categories=[],
            functions=[(CognitiveFunction(id=function1_id, name="Attention"), 4), 
                       (CognitiveFunction(id=function2_id, name="Perception"), 2)],
        )
        self.db.add_game(game)

        self.db.delete_cognitive_function(function1_id)

        games = self.db.get_game(game_title="Game with Functions")
        self.assertEqual(len(games), 1)
        self.assertEqual(len(games[0].functions), 1)
        self.assertEqual(games[0].functions[0][0].id, function2_id)

    def test_get_games_with_filters_by_title(self):
        game1 = Game(
            title="Memory Game",
            description="A game about memory",
            image=None,
            materials=[],
            categories=[],
            functions=[],
        )
        game2 = Game(
            title="Attention Game",
            description="A game about attention",
            image=None,
            materials=[],
            categories=[],
            functions=[],
        )
        self.db.add_game(game1)
        self.db.add_game(game2)

        games = self.db.get_games_with_filters(game_title="Memory")
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Memory Game")

    def test_get_games_with_filters_by_cognitive_category(self):
        category = CognitiveCategory(name="Memory")
        self.db.add_cognitive_category(category)
        category_id = self.db.get_cognitive_category(category_name="Memory")[0].id

        game1 = Game(
            title="Game with Memory",
            description="A game with memory category",
            image=None,
            materials=[],
            categories=[(CognitiveCategory(id=category_id, name="Memory"), 5)],
            functions=[],
        )
        game2 = Game(
            title="Attention Game",
            description="A game about attention",
            image=None,
            materials=[],
            categories=[],
            functions=[],
        )
        self.db.add_game(game1)
        self.db.add_game(game2)

        games = self.db.get_games_with_filters(cognitive_categories_ids=[category_id])
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Game with Memory")

    def test_get_games_with_filters_by_cognitive_function(self):
        function = CognitiveFunction(name="Attention")
        self.db.add_cognitive_function(function)
        function_id = self.db.get_cognitive_function(function_name="Attention")[0].id

        game1 = Game(
            title="Game with Memory",
            description="A game with memory category",
            image=None,
            materials=[],
            categories=[],
            functions=[],
        )
        game2 = Game(
            title="Game with Attention",
            description="A game with attention function",
            image=None,
            materials=[],
            categories=[],
            functions=[(CognitiveFunction(id=function_id, name="Attention"), 3)],
        )
        self.db.add_game(game1)
        self.db.add_game(game2)

        games = self.db.get_games_with_filters(cognitive_functions_ids=[function_id])
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Game with Attention")

    def test_get_games_with_filters_by_materials(self):
        game1 = Game(
            title="Game with Visual Material",
            description="A game with visual material",
            image=None,
            materials=[Material.VISUAL],
            categories=[],
            functions=[],
        )
        game2 = Game(
            title="Game with Tactile Material",
            description="A game with Tactile material",
            image=None,
            materials=[Material.TACTILE],
            categories=[],
            functions=[],
        )
        self.db.add_game(game1)
        self.db.add_game(game2)

        games = self.db.get_games_with_filters(materials=[Material.VISUAL])
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Game with Visual Material")

    def test_get_games_with_filters_combined(self):
        category = CognitiveCategory(name="Memory")
        function = CognitiveFunction(name="Attention")
        self.db.add_cognitive_category(category)
        self.db.add_cognitive_function(function)

        category_id = self.db.get_cognitive_category(category_name="Memory")[0].id
        function_id = self.db.get_cognitive_function(function_name="Attention")[0].id

        game = Game(
            title="Complex Game",
            description="A game with multiple filters",
            image=None,
            materials=[Material.VISUAL],
            categories=[(CognitiveCategory(id=category_id, name="Memory"), 5)],
            functions=[(CognitiveFunction(id=function_id, name="Attention"), 3)],
        )
        self.db.add_game(game)

        games = self.db.get_games_with_filters(
            game_title="Complex",
            cognitive_categories_ids=[category_id],
            cognitive_functions_ids=[function_id],
            materials=[Material.VISUAL],
        )
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].title, "Complex Game")

    def test_get_games_with_filters_no_matches(self):
        games = self.db.get_games_with_filters(game_title="Nonexistent Game")
        self.assertEqual(len(games), 0)


if __name__ == "__main__":
    unittest.main()
