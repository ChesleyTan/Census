from flask import Flask, render_template, redirect, request, flash
import fetch

app=Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    categories = {}
    for category in fetch.CATEGORY_FULLNAMES:
        if category != fetch.NAME:
            categories[category] = fetch.CATEGORY_FULLNAMES[category]

    states = []
    for state in fetch.STATES:
        if len(fetch.STATES[state])>1:
            states.append(fetch.STATES[state])
    
    return render_template("index.html", page_title="Home", categories=categories, states=states)

@app.route("/results", methods=['POST'])
def results():
    categories = []
    category_prefix="criteria"
    for i in [1,2,3,4,5]:
        category = request.form[category_prefix + str(i)]
        if category != 'None' and category in fetch.CATEGORY_FULLNAMES:
            categories.append(category)

    return render_template("results.html",
            data_dict=fetch.getSummary(request.form['state'], categories), page_title="Results")

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=8080)
