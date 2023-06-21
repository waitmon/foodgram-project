class UsersEndpoints:
    """Endpoints for operations with users profiles"""

    url_user_registration = 'http://127.0.0.1:8000/api/users/'
    url_user_list = 'http://127.0.0.1:8000/api/users/'
    url_current_user_profile = 'http://127.0.0.1:8000/api/users/me/'
    url_change_password = 'http://127.0.0.1:8000/api/users/set_password/'
    url_auth_token = 'http://127.0.0.1:8000/api/auth/token/login/'
    url_logout = 'http://127.0.0.1:8000/api/auth/token/logout/'


class TagsEndpoints:
    """Endpoint for getting tags"""

    url_tags_list = 'http://127.0.0.1:8000/api/tags/'


class RecipesEndpoints:
    """Endpoint for recipes CRUD operations"""
    url_recipes = 'http://127.0.0.1:8000/api/recipes/'


class ShoppingListEndpoints:
    """Endpoint for shopping list CRUD operations"""
    url_shopping_list = f'http://127.0.0.1:8000/api/recipes/{id}/shopping_cart'
    url_download_shopping_list = 'http://127.0.0.1:8000/api/recipes/download_shopping_cart/'


class FavoritesEndpoints:
    """Endpoint for favorites creating/deleting"""
    url_favorite = f'http://127.0.0.1:8000/api/recipes/{id}/favorite'


class IngredientsEndpoints:
    """Endpoints for ingredients getting"""
    url_ingredients_list = 'http://127.0.0.1:8000/api/ingredients/'
    url_get_ingredient_id = f'http://127.0.0.1:8000/api/ingredients/{id}/'


class SubscriptionsEndpoints:
    """Endpoints for subscriptions"""
    url_subscription_list = 'http://127.0.0.1:8000/api/users/subscriptions/'
