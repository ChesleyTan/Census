from flask import Flask, render_template, redirect, request, flash
import fetch

app=Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", page_title="Home")

# TODO restrict method to POST
@app.route("/results", methods=['GET', 'POST'])
def results():
    # TODO remove testing demo
    state = "New York"
    categories = [fetch.TOTAL_POPULATION]
    return render_template("results.html", data_dict=fetch.getSummary(state, categories), page_title="Results")

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=8080)
