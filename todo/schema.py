instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS todo;',
    'DROP TABLE IF EXISTS user;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password LONGTEXT NOT NULL
            )
    """,
    """
        CREATE TABLE todo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL,
            category VARCHAR(50),
            FOREIGN KEY (created_by) REFERENCES user (id),
            id_user INT NOT NULL DEFAULT '1',
            display_order INT NOT NULL DEFAULT '1'
        );
    """
]

# definimos las variables de entorno en la terminal
# export FLASK_DATABASE_HOST='localhost'
# export FLASK_DATABASE_PASSWORD='org22+'
# export FLASK_DATABASE_USER='alceo20'
# export FLASK_DATABASE='testing'

# password VARCHAR(100) NOT NULL
