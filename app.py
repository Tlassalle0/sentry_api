from flask import Flask
# On importe Flask pour créer l’application web/API.

from flask_cors import CORS
# On importe CORS pour autoriser les appels depuis un frontend ou un outil externe.

from flask_restx import Api, Resource, fields
# Api permet de créer une API documentée avec Swagger.
# Resource permet de créer des classes de routes API.
# fields permet de décrire les champs JSON visibles dans Swagger.

import sentry_sdk

from crud_product import (
    get_all_products,
    # Fonction qui retourne tous les produits depuis MySQL.

    get_product_by_id,
    # Fonction qui retourne un produit précis.

    create_product,
    # Fonction qui ajoute un produit dans MySQL.

    update_product,
    # Fonction qui modifie un produit dans MySQL.

    delete_product
    # Fonction qui supprime un produit dans MySQL.
)
# On importe toutes les fonctions SQL depuis le repository.

import logging
# On importe logging.

from logging.handlers import RotatingFileHandler
# On importe RotatingFileHandler pour gérer la rotation des fichiers.

logger = logging.getLogger("api_logger")
# On crée un logger nommé api_logger.

logger.setLevel(logging.INFO)
# On définit le niveau minimum du logger.

handler = RotatingFileHandler(
    "api.log",
    # Fichier principal de logs.

    maxBytes=1000000,
    # Taille maximale du fichier avant rotation : environ 1 Mo.

    backupCount=3
    # Nombre de fichiers de sauvegarde conservés.
)
# On crée le handler de rotation.

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# On définit le format des logs.

handler.setFormatter(formatter)
# On applique le format au handler.

logger.addHandler(handler)
# On attache le handler au logger.

sentry_sdk.init(
    dsn="https://c615b0d3953b06723c631432d1dc3b60@o4511615126208512.ingest.de.sentry.io/4511615161335888",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

app = Flask(__name__)
# On crée l’application Flask principale.

CORS(app)
# On active CORS sur l’application.

logger.info("App start")


api = Api(
    app,
    # On associe Flask-RESTX à l’application Flask.

    version="1.0",
    # Version de l’API affichée dans Swagger.

    title="API Produits",
    # Titre affiché en haut de la documentation Swagger.

    description="API Python Flask connectée à MySQL/phpMyAdmin",
    # Description de l’API affichée dans Swagger.

    doc="/swagger"
    # URL de la documentation Swagger.
    # L’interface sera disponible sur http://127.0.0.1:5000/swagger
)


product_namespace = api.namespace(
    "products",
    # Nom du groupe de routes dans Swagger.
    # Les routes seront affichées dans une section products.

    description="Gestion des produits"
    # Description de cette section Swagger.
)


product_model = api.model("Product", {
    # Modèle JSON attendu pour créer ou modifier un produit.

    "nom": fields.String(required=True, description="Nom du produit", example="Clavier"),
    # Champ texte obligatoire.
    # Swagger affichera un exemple avec la valeur "Clavier".

    "prix": fields.Float(required=True, description="Prix du produit", example=49.99),
    # Champ numérique décimal obligatoire.
    # Swagger affichera 49.99 comme exemple.

    "stock": fields.Integer(required=True, description="Stock disponible", example=10)
    # Champ entier obligatoire.
    # Swagger affichera 10 comme exemple.
})


product_response_model = api.model("ProductResponse", {
    # Modèle JSON utilisé pour décrire la réponse d’un produit.

    "id": fields.Integer(description="Identifiant du produit", example=1),
    # Identifiant du produit retourné par MySQL.

    "nom": fields.String(description="Nom du produit", example="Clavier"),
    # Nom du produit retourné par l’API.

    "prix": fields.Float(description="Prix du produit", example=49.99),
    # Prix du produit retourné par l’API.

    "stock": fields.Integer(description="Stock disponible", example=10)
    # Stock du produit retourné par l’API.
})


@app.route("/error")
def hello_world():
    1/0  # raises an error
    return "<p>Hello, World!</p>"

@app.route("/health")
def hello_world():
    return "<p>Healthy</p>"

@product_namespace.route("")
# On crée la route /products dans le namespace products.

class ProductList(Resource):
    # Cette classe gère la liste complète des produits.

    @product_namespace.marshal_list_with(product_response_model)
    # Indique à Swagger que la réponse est une liste de produits.

    def get(self):
        # Cette méthode répond à GET /products.
        logger.info("Got all products")
        return get_all_products()
        # On récupère tous les produits depuis MySQL et on les retourne.


    @product_namespace.expect(product_model)
    # Indique à Swagger que cette route attend un JSON de type Product.

    def post(self):
        # Cette méthode répond à POST /products.

        data = api.payload
        # api.payload récupère le JSON envoyé par le client dans Swagger ou Postman.

        nom = data.get("nom")
        # On récupère le champ nom du JSON.

        prix = data.get("prix")
        # On récupère le champ prix du JSON.

        stock = data.get("stock")
        # On récupère le champ stock du JSON.

        if not nom or prix is None or stock is None:
            # On vérifie que les champs obligatoires sont présents.

            return {
                "error": "nom, prix et stock sont obligatoires"
            }, 400
            # On retourne une erreur 400 si une donnée manque.

        new_id = create_product(nom, prix, stock)
        # On insère le produit dans MySQL et on récupère son nouvel id.

        return {
            "message": "Produit créé",
            "id": new_id
        }, 201
        # On retourne un message de création avec le code HTTP 201.


@product_namespace.route("/<int:product_id>")
# On crée les routes /products/1, /products/2, etc.

class ProductItem(Resource):
    # Cette classe gère un produit précis.

    @product_namespace.marshal_with(product_response_model)
    # Indique à Swagger que cette route retourne un produit.

    def get(self, product_id):
        # Cette méthode répond à GET /products/{product_id}.
        logger.info("Get specific product")

        produit = get_product_by_id(product_id)
        # On cherche le produit dans MySQL.

        if produit is None:
            # Si aucun produit n’est trouvé.
            logger.error("Product not found")

            api.abort(404, "Produit introuvable")
            # On retourne une erreur 404 dans Swagger.

        logger.info("Product found")
        return produit
        # On retourne le produit trouvé.


    @product_namespace.expect(product_model)
    # Indique à Swagger que cette route attend un JSON de type Product.

    def put(self, product_id):
        # Cette méthode répond à PUT /products/{product_id}.

        data = api.payload
        # On récupère le JSON envoyé dans la requête.

        nom = data.get("nom")
        # On récupère le nouveau nom.

        prix = data.get("prix")
        # On récupère le nouveau prix.

        stock = data.get("stock")
        # On récupère le nouveau stock.

        if not nom or prix is None or stock is None:
            # On vérifie que les données nécessaires sont présentes.

            return {
                "error": "nom, prix et stock sont obligatoires"
            }, 400
            # On retourne une erreur 400 si le JSON est incomplet.

        lignes_modifiees = update_product(product_id, nom, prix, stock)
        # On modifie le produit dans MySQL.
        # La fonction retourne le nombre de lignes modifiées.

        if lignes_modifiees == 0:
            # Si aucune ligne n’est modifiée, l’id n’existe pas.

            api.abort(404, "Produit introuvable")
            # On retourne une erreur 404.

        return {
            "message": "Produit modifié"
        }
        # On retourne un message de succès.


    def delete(self, product_id):
        # Cette méthode répond à DELETE /products/{product_id}.

        lignes_supprimees = delete_product(product_id)
        # On supprime le produit dans MySQL.
        # La fonction retourne le nombre de lignes supprimées.

        if lignes_supprimees == 0:
            # Si aucune ligne n’est supprimée, l’id n’existe pas.

            api.abort(404, "Produit introuvable")
            # On retourne une erreur 404.

        return {
            "message": "Produit supprimé"
        }
        # On retourne un message de succès.


if __name__ == "__main__":
    # Ce bloc s’exécute seulement quand on lance ce fichier directement.

    app.run(debug=True)
    # On démarre le serveur Flask.
    # debug=True active 