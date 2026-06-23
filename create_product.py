from db import get_connection

connexion = get_connection()
curseur = connexion.cursor()

sql = "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)"
valeurs = ("Clavier", 49.99, 10)

curseur.execute(sql, valeurs)
connexion.commit()

print("Produit ajouté avec succès")

curseur.close()
connexion.close()