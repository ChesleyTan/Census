from flask import Flask, render_template, redirect, request, flash, session
import fetch

app=Flask(__name__)
app.secret_key = 'eMG>h4_S:<o<Ow;_+Ja&imp(sLrr)aQO{(#r_NQa~.|HkTlDEtW{,bVs[3B!i=sy'

@app.route("/", methods=['GET'])
def index():
    submit = request.args.get("submit")
    if (submit == "View"):
        session['crit1'] = request.args.get("criteria1")
        session['crit2'] = request.args.get("criteria2")
        session['crit3'] = request.args.get("criteria3")
        session['crit4'] = request.args.get("criteria4")
        session['crit5'] = request.args.get("criteria5")
        session['state'] = request.args.get("state")
        return redirect("/results")
    
    categories = []
    for category in fetch.CATEGORY_FULLNAMES:
        categories.append(fetch.CATEGORY_FULLNAMES[category])
    categories.remove("State Name")

    states = []
    for state in fetch.STATES:
        if len(fetch.STATES[state])>1:
            states.append(fetch.STATES[state])
    
    return render_template("index.html", page_title="Home", categories=categories, states=states)

# TODO restrict method to POST
@app.route("/results", methods=['GET', 'POST'])
def results():
    # TODO remove testing demo
    categories = []
    for category in fetch.CATEGORY_FULLNAMES:
        for i in range(5):
            if (fetch.CATEGORY_FULLNAMES[category] == session['crit'+str(i+1)]):
                categories.append(category)

    return render_template("results.html", data_dict=fetch.getSummary(session.get('state'), categories), page_title="Results")

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=8080)
