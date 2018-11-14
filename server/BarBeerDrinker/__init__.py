from flask import jsonify, make_response, request, Flask, render_template, url_for
from BarBeerDrinker import database

app = Flask(__name__)

@app.route('/api/drinker')
def get_drinkers():
        return render_template('drinker.html', result=database.get_drinker())

@app.route('/api/drinker/<drinker>')
def info_on_drinker(drinker):
	return render_template('drinker.html', result1=database.info_on_drinker(drinker))


@app.route('/api/bar')
def get_bars():
	return render_template('bar.html', result=database.get_bars())

@app.route('/api/bar/<bar>')
def top_spender(bar):
	return render_template('bar.html', result1=database.top_spenders(bar), result2=database.top_beers(bar), result3=database.top_consumables(bar))

@app.route('/api/consumable')
def get_consumables():
	return render_template('beer.html', result=database.get_consumables())

@app.route('/api/consumable/<consumable>')
def consumables_sold_most(consumable):
	return render_template('beer.html', result1=database.consumable_sold_most(consumable), result2=database.drinkers_who_like(consumable))

@app.route('/')
def hello_world():
	return render_template('home.html')

 
