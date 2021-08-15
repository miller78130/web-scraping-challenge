from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars_data = mongo.db.Mars.find_one()

    return render_template("index.html", link = mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.Mars.update({}, mars_data, upsert=True)
    #return "Scraping Successful!"
    
    # Redirect to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)