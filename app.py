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
    sql = """
                SELECT * FROM Category;"""
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
    TotalTime, Ingredients, ImageURL
      FROM Recipe
      WHERE RecipeID = ?;"""
    results = query_db(sql, (id,))
    if not results:
        return "Recipe ID not found in database!"
    return render_template("recipe.html", recipe=results[0])


# results = query_db(sql, (id,), one=True)
# return render_template("recipe.html", recipe=results)


if __name__ == "__main__":
    app.run(debug=True)