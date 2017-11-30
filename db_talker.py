import MySQLdb
import config as cnf

def db():
    return MySQLdb.connect(cnf.db_host, cnf.db_user, cnf.db_pw, cnf.db_name)

def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

def exec_sql(statement, args=()):
    database = db()
    cur = database.cursor()
    cur.execute(statement, args)
    database.commit()
    cur.connection.close()

def insert_item(table, **items):
    columns = "("
    values = "("
    a = 1
    for i in items:
        value = items.get(i)
        try:
            value = value.decode(encoding="utf-8", errors="strict")
        except AttributeError:
            pass
        columns += i
        values += "'"
        values += str(value)
        values += "'"
        if a == len(items):
            values += ")"
            columns += ")"
        else:
            values += ","
            columns += ","
        a += 1
    insert_statement = "INSERT into " + table.upper() + " " + columns + " values " + values
    exec_sql(insert_statement)

def remove_item(table, **conditions):
    s = "DELETE FROM " + table + " WHERE "
    cons = ""
    a = 1
    for c in conditions:
        value = conditions.get(c)
        try:
            value = value.decode(encoding="utf-8", errors="strict")
        except AttributeError:
            pass
        cons += c + " = '" + value + "'"
        if a < len(conditions):
            cons += " AND "
        a += 1
    s += cons
    exec_sql(s)