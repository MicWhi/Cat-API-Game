from flask import Flask, render_template, request
from cat import *

app = Flask(__name__)


@app.context_processor
def inject_data():
    """Enables the data stored in the csv files to be read and used in the HTML page."""
    data = {'image1': read_csv_data("cutest_cat.csv"),
            'image2': read_csv_data("challenger.csv"),
            'win_count': read_csv_data("win_count.csv")}

    return data


@app.route("/", methods=['POST', 'GET'])
def home():
    """Serves the web app for the user to interact with locally."""

    # The on screen buttons send POST requests when clicked and are captured here
    if request.method == 'POST':

        if request.form['submitted_button'] == "Cutie Pie":
            store_new_image_url('challenger.csv')
            increase_win_counter()

        elif request.form['submitted_button'] == "Challenger":
            transfer_challenger_to_cutest()
            store_new_image_url('challenger.csv')
            set_win_counter(1) # set to 1 after as the challenger gains first win by becoming "Cutie Pie"

        return render_template("battle_cats.html")

    # Loading or refreshing the page performs GET request
    # This starts a new game therefore loading new images and resetting the win counter
    else:
        initialise_images_and_win_counter()
        return render_template("battle_cats.html")


if __name__ == '__main__':
    app.run(debug=True)
