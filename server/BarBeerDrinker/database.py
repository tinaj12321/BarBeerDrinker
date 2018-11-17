
from sqlalchemy import create_engine
from sqlalchemy import sql

from BarBeerDrinker import config

engine = create_engine(config.database_uri)
con = engine.connect()

#bar function
def get_bars():
	rs = con.execute("SELECT * FROM Bars;")
	return [dict(row) for row in rs]

def get_casinos():
	rs = con.execute("SELECT DISTINCT Casino, City, Address, City FROM Bars;")
	return [dict(row) for row in rs]

def get_casino_bars(casino):
	get_bars = sql.text("SELECT Bar FROM Bars WHERE Casino=:c;")
	rs = con.execute(get_bars, c=casino)
	return [dict(row) for row in rs]
	
def top_spenders(bar):
	top_spender = sql.text("SELECT p.`Name`,b.total, b.transactionID  FROM Bills b, Pays p WHERE p.bar=b.bar AND p.bar=:b AND b.transactionID = p.transactionID GROUP BY p.`Name` ORDER BY total DESC LIMIT 5;")
	rs = con.execute(top_spender, b=bar)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def top_beers(bar):
	top_beer = sql.text("SELECT b.consumable, count(b.consumable) AS amount_sold FROM Bills b WHERE b.bar=:b GROUP BY b.consumable, b.bar ORDER BY amount_sold DESC LIMIT 5;")
	rs = con.execute(top_beer, b=bar)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def top_consumables(bar):
	top_consumables=sql.text("SELECT Consumables.Manufacturer, count(Bills.consumable) AS num_sold FROM Bills LEFT JOIN Consumables ON Bills.consumable = Consumables.Consumable WHERE Bills.bar =:b GROUP BY Bills.consumable ORDER BY num_sold DESC LIMIT 5;")
	rs = con.execute(top_consumables, b=bar)
	if rs is None:
		return None
	return [dict(row) for row in rs]
 
def get_bill():
	rs = con.execute("SELECT * FROM Bills;")
	return [dict(row) for row in rs]

def get_consumables():
	rs = con.execute("SELECT *  FROM Consumables;")
	return [dict(row) for row in rs]

def consumable_sold_most(consumable):
	consumable_sold_most = sql.text("SELECT bar, count(consumable) AS num_sold FROM Bills WHERE consumable=:c GROUP BY bar ORDER BY num_sold DESC LIMIT 5;")
	rs = con.execute(consumable_sold_most, c=consumable)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def drinkers_who_like(consumable):
	drinkers_who_like = sql.text("SELECT p.`Name`, b.consumable, count(consumable) as num_bought From Pays p LEFT JOIN Bills b ON p.transactionID = b.transactionID WHERE b.consumable=:c GROUP BY p.`Name`, b.consumable ORDER BY num_bought DESC LIMIT 5;")
	rs = con.execute(drinkers_who_like, c=consumable)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def get_drinkers():
	rs = con.execute("SELECT * FROM Drinker;")
	return [dict(row) for row in rs]

def info_on_drinker(drinker):
	transactionID  = sql.text("SELECT b.transactionId, SUBSTRING(b.time_occurred,3,6) AS time_occurred, b.bar FROM Pays p LEFT JOIN Bills b ON p.transactionID = b.transactionID WHERE p.`Name` =:d GROUP BY b.transactionID ORDER BY time_occurred;")
	rs=con.execute(transactionID, d = drinker)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def beers_ordered_most(drinker):
	beers_ordered_most = sql.text("SELECT b.consumable, count(b.consumable) AS amount_bought FROM Pays p LEFT JOIN Bills b ON p.transactionId=b.transactionID WHERE p.Name=:d ORDER BY amount_bought DESC LIMIT 5;")
	rs=con.execute(beers_ordered_most, d = drinker)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def spending_of_drinker(drinker):
	time_dist = sql.text("SELECT b.bar,b.total  FROM Bills b, Pays p WHERE p.bar=b.bar AND p.Name=:d AND b.transactionID = p.transactionID GROUP BY b.bar ORDER BY total DESC;")
	rs=con.execute(time_dist, d = drinker)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def monthly_breakdown(drinker):
	monthly_breakdown = sql.text("SELECT IF((LEFT(b.month_and_day,2) > 10), LEFT(b.month_and_day,2) AS month, CONCAT(' ',CONCAT('0',LEFT(b.month_and_day,2)) AS month), IF((RIGHT(b.month_and_day,2) > 10)), CONCAT(' ',(RIGHT(b.month_and_day,2))) AS day, CONCAT(' ',(CONCAT('0',RIGHT(b.month_and_day,2)))) AS day), CONCAT(2018,(CONCAT(month,day))) AS prelim_string, REPLACE(prelim_string,' ','/') AS date_format, DATEPART(month, date_format) AS formatted_month, b.total FROM Bills b, Pays p WHERE p.bar=b.bar AND p.Name=:d AND b.transactionID = p.transactionID GROUP BY b.bar ORDER BY total DESC;")
	rs=con.execute(monthly_breakdown, d = drinker)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def get_likes():
	rs = con.execute("SELECT * FROM Likes;")
	return [dict(row) for row in rs]

def get_pays():
	rs = con.execute("SELECT * FROM Pays;")
	return [dict(row) for row in rs]

def get_sells():
	rs = con.execute("SELECT * FROM Sells;")
	return [dict(row) for row in rs]
