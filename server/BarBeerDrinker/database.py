
from sqlalchemy import create_engine
from sqlalchemy import sql

from BarBeerDrinker import config

engine = create_engine(config.database_uri)

#bar function
def get_bars():
	with engine.connect() as con:
		rs = con.execute("SELECT Bar, Casino, City, Address, City, Hours  FROM bars;")
		return [dict(row) for row in rs]

def top_spenders(bar):
	with engine.connect() as con:
		top_spender = sql.text("SELECT p.`Name`, SUBSTRING(b.`Occurred day of week and time`, 3,6) AS time_sold, b.`Occurred month and day` AS month_and_day, b.`total of all ids with tip and tax` AS total FROM bill b, pays p, frequents f WHERE f.`Drinker`=p.`DRINKER` AND p.`BAR`=b.`bar` AND p.bar=:b AND b.transactionID = p.`TRANSACTION ID` GROUP BY b.`total with tip and tax`, p.`DRINKER` ORDER BY b.`total with tip and tax` DESC;")
		rs = con.execute(top_spender, b=bar)
		if rs is None:
			return None
		return [dict(row) for row in rs]

def top_beers(bar):
	with engine.connect() as con:
		top_beer = sql.text("SELECT s.`Consumable`, count(b.`Item`) AS amount_sold, SUBSTRING(b.`Occurred day of week and time`, 3,6)AS time_sold, b.`Occurred month and time` AS month_and_day FROM sells s, bill b WHERE s.`Consumable`=b.`Item` AND s.`Bars`=b.`Bar`AND b.`Bar`=:b GROUP BY b.`Item`, b.`Bar` ORDER BY count(b.`Item`) DESC;")
		rs = con.execute(top_beer, b=bar)
		if rs is None:
			return None
		return [dict(row) for row in rs]

def top_consumables(bar):
	with engine.connect() as con:
		top_consumables=sql.text("SELECT c.`Manufacturer`, count(c.`Consumable`) AS amount_sold, SUBSTRING(b.`Occurred day of week and time`, 3,6) AS time_sold, b.`Occurred month and day` AS month_and_day FROM consumables c, sells s WHERE c.`Consumable` = s.`Consumable` AND s.`Bars`=:b GROUP BY c.`Manufacturer` ORDER BY count(c.`Consumable`) DESC;")
		rs = con.execute(top_consumables, b=bar)
		if rs is None:
                        return None
		return [dict(row) for row in rs]
 
def get_bill():
	with engine.connect() as con:
 		rs = con.execute("SELECT Name, Bar, Item, `Transaction ID`, `Occurred month and day`, `Occurred day of week and time`, tip, subtotal, `total of all ids with tip and tax` FROM bill;")
 		return [dict(row) for row in rs]

def get_consumables():
	with engine.connect() as con:
 		rs = con.execute("SELECT Consumable, Manufacturer, Price FROM consumables;")
 		return [dict(row) for row in rs]

def consumable_sold_most(consumable):
	with engine.connect() as con:
		consumable_sold_most = sql.text("SELECT b.Bar, s.Consumable, count(*) AS consumables_sold, b.`Occurred day of week and time` AS month_and_day, FROM sells s, bill b WHERE s.Consumable=:c  AND b.Bar = s.Bars GROUP BY  b.Bar, s.Consumable ORDER BY count(*) DESC;")
		rs = con.execute(consumable_sold_most, c=consumable)
		if rs is None:
			return None
		return [dict(row) for row in rs]

def drinkers_who_like(consumable):
	with engine.connect() as con:
		drinkers_who_like = sql.text("SELECT DISTINCT l.Person, SUBSTRING(b.`Occurred day of week and time`, 3,6) AS time_transaction_occurred, b.`Occurred month and day` AS month_and_day, count(*) AS amt_drinker_buys FROM likes l, pays p, bill b WHERE l.Person=p.DRINKER  AND l.Consumable=:c AND l.Consumable=b.item GROUP BY  l.Person, SUBSTRING(b.`occurred`, 3,6) ORDER BY SUBSTRING(b.`occurred`, 3,6) ASC;")
		rs = con.execute(drinkers_who_like, c=consumable)
		if rs is None:
			return None
		return [dict(row) for row in rs]

def get_drinker():

	with engine.connect() as con:
                 rs = con.execute("SELECT Name, `Phone Number`, City, Address FROM drinker;")
                 return [dict(row) for row in rs]

def info_on_drinker(drinker):
	with engine.connect() as con:
		transactionID  = sql.text("SELECT p.`Transaction ID`,p.Bar,SUBSTRING(b.`occurred`, 3,6)  AS time_occurred FROM pays p, bill b WHERE b.`transactionID` = p.`Transaction ID` AND p.DRINKER = :d GROUP BY SUBSTRING(b.`occurred`, 3,6), p.BAR, p.`TRANSACTION ID` ORDER BY SUBSTRING(b.`occurred`, 3,6) ASC;")
		rs=con.execute(transactionID, d = drinker) 
		if rs is None:
			return None
		return [dict(row) for row in rs]

def get_frequents():
	with engine.connect() as con:
		rs = con.execute("SELECT Drinker, Bar FROM frequents;")
		return [dict(row) for row in rs]

def get_likes():
	with engine.connect() as con:
		rs = con.execute("SELECT Person, Consumable FROM likes;")
		return [dict(row) for row in rs]


def get_pays():

	with engine.connect() as con:
		rs = con.execute("SELECT BAR, DRINKER, `TRANSACTION ID` FROM pays;")
		return [dict(row) for row in rs]

def get_sells():

	with engine.connect() as con:
		rs = con.execute("SELECT Bars, Consumable, Price FROM sells;")
		return [dict(row) for row in rs]

