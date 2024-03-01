from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model
# Have import from mysqlconnection on every model for DB interactions
# Import the model's python file as a module, not the class directly so you avoid circular import errors!
# For example: from flask_app.models import table2_model

'''
! Note: If you are working with tables that are related to each other, 
!       you'll want to import the other table's class here for when you need to create objects with that class. 

! Example: importing pets so we can make pet objects for our users that own them.

Class should match the data table exactly that's in your DB.

REMEMBER TO PARSE DATA INTO OBJECTS BEFORE SENDING TO PAGES!

'''

class Favorite:
    DB = 'space_schema'

    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.favorite_user = None

    @classmethod
    def create_favorite(cls, data):
        query = """
        INSERT INTO favorites (date, user_id)
        VALUES (%(date)s, %(user_id)s);
        """

        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def get_all_favorites(cls):
        query = """
        SELECT * FROM favorites
        JOIN users ON users.id = favorites.user_id;
        """

        results = connectToMySQL(cls.DB).query_db(query)

        all_favorites = []

        for row in results:
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }

            one_favorite = cls(row)
            one_favorite.favorite_user = user_model.User(user_data)
            all_favorites.append(one_favorite)

        return all_favorites

    @classmethod
    def get_one_favorite(cls, data):
        query = """
        SELECT * FROM favorites
        JOIN users ON users.id = favorites.user_id
        WHERE favorites.id = %(favorite_id)s;
        """

        results = connectToMySQL(cls.DB).query_db(query, data)

        one_favorite = cls(results[0])
        user_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }

        one_favorite.favorite_user = user_model.User(user_data)

        return one_favorite

    @classmethod
    def delete_favorite(cls, data):
        query = """
        DELETE FROM favorites
        WHERE id = %(favorite_id)s;
        """

        results = connectToMySQL(cls.DB).query_db(query, data)
        return results