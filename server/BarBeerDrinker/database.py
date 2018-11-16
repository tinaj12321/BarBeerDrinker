
from sqlalchemy import create_engine
from sqlalchemy import sql

from BarBeerDrinker import config

engine = create_engine(config.database_uri)

#bar function
def get_bars():
	with engine.connect() as con:
		rs = con.execute("SELECT * FROM Bars;")
		return [dict(row) for row in rs]

def get_casinos():
        with engine.connect() as con:
                rs = con.execute("SELECT DISTINCT Casino, City, Address, City FROM Bars;")
                return [dict(row) for row in rs]

def top_spenders(bar):
	with engine.connect() as con:
            top_spender = sql.text("SELECT p.`Name`,b.total, b.transactionID  FROM Bills b, Pays p WHERE p.bar=b.bar AND p.bar=:b AND b.transactionID = p.transactionID GROUP BY p.`Name` ORDER BY total DESC LIMIT 5;")
		rs = con.execute(top_spender, b=bar)
		if rs is None:
			return None
		return [dict(row) for row in rs]

def top_beers(bar):
	with engine.connect() as con:
            top_beer = sql.text("SELECT b.`consumable`, count(b.`consumable`) AS amount_sold FROM Bills b WHERE b.`Bar`=:b GROUP BY b.`consumable`, b.`bar` ORDER BY count(b.`consumable`) DESC LIMIT 5;;")
            rs = con.execute(top_beer, b=bar)
            if rs is None:
		    return None
            return [dict(row) for row in rs]

def top_consumables(bar):
	with engine.connect() as con:
            top_consumables=sql.text("SELECT Consumables.Manufacturer, count(Bills.consumable) AS num_sold FROM Bills LEFT JOIN Consumables ON Bills.consumable = Consumables.Consumable WHERE Bills.bar =:b GROUP BY Bills.consumable ORDER BY num_sold DESC LIMIT 5;")
            rs = con.execute(top_consumables, b=bar)
            if rs is None:
                return None
            return [dict(row) for row in rs]
 
def get_bill():
	with engine.connect() as con:
 		rs = con.execute("SELECT * FROM Bills;")
 		return [dict(row) for row in rs]

def get_consumables():
	with engine.connect() as con:
 		rs = con.execute("SELECT *  FROM Consumables;")
 		return [dict(row) for row in rs]

def consumable_sold_most(consumable):
	with engine.connect() as con:
            consumable_sold_most = sql.text("SELECT bar, count(consumable) FROM Bills WHERE consumable=:c GROUP BY bar ORDER BY count(consumable) DESC LIMIT 5SELECT bar, count(consumable) FROM Bills WHERE consumable=:c GROUP BY bar ORDER BY count(consumable) DESC LIMIT 5;")
		rs = con.execute(consumable_sold_most, c=consumable)
		if rs is None:
			return None
		return [dict(row) for row in rs]

def drinkers_who_like(consumable):
	with engine.connect() as con:
            drinkers_who_like = sql.text("SELECT p.`Name`, b.consumable, count(consumable) as num_bought From Pays p LEFT JOIN Bills b ON p.transactionID = b.transactionID WHERE b.consumable=:c GROUP BY p.`Name`, b.consumable ORDER BY num_bought DESC LIMIT 5;")
		rs = con.execute(drinkers_who_like, c=consumable)
		if rs is None:
			return None
		return [dict(row) for row in rs]

def get_drinkers():

	with engine.connect() as con:
                 rs = con.execute("SELECT * FROM Drinker;")
                 return [dict(row) for row in rs]

def info_on_drinker(drinker):
	with engine.connect() as con:
            transactionID  = sql.text("SELECT b.transactionId, SUBSTRING(b.time_occurred,3,6) AS time_occurred, b.bar FROM Pays p LEFT JOIN Bills b ON p.transactionID = b.transactionID WHERE p.`Name` =:d GROUP BY b.transactionID ORDER BY time_occurred;")
		rs=con.execute(transactionID, d = drinker) 
		if rs is None:
			return None
		return [dict(row) for row in rs]

def get_frequents():
	with engine.connect() as con:
		rs = con.execute("SELECT * FROM Frequents;")
		return [dict(row) for row in rs]

def get_likes():
	with engine.connect() as con:
		rs = con.execute("SELECT * FROM Likes;")
		return [dict(row) for row in rs]


def get_pays():

	with engine.connect() as con:
		rs = con.execute("SELECT * FROM Pays;")
		return [dict(row) for row in rs]

def get_sells():

	with engine.connect() as con:
		rs = con.execute("SELECT * FROM Sells;")
		return [dict(row) for row in rs]

