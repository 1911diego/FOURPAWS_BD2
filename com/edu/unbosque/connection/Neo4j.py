from datetime import datetime

from neo4j import GraphDatabase, basic_auth

URL = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "1234"
DATABASE = "fourpaws"

driver = GraphDatabase.driver(URL, auth=basic_auth(USERNAME, PASSWORD))

db = driver.session(database=DATABASE)

summary = db.write_transaction(lambda tx: tx.run("CREATE (:Person:Owner {name: 'Nicolas Avila'})-[:OWNS]->(:Pet:Cat {name: 'Meme'})").consume())
summary.counters.properties_set

db.close()
