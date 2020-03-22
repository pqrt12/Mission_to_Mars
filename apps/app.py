from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping
import time

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   print("Scraping Successful!")
   time.sleep(1)
   return redirect("/")

@app.route("/hemispheres/<index>")
def show_hemisphere(index):
   idx = int(index)
   mars = mongo.db.mars.find_one()
   if (idx >= len(mars["hemispheres"])) or (idx < 0):
      idx = 0
   hemi = mars["hemispheres"][idx]
   return render_template("hemisphere.html", hemisphere=hemi)


if __name__ == "__main__":
   app.run()
