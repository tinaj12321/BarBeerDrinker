from flask import jsonify, make_response, request, Flask, render_template, url_for
from BarBeerDrinker import database

app = Flask(__name__)

@app.route('/api/drinker')
def get_drinkers():
        return render_template('drinker.html', result=database.get_drinkers())

@app.route('/api/drinker/<drinker>')
def info_on_drinker(drinker):
	result2=database.beers_ordered_most(drinker)
	r2labels=[r['consumable'] for r in result2]
	r2data=[r['amount_bought'] for r in result2]
	result3=database.spending_of_drinker(drinker)
	r3labels=[r['bar'] for r in result3]
	r3data=[r['total'] for r in result3]
	return render_template('drinker.html', text_title=drinker, result1=database.info_on_drinker(drinker), 
		r2labels=r2labels, r2data=r2data, result2=result2, title1="Most ordered consumables", max1=max(r2data)+10,
		result3=result3, r3labels=r3labels, r3data=r3data, title2="Spending Habits", max3=max(r3data)+10)

@app.route('/api/casinos')
def get_casino():
	return render_template('casino.html', result=database.get_casinos())

@app.route('/api/modify')
def modify():
	return render_template('modification.html')

@app.route('/api/modify/add')
def add():
	return render_template('add.html')

@app.route('/api/modify/add/<table>')
def add_item():
	return render_template('add.html')

@app.route('/api/modify/update')
def update():
	return render_template('update.html')

@app.route('/api/modify/update/<table>')
def update_item():
	return render_template('update.html')

@app.route('/api/modify/delete')
def delete():
	return render_template('delete.html')

@app.route('/api/modify/delete/<table>')
def delete_item(table):
	return render_template('delete.html')

@app.route('/api/casinos/<casino>')
def get_casino_info(casino):
	return render_template('casino.html', text_title=casino, result1=database.get_casino_bars(casino))

@app.route('/api/bar')
def get_bars():
	return render_template('bar.html', result=database.get_bars())

@app.route('/api/bar/<bar>')
def top_spender(bar):
	result1=database.top_spenders(bar)
	r1labels=[r['Name'] for r in result1]
	r1data=[r['total'] for r in result1]
	result2=database.top_beers(bar)
	r2labels=[r['consumable'] for r in result2]
	r2data=[r['amount_sold'] for r in result2]
	result3=database.top_consumables(bar)
	r3labels=[r['Manufacturer'] for r in result3]
	r3data=[r['num_sold'] for r in result3]
	return render_template('bar.html', result1=result1, r1data=r1data, r1labels=r1labels, title1="Top Spenders", max1=max(r1data)+10,
		result2=result2, r2labels=r2labels, r2data=r2data, title2="Top Consumables", max2=max(r2data)+10,
		result3=result3, r3labels=r3labels, r3data=r3data, title3="Top Manufacturers", max3=max(r3data)+10)

@app.route('/api/consumable')
def get_consumables():
	return render_template('beer.html', result=database.get_consumables())

@app.route('/api/consumable/<consumable>')
def consumables_sold_most(consumable):
	return render_template('beer.html', result1=database.consumable_sold_most(consumable), result2=database.drinkers_who_like(consumable))

@app.route('/')
def hello_world():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')
 
