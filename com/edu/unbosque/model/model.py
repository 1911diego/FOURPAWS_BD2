from com.edu.unbosque.connection import Neo4j as myModule
from datetime import datetime
db = myModule.db


def crearMascota(nameOwner, namePet, especie):
    summary = db.write_transaction(lambda tx: tx.run(
        "MATCH (d:Person {name: '"+nameOwner+"'}) CREATE (i:Pet:"+especie+" {name: '"+namePet+"'}) CREATE (d)-[:Owns]->(i)").consume())

    summary.counters.properties_set
    db.close()

def validarUser(nameUser):
    result = db.read_transaction(lambda tx:
        tx.run("MATCH (i:Person {name: '"+nameUser+"'}) RETURN i.name AS name").single())
    db.close()
    if result == None:
        print(result)
        return "None";
    else:
        print(result["name"])
        return result["name"]

def validarMascota(namePet):
    result = db.read_transaction(lambda tx:
        tx.run("MATCH (i:Pet {name: '"+namePet+"'}) RETURN i.name AS name").single())
    db.close()
    if result == None:
        print(result)
        return "None";
    else:
        print(result["name"])
        return result["name"]



def crearPersona(nameUser):
    summary = db.write_transaction(lambda tx: tx.run(
        "CREATE (:Person:Owner {name: '" + nameUser + "'})").consume())
    summary.counters.properties_set
    db.close()

def taggearFoto1(namePet, url):
    summary = db.write_transaction(lambda tx: tx.run(
        "MATCH (d:Pet {name: '"+namePet+"'}) CREATE (i:Picture {urlFoto:  '"+url+"'}) CREATE (d)-[:APPEARS_IN]->(i)").consume())
    summary.counters.properties_set
    db.close()

def taggearFoto2(namePet, url):
    summary = db.write_transaction(lambda tx: tx.run(
        "MATCH (d:Picture {urlFoto: '"+url+"'}) MATCH (i:Pet {name: '"+namePet+"'}) CREATE (i)-[:APPEARS_IN]->(d)").consume())
    summary.counters.properties_set
    db.close()

def like(nameUser, url):
    summary = db.write_transaction(lambda tx: tx.run(
        "MATCH (d:Person {name: '"+nameUser+"'}) MATCH (i:Picture {urlFoto: '"+url+"'}) CREATE (d)-[:like]->(i)").consume())
    summary.counters.properties_set
    db.close()

def petUser(nameUser):
    result = db.read_transaction(lambda tx: list(
        tx.run("MATCH (p:Person{name: '"+nameUser+"'})-[r:Owns]->(i:Pet) RETURN i.name AS name")))
    db.close()
    if result == None:
        print(result)
        return "None";
    else:
        print(result["name"])
        return result["name"]


def countLikes():
    result = db.read_transaction(lambda tx: list(
        tx.run("MATCH (p:Person)-[r:like]->(i:Picture) RETURN i.urlFoto AS urlFoto, COUNT(r) AS num_pictures")))
    for r in result:
        print(r["urlFoto"] + " => " + str(r["num_pictures"]))
    db.close()

#crearMascota("Calvo", "A mimir", "Gato")
#crearPersona("Calvoaas")
#taggearFoto1("A mimir", "000000")
#taggearFoto2("Eevee", "https://assets.pokemon.com/assets/cms2/img/pokedex/full/143.png")
like("Calvoaas", "000000")
#countLikes()
#validarUser("Calvo")
#validarMascota("A mimirasf")