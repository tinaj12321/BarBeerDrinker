
from sqlalchemy import create_engine
from sqlalchemy import sql

from BarBeerDrinker import config

engine = create_engine(config.database_uri)
con = engine.connect()

#bar function
def queries(a,b,c):
	result=sql.text("SELECT :a FROM :b WHERE :c")
	rs = con.execute(result, a=a,b=b,c=c)
	return [dict(row) for row in rs]


def get_bars_ver():
	rs = con.execute("SELECT * FROM Bars;")
	return [dict(row) for row in rs]
def get_bills_ver():
	rs = con.execute("SELECT * FROM Bills;")
	return [dict(row) for row in rs]
def get_consumables_ver():
	rs = con.execute("SELECT * FROM Consumables;")
	return [dict(row) for row in rs]
def get_frequents_ver():
	rs = con.execute("SELECT * FROM Frequents;")
	return [dict(row) for row in rs]
def get_likes_ver():
	rs = con.execute("SELECT * FROM Likes;")
	return [dict(row) for row in rs]
def get_pays_ver():
	rs = con.execute("SELECT * FROM Pays;")
	return [dict(row) for row in rs]
def get_sells_ver():
	rs = con.execute("SELECT * FROM Sells;")
	return [dict(row) for row in rs]
def get_drinkers_ver():
	rs = con.execute("SELECT * FROM Drinkers;")
	return [dict(row) for row in rs]



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
	top_spender = sql.text("SELECT p.`Name`,b.total, b.transactionID  FROM Bills b, Pays p WHERE p.Bar=b.bar AND p.Bar=:b AND b.transactionID = p.transactionID GROUP BY p.`Name` ORDER BY total DESC LIMIT 5;")
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

def find_bar(bar, casino, address, city, hours):
	find_bar=sql.text("SELECT Bar, Casino, Address, City, Hours FROM Bars WHERE Bar=:b AND Casino=:casino AND Address=:a AND City=:city")
	rs = con.execute(find_bar, b=bar, casino=casino, a=address, city=city, h=hours)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def find_bar_helper(bar):
	find_bar_helper=sql.text("SELECT Bar FROM Bar b WHERE Bar=:b")
	rs = con.execute(find_bar_helper, b=bar)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def find_bill(consumable, transactionID):
	find_bill=sql.text("SELECT consumable, transactionID FROM Bills b WHERE consumable=:c and transactionID=:t")
	rs=con.execute(find_bill, c=consumable, t=transactionID)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def insert_bill(bar, consumable, trans_time, trans_day, transID, subtotal, tip, total):
	insert_bill=sql.text("INSERT INTO Bills (Bar, Consumable, time_occurred, month_and_day, transactionId, subtotal, tip, total) VALUES(:b, :c, :ti, :m, :trans, :sub, :tip, :total);")
	rs=con.execute(insert_bill, b=bar, c=consumable, ti=trans_time, m=trans_day, trans=transID, sub=subtotal, tip=tip, total=total)

def insert_bar(bar, casino, address, city, hours):
	insert_bar=sql.text("INSERT INTO Bars (Bar, Casino, Address, City, Hours) VALUES(:b, :casino, :a, :c, :h);")
	rs=con.execute(insert_bar, b=bar, casino=casino, a=address, c=city, h=hours)

def get_bill():
	rs = con.execute("SELECT * FROM Bills;")
	return [dict(row) for row in rs]

def get_consumables():
	rs = con.execute("SELECT *  FROM Consumables;")
	return [dict(row) for row in rs]

def find_consumable(consumable, manufacturer):
	find_consumable=sql.text("SELECT consumable, manufacturer FROM Consumables WHERE consumable=:c AND manufacturer=:m;")
	rs=con.execute(find_consumable, c=consumable, m=manufacturer)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def find_consumable_helper(consumable):
	find_consumable_helper=sql.text("SELECT consumable FROM Consumables WHERE consumable=:c;")
	rs=con.execute(find_consumable_helper, c=consumable)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def insert_consumable(consumable, manufacturer):
	insert_consumable=sql.text("INSERT INTO Consumables(Consumable, Manufacturer) VALUES(:c, :m);")
	rs=con.execute(insert_consumable, c=consumable, m=manufacturer)

def consumable_sold_most(consumable):
	consumable_sold_most = sql.text("SELECT bar, count(consumable) AS num_sold FROM Bills WHERE consumable=:c GROUP BY bar ORDER BY num_sold DESC LIMIT 5;")
	rs = con.execute(consumable_sold_most, c=consumable)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def drinkers_who_like(consumable):
	drinkers_who_like = sql.text("SELECT p.`Name`, count(consumable) as num_bought From Pays p LEFT JOIN Bills b ON p.transactionID = b.transactionID WHERE b.consumable=:c GROUP BY p.`Name`, b.consumable ORDER BY num_bought DESC LIMIT 5;")
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
	monthly_breakdown = sql.text("SELECT CONCAT(LEFT(b.month_and_day,2), RIGHT(b.month_and_day,2)) AS date_bought, b.total  FROM Bills b, Pays p WHERE p.bar=b.bar AND p.Name=:d AND b.transactionID = p.transactionID GROUP BY b.bar ORDER BY total DESC;")
	rs=con.execute(monthly_breakdown, d = drinker)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def find_drinker(drinker, phone, addr, city):
	find_drinker=sql.text("SELECT `\ufeffName`, `Phone Number`, Address, City FROM Drinker WHERE `\ufeffName`=:n AND `Phone Number`=:p AND Address=:a AND City=:c;")
	rs=con.execute(find_drinker, n=drinker, p=phone, a=addr, c=city)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def find_drinker_helper(drinker):
	find_drinker_helper=sql.text("SELECT `\ufeffName` FROM Drinker WHERE `\ufeffName`=:n;")
	rs=con.execute(find_drinker_helper, n=drinker)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def insert_drinker(drinker,phone,addr,city):
	insert_drinker=sql.text("INSERT INTO Drinker(`\ufeffName`, `Phone Number`, Address, City) VALUES (:n, :p, :a,:c);")
	rs=con.execute(insert_drinker, n=drinker, p=phone, a=addr, c=city)

def get_likes():
	rs = con.execute("SELECT * FROM Likes;")
	return [dict(row) for row in rs]

def find_likes(drinker, consumable):
	find_likes=sql.text("SELECT Person, Consumable FROM Likes WHERE Person=:p AND Consumable=:c;")
	rs=con.execute(find_likes, p=drinker, c=consumable)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def insert_likes(drinker, consumable):
	insert_likes=sql.text("INSERT INTO Likes(Person, Consumable) VALUES :d, :c;")
	rs=con.execute(insert_frequents, d=drinker, c=consumable)

def get_pays():
	rs = con.execute("SELECT * FROM Pays;")
	return [dict(row) for row in rs]

def get_frequents():
	rs = con.execute("SELECT * FROM Frequents;")
	return [dict(row) for row in rs]

def find_pays(transID, drinker, bar):
	find_pays=sql.text("SELECT TransactionId, Name, Bar FROM Pays WHERE TransactionId=:t AND Name=:d AND Bar=:b;")
	rs=con.execute(find_pays,t=transID, d=drinker, b=bar)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def insert_pays(transID, drinker, bar):
	insert_pays=sql.text("INSERT INTO Pays(TransactionId, Name, Bar) VALUES (:t, :n, :b);")
	rs=con.execute(insert_frequents, t=transID, n=drinker, b=bar)

def get_sells():
	rs = con.execute("SELECT * FROM Sells;")
	return [dict(row) for row in rs]

def find_sells(bar, consumable, price):
	find_sells=sql.text("SELECT Bar,Consumable,price WHERE Bar=:b AND Consumable=:c AND price=:p ;")
	rs=con.execute(find_sells, b=bar, c=consumable, p=price)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def insert_sells(bar,consumable,price):
	insert_sells=sql.text("INSERT INTO Sells(Bar,Consumable,price) VALUES(:b, :c, :p);")
	rs=con.execute(insert_sells, b=bar, c=consumable, p=price)

def find_frequents(drinker,bar):
	find_frequents=sql.text("SELECT Drinker, Bar FROM Frequents WHERE Drinker=:d AND Bar=:b;")
	rs=con.execute(find_frequents, d=drinker, b=bar)
	if rs is None:
		return None
	return [dict(row) for row in rs]


def insert_frequents(drinker,bar):
	insert_frequents=sql.text("INSERT INTO Frequents(Drinker, Bar) VALUES(:d, :b);")
	rs=con.execute(insert_frequents, d=drinker, b=bar)

def time_pattern(hours, time_occurred):
	time_pattern=sql.text("SELECT  b1.`Bar`, b2.`Consumable` ,b2.`time_occurred`, b2.`transactionID`, b2.`subtotal`, b2.`total` FROM `Bars` b1, `Bills` b2 WHERE b1.`Bar` = b2.`Bar` AND (SUBSTRING(:t, 3,6) > SUBSTRING((SUBSTRING(:h,((SUBSTRING(:t, 1, 1))*10)-9, 9)) , 1, 4)  OR  SUBSTRING(:t, 3,6)< SUBSTRING((SUBSTRING(:h,((SUBSTRING(:t, 1, 1))*10)-9, 9)) , 5, 9));")
	rs=con.execute(time_pattern, h=hours, t=time_occurred)

def drinker_pattern_likes(drinker, consumable):
	drinker_pattern=sql.text("Select DISTINCT f.`Drinker`, f.`Bar` from `frequents` f , `likes` l, `sells` s where f.`Drinker`=:d and f.`Bar`=s.`Bars` and s.`Consumable`=:c;")
	rs=con.execute(drinker_pattern, d=drinker, c=consumable)
	if rs is None:
		return None
	return [dict(row) for row in rs]

def drinker_pattern_frequents(drinker, bar):
	drinker_pattern=sql.text("Select DISTINCT f.`Drinker`, f.`Bar` from `frequents` f , `likes` l, `sells` s where :d=l.Person and :b=s.`Bars` and s.`Consumable`=l.Consumable;")
	rs=con.execute(drinker_pattern, d=drinker, b=bar)
	if rs is None:
		return None
	return [dict(row) for row in rs]

