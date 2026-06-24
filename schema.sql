CREATE TABLE IF NOT EXISTS products (
    id    INT          NOT NULL AUTO_INCREMENT,
    nom   VARCHAR(255) NOT NULL,
    prix  FLOAT        NOT NULL,
    stock INT          NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO products (nom, prix, stock) VALUES
    ('Clavier', 49.99, 10),
    ('Souris', 29.99, 25),
    ('Écran', 199.99, 5);