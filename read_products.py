from db import get_connection

connexion = get_connection()
curseur = connexion.cursor()

sql = "SELECT id, nom, prix, stock FROM produits"
curseur.execute(sql)

produits = curseur.fetchall()

for produit in produits:
    print(produit)

curseur.close()
connexion.close()