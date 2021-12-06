from com.edu.unbosque.connection import Neo4j as myModule
import uuid
from datetime import datetime
db = myModule.db


def crearMascota(idOwner, idPet, especie):
    id = str(uuid.uuid4())
    summary = db.write_transaction(lambda tx: tx.run(
        "MATCH (d:Person {id: '"+idOwner+"'}) CREATE (i:Pet:"+especie+" {id: '" + id + "', name: '"+idPet+"'}) CREATE (d)-[:Owns]->(i)").consume())

    summary.counters.properties_set
    db.close()

def validarUser(nameUser):
    result = db.read_transaction(lambda tx:
        tx.run("MATCH (i:Person {name: '"+nameUser+"'}) RETURN i.name AS name").single())
    db.close()
    if result == None:
        return "None";
    else:
        return result["name"]

def validarMascota(namePet):
    result = db.read_transaction(lambda tx:
        tx.run("MATCH (i:Pet {name: '"+namePet+"'}) RETURN i.name AS name").single())
    db.close()
    if result == None:
        return "None";
    else:
        return result["name"]



def crearPersona(nameUser, id):
    summary = db.write_transaction(lambda tx: tx.run(
        "CREATE (:Person:Owner {id: '" + id + "', name: '" + nameUser + "'})").consume())
    summary.counters.properties_set
    db.close()

def taggearFoto1(idPet, url):
    id = str(uuid.uuid4())
    summary = db.write_transaction(lambda tx: tx.run(
        "MATCH (d:Pet {name: '"+idPet+"'}) CREATE (i:Picture {id: '" + id + "',urlFoto: '"+url+"'}) CREATE (d)-[:APPEARS_IN]->(i)").consume())
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

def countLikes():
    result = db.read_transaction(lambda tx: list(
        tx.run("MATCH (p:Person)-[r:like]->(i:Picture) RETURN i.urlFoto AS urlFoto, COUNT(r) AS num_pictures ORDER BY num_pictures DESC")))
    db.close()
    return result

def petUser(nameUser):
    result = db.read_transaction(lambda tx: list(
        tx.run("MATCH (p:Person{name: '"+nameUser+"'})-[r:Owns]->(i:Pet) RETURN i.name AS name")))
    db.close()
    if result == None:
        return "None";
    else:
        return result

def fotos():
    result = db.read_transaction(lambda tx: list(
        tx.run("MATCH (n:Picture) RETURN n.urlFoto as foto")))
    db.close()
    if result == None:
        return "None"
    else:
        return result


