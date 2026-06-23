from db import get_connection
# On importe la fonction qui permet d’ouvrir une connexion à MySQL.


def get_all_products():
    # Fonction qui récupère tous les produits de la base.

    connexion = get_connection()
    # On ouvre une connexion à MySQL.

    curseur = connexion.cursor(dictionary=True)
    # On crée un curseur.
    # dictionary=True permet d’obtenir les résultats sous forme de dictionnaires Python.
    # Exemple : {"id": 1, "nom": "Clavier", "prix": 49.99, "stock": 10}

    curseur.execute("SELECT id, nom, prix, stock FROM produits")
    # On exécute une requête SQL pour récupérer tous les produits.

    produits = curseur.fetchall()
    # fetchall() récupère toutes les lignes retournées par la requête.

    curseur.close()
    # On ferme le curseur.

    connexion.close()
    # On ferme la connexion à MySQL.

    return produits
    # On retourne la liste des produits à l’API.


def get_product_by_id(product_id):
    # Fonction qui récupère un seul produit à partir de son id.

    connexion = get_connection()
    # On ouvre une connexion à MySQL.

    curseur = connexion.cursor(dictionary=True)
    # On crée un curseur qui retourne des dictionnaires.

    sql = "SELECT id, nom, prix, stock FROM produits WHERE id = %s"
    # Requête SQL qui récupère un produit précis.
    # WHERE id = %s permet de cibler uniquement le produit demandé.

    curseur.execute(sql, (product_id,))
    # On exécute la requête avec l’id reçu.
    # (product_id,) est un tuple Python avec une seule valeur.

    produit = curseur.fetchone()
    # fetchone() récupère une seule ligne.

    curseur.close()
    # On ferme le curseur.

    connexion.close()
    # On ferme la connexion.

    return produit
    # On retourne le produit trouvé, ou None si aucun produit n’existe avec cet id.


def create_product(nom, prix, stock):
    # Fonction qui ajoute un nouveau produit dans la base.

    connexion = get_connection()
    # On ouvre une connexion à MySQL.

    curseur = connexion.cursor()
    # On crée un curseur pour exécuter une requête SQL.

    sql = "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)"
    # Requête SQL d’insertion.
    # Les %s sont des emplacements sécurisés pour les valeurs.

    valeurs = (nom, prix, stock)
    # Tuple contenant les valeurs à insérer.

    curseur.execute(sql, valeurs)
    # On exécute la requête avec les valeurs.

    connexion.commit()
    # commit() valide réellement l’insertion dans la base.
    # Sans commit(), la donnée peut ne pas être enregistrée.

    new_id = curseur.lastrowid
    # lastrowid récupère l’id du nouveau produit créé.

    curseur.close()
    # On ferme le curseur.

    connexion.close()
    # On ferme la connexion.

    return new_id
    # On retourne l’id du produit créé à l’API.


def update_product(product_id, nom, prix, stock):
    # Fonction qui modifie un produit existant.

    connexion = get_connection()
    # On ouvre une connexion à MySQL.

    curseur = connexion.cursor()
    # On crée un curseur.

    sql = "UPDATE produits SET nom = %s, prix = %s, stock = %s WHERE id = %s"
    # Requête SQL de modification.
    # WHERE id = %s est indispensable pour modifier uniquement le produit ciblé.

    valeurs = (nom, prix, stock, product_id)
    # Tuple contenant les nouvelles valeurs et l’id du produit à modifier.

    curseur.execute(sql, valeurs)
    # On exécute la requête SQL.

    connexion.commit()
    # On valide la modification dans MySQL.

    lignes_modifiees = curseur.rowcount
    # rowcount indique combien de lignes ont été modifiées.
    # Si rowcount vaut 0, aucun produit avec cet id n’a été trouvé.

    curseur.close()
    # On ferme le curseur.

    connexion.close()
    # On ferme la connexion.

    return lignes_modifiees
    # On retourne le nombre de lignes modifiées à l’API.


def delete_product(product_id):
    # Fonction qui supprime un produit à partir de son id.

    connexion = get_connection()
    # On ouvre une connexion à MySQL.

    curseur = connexion.cursor()
    # On crée un curseur.

    sql = "DELETE FROM produits WHERE id = %s"
    # Requête SQL de suppression.
    # WHERE id = %s évite de supprimer toute la table.

    curseur.execute(sql, (product_id,))
    # On exécute la requête avec l’id du produit à supprimer.

    connexion.commit()
    # On valide la suppression.

    lignes_supprimees = curseur.rowcount
    # rowcount indique combien de lignes ont été supprimées.

    curseur.close()
    # On ferme le curseur.

    connexion.close()
    # On ferme la connexion.

    return lignes_supprimees
    #