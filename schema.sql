CREATE TABLE IF NOT EXISTS products (
    id    INT          NOT NULL AUTO_INCREMENT,
    nom   VARCHAR(255) NOT NULL,
    prix  FLOAT        NOT NULL,
    stock INT          NOT NULL,
    PRIMARY KEY (id)
);