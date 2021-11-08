import sqlite3
from flask import g, Flask, jsonify, request

DATABASE = 'data.db'
app = Flask(__name__)
#takes care of Portuguese characters
app.config['JSON_AS_ASCII'] = False

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

def get_companies(cursor, operators):
    #gets all companies given a set of operators

    sql = "select distinct nm_fantasia from companies where nm_socio in ({seq})".format(
        seq=','.join(['?'] * len(operators)))
    #list of companies
    rows = cursor.execute(sql, operators).fetchall()
    return rows

def reformat(operators):
    l =[]
    for each in operators:
        if isinstance(each, list) or isinstance(each, tuple):
            l.append(each[0])
        else:
            l.append(each)
    return l

def get_operators(cursor, companies):
    #gets all operators given a set of companies

    sql = "select distinct nm_socio from companies where nm_fantasia in ({seq})".format(
        seq=','.join(['?'] * len(companies)))
    # list of operators
    rows = cursor.execute(sql, companies).fetchall()
    return rows

@app.route('/operators')
def func1():
    company = request.args.get('company', '')
    if company == "":
        return 'Must send a company name!', 400

    #get cursor to query db, don't need to worry about closing
    cur = get_db().cursor()
    operators = get_operators(cur, (company,))

    return jsonify({"results": operators})

@app.route('/companies')
def func2():
    operator = request.args.get('company', '')
    if operator == "":
        return 'Must send an operator name!', 400

    # get cursor to query db, don't need to worry about closing
    cur = get_db().cursor()
    companies = get_companies(cur, (operator,))

    return jsonify({"results": companies})

@app.route('/graph')
def func3():
    company = request.args.get('company', '')
    if company == "":
        return 'Must send a company name!', 400

    # get cursor to query db, don't need to worry about closing
    cur = get_db().cursor()
    operators = get_operators(cur, (company,))
    if len(operators) == 0:
        return jsonify({"results": []})

    operators = reformat(operators)
    related_companies = get_companies(cur, operators)

    return jsonify({"results": related_companies})
