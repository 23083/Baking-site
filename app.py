from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

# initialise app
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    # home page - Category
    sql = """SELECT * FROM Category;"""
    results = query_db(sql)
    return render_template("home.html", results=results)


@app.route("/category/<int:id>")
def category(id):
    # just one category based on the id
    sql = """ SELECT Recipe.RecipeID,Recipe.RecipeName,
    Recipe.Description,Recipe.ImageURL
    FROM Recipe
    JOIN Category ON Recipe.CategoryID=Category.CategoryID
    WHERE Category.CategoryID = ?;"""
    results = query_db(sql, (id,))
    return render_template("category.html", results=results)


@app.route("/recipe/<int:id>")
def recipe(id):
    sql = """SELECT RecipeID, RecipeName, Description, Instructions,
             TotalTime, Ingredients, ImageURL, CategoryID
             FROM Recipe
             WHERE RecipeID = ?;"""
    results = query_db(sql, (id,))
    if results and len(results) > 0:
        recipe_data = results[0]
    else:
        recipe_data = None
    return render_template("recipe.html", recipe=recipe_data)


@app.errorhandler(404)
def page_not_found(e):
    # Triggers if a user types a wrong URL path
    return render_template('error.html', error_title="Page Not Found (404)",
                           error_message="Oops! The recipe you are looking for doesn't exist."), 404


@app.errorhandler(500)
def internal_server_error(e):
    # Triggers if there is a database crash or code breaks
    return render_template('error.html', error_title="Server Error (500)",
                           error_message="Something went wrong. We are looking into it!"), 500


if __name__ == "__main__":
    app.run(debug=True)