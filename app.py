import datetime
import os

from flask import Flask, render_template, redirect, url_for, Response
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    results = []
    qry = db_session.query(Items)
    results = qry.all()

# Author:Sandhya Nagarajan
# Date : 06/09/2018
# Notes: <Bugfix>
# the 'results' tuple have the list of all the items in the db
# iterate through the list and add it to a outputFile
# read the file and return the content as a String
# (could have directly dumped it as string instead of writing into file
# wrote into a line to make the output more readable)
# <improvement>
# Its ideal to close the db session
    db_session.close()
    outputFile = open("outputFromDB.txt", "w")
    outputFile.write("The Query from the DB are : ")
    for currentItem in results:
        outputFile.write("\n" + currentItem.name + "  " + str(currentItem.quantity) + "  " + currentItem.description + "  " + str(currentItem.date_added))
    outputFile.close()
    outputFile = open("outputFromDB.txt", "r")
    outputString = Response(outputFile.read(), mimetype='text/plain' )
    outputFile.close()
    return outputString

# Author:Sandhya Nagarajan
# Date : 06/09/2018
# Notes: <Debugging>
# Enables the flask app to run in debug mode
app.config['DEBUG'] = True

# Author:Sandhya Nagarajan
# Date : 06/01/2018
# Notes: <Systems puzzle fix:
#Adding 5001 port to run lets us access from localhost.
# alternatively, we can change the port in dockerfile and flaskapp conf to 5000
# then there is no need to add the port explicity here
if __name__ == '__main__':
    app.run(host='0.0.0.0',port = '5001')
