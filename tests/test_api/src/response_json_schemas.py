from pytest_voluptuous import S
from voluptuous import Optional


class RequestSamplesSchemas:
    """Json schemas for validation."""
    json_schema_registration_response = S({
        "email": str,
        "id": int,
        "username": str,
        "first_name": str,
        "last_name": str
    })

    json_schema_users_list = S(

            {
                "count": int,
                "next": str,
                "previous": None,
                "results": [
                    {
                        "email": str,
                        "id": int,
                        "username": str,
                        "first_name": str,
                        "last_name": str,
                        "is_subscribed": bool
                    }
                ]
            }

    )
    json_schema_user_profile = S(
        {
            "email": str,
            "id": int,
            "username": str,
            "first_name": str,
            "last_name": str,
            "is_subscribed": bool
        }
    )

    json_schema_tags = S(
        [
            {
                "id": int,
                "name": str,
                "color": str,
                "slug": str
            }
        ]
    )

    json_schema_recipes = S(
        {
            "count": int,
            "next": str,
            "previous": str,
            "results": [
                {
                    "id": int,
                    "tags": [
                        {
                            "id": int,
                            "name": str,
                            "color": str,
                            "slug": str
                        }
                    ],
                    "author": {
                        "email": str,
                        "id": int,
                        "username": str,
                        "first_name": str,
                        "last_name": str,
                        "is_subscribed": bool
                    },
                    "ingredients": [
                        {
                            "id": int,
                            "name": str,
                            "measurement_unit": str,
                            "amount": int
                        }
                    ],
                    "is_favorited": bool,
                    "is_in_shopping_cart": bool,
                    "name": str,
                    "image": str,
                    "text": str,
                    "cooking_time": int
                }
            ]
        }
    )
    json_schema_add_to_shopping_list_and_favorites = S(
        {
            "id": int,
            "name": str,
            "image": str,
            "cooking_time": int
        }
    )

    json_schema_my_subscriptions = S(
        {
            "count": int,
            Optional("next"): None,
            Optional("previous"): None,
            "results": [
                {
                    "email": str,
                    "id": int,
                    "username": str,
                    "first_name": str,
                    "last_name": str,
                    "is_subscribed": bool,
                    "recipes": [
                        {
                            "id": int,
                            "name": str,
                            "image": str,
                            "cooking_time": int
                        }
                    ],
                    "recipes_count": int
                }
            ]
        }
    )

    json_schema_user_subscription = S(
        {
            "email": str,
            "id": int,
            "username": str,
            "first_name": str,
            "last_name": str,
            "is_subscribed": bool,
            "recipes": [
                {
                    "id": int,
                    "name": str,
                    "image": str,
                    "cooking_time": int
                }
            ],
            "recipes_count": int
        }
    )

    json_schema_ingredients = S(
        [
            {
                "id": int,
                "name": str,
                "measurement_unit": str
            }
        ]
    )
