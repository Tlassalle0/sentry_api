from db import get_connection

connexion = get_connection()
curseur = connexion.cursor()

sql = "UPDATE produits SET prix = %s, stock = %s WHERE id = %s"
valeurs = (39.99, 15, 1)

curseur.execute(sql, valeurs)
connexion.commit()

print("Produit modifié avec succès")

curseur.close()
connexion.close()