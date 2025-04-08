CREATE TABLE IF NOT EXISTS cognitive_categories (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL UNIQUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_cognitive_categories_name ON cognitive_categories (name);
CREATE INDEX IF NOT EXISTS idx_cognitive_categories_id ON cognitive_categories (id);
CREATE TABLE IF NOT EXISTS cognitive_functions (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL UNIQUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_cognitive_functions_name ON cognitive_functions (name);
CREATE INDEX IF NOT EXISTS idx_cognitive_functions_id ON cognitive_functions (id);
CREATE TABLE IF NOT EXISTS games (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `title` TEXT NOT NULL UNIQUE,
    `description` TEXT NOT NULL,
    `cognitive_functions` TEXT, -- Stores [(function_id, weight)] as JSON
    `cognitive_categories` TEXT, -- Stores [(category_id, weight)] as JSON
    `materials` TEXT,
    `image` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_games_title ON games (title);
CREATE INDEX IF NOT EXISTS idx_games_id ON games (id);