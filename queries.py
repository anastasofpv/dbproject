from project import *


def show_all_statues(conn):
    column_names = get_column_names(conn, "ΕΚΘΕΜΑ")
    sql = """ SELECT * FROM ΕΚΘΕΜΑ """
    results = query(conn, sql)
    return column_names, results


def show_all_rooms(conn):
    column_names = get_column_names(conn, "ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ")
    sql = """SELECT * FROM `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`"""
    results = query(conn, sql)
    return column_names, results


def show_all_views(conn):
    column_names = get_column_names(conn, "ΕΠΙΣΚΕΨΗ")
    sql = """ SELECT * FROM ΕΠΙΣΚΕΨΗ """
    results = query(conn, sql)
    return column_names, results


def show_all_exhibitions(conn):
    column_names = get_column_names(conn, "ΕΚΔΗΛΩΣΗ")
    sql = """ SELECT * FROM ΕΚΔΗΛΩΣΗ """
    results = query(conn, sql)
    return column_names, results


def fast_maintenance(conn):
    column_names = (('Ονομα Εκθεματος',), ('Συντηρηση',))
    sql = """select `Ονομα Εκθεματος`, `Συντηρηση`
             from `ΕΚΘΕΜΑ` 
             ORDER BY `Συντηρηση`
             LIMIT 5 """
    results = query(conn, sql)
    return column_names, results


def fast_exhibitions(conn):
    column_names = (('Κατηγορια',), ('Ημ. Εν. Εκδηλωσης',),
                    ('Ημ. Ληξης εκδηλωσης',))
    sql = """ SELECT `Κατηγορια`, `Ημ. Εν. Εκδηλωσης` , `Ημ. Ληξης εκδηλωσης` FROM `ΕΚΔΗΛΩΣΗ` ORDER BY `Ημ. Εν. Εκδηλωσης` LIMIT 3 """
    results = query(conn, sql)
    return column_names, results


def egyptian_statues(conn):
    column_names = (('Ονομα Εκθεματος',), ('Περιγραφη',))
    sql = """ SELECT `ΕΚΘΕΜΑ`.`Ονομα Εκθεματος`, `ΕΚΘΕΜΑ`.`Περιγραφη`
FROM ((`ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ` JOIN `Περιεχει` ON `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας`= `Περιεχει`.`id Αιθουσας`) JOIN `ΕΚΘΕΜΑ` ON `ΕΚΘΕΜΑ`.`id Εκθεματος` = `Περιεχει`.`id Εκθεματος`)
WHERE `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`Ονομα Αιθουσας` LIKE '%ΑΙΓΥΠΤΙΑΚΑ%'"""
    results = query(conn, sql)
    return column_names, results


def rome_season_statues(conn):
    column_names = (('Ονομα Εκθεματος',), ('Περιγραφη',))
    sql = """ SELECT `ΕΚΘΕΜΑ`.`Ονομα Εκθεματος`, `ΕΚΘΕΜΑ`.`Περιγραφη`
FROM ((`ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ` JOIN `Περιεχει` ON `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας`= `Περιεχει`.`id Αιθουσας`) JOIN `ΕΚΘΕΜΑ` ON `ΕΚΘΕΜΑ`.`id Εκθεματος` = `Περιεχει`.`id Εκθεματος`)
WHERE `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`Ονομα Αιθουσας` LIKE '%ΡΩΜΑΙΚΑ%'"""
    results = query(conn, sql)
    return column_names, results


def first_three_rooms(conn):
    column_names = (('Αριθμος Εκθεματων ανα Αιθουσα',), ('Ονομα Αίθουσας',))
    sql = """  SELECT COUNT(`ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας`), `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`Ονομα Αιθουσας`
                FROM ((`ΕΚΘΕΜΑ` JOIN `Περιεχει` ON `ΕΚΘΕΜΑ`.`id Εκθεματος`= `Περιεχει`.`id Εκθεματος`)
	                JOIN `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ` ON `Περιεχει`.`id Αιθουσας`=`ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας`)
                GROUP BY `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας`
                ORDER BY COUNT(`ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας`) DESC
                LIMIT 3  """
    results = query(conn, sql)
    return column_names, results

def next_exhibition(conn):
    
    column_names = (('Τύπος επισκεψης',), ('Κατηγορια',), ('Ονομα Αιθουσας',), ('Ημ. Εν. Εκδηλωσης',), ('Εισητηριο',), ('Πληροφοριες - Κρατησεις',))
    sql = """ SELECT  `ΕΠΙΣΚΕΨΗ`.`Τύπος επισκεψης`,
		              `ΕΚΔΗΛΩΣΗ`.`Κατηγορια`, 
		              `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`Ονομα Αιθουσας`,
                      `ΕΚΔΗΛΩΣΗ`.`Ημ. Εν. Εκδηλωσης`,
                      `ΕΠΙΣΚΕΨΗ`.`Εισητηριο`,
                      `ΕΠΙΣΚΕΨΗ`.`Πληροφοριες - Κρατησεις`        
              FROM ((((`ΕΠΙΣΚΕΨΗ` JOIN `Εχει` ON `ΕΠΙΣΚΕΨΗ`.`id επισκεψης` = `Εχει`.`id επισκεψης`)
                    JOIN `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ` ON `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας` = `Εχει`.`id Αιθουσας`)
                    JOIN `Διοργανωνεται` ON `Διοργανωνεται`.`id Αιθουσας` = `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας`)
                    JOIN `ΕΚΔΗΛΩΣΗ` ON `ΕΚΔΗΛΩΣΗ`.`id Εκδηλωσης` = `Διοργανωνεται`.`id Εκδηλωσης` )
              WHERE `ΕΠΙΣΚΕΨΗ`.`Τύπος επισκεψης` LIKE '%εκδηλωση%'
              ORDER BY `ΕΚΔΗΛΩΣΗ`.`Ημ. Εν. Εκδηλωσης`
              LIMIT 1"""
    
    sql2 = """ SELECT  `ΕΚΔΗΛΩΣΗ`.`Μεγιστος Αρ. Επισκεπτων`       
              FROM ((((`ΕΠΙΣΚΕΨΗ` JOIN `Εχει` ON `ΕΠΙΣΚΕΨΗ`.`id επισκεψης` = `Εχει`.`id επισκεψης`)
                    JOIN `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ` ON `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας` = `Εχει`.`id Αιθουσας`)
                    JOIN `Διοργανωνεται` ON `Διοργανωνεται`.`id Αιθουσας` = `ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ`.`id Αιθουσας`)
                    JOIN `ΕΚΔΗΛΩΣΗ` ON `ΕΚΔΗΛΩΣΗ`.`id Εκδηλωσης` = `Διοργανωνεται`.`id Εκδηλωσης` )
              WHERE `ΕΠΙΣΚΕΨΗ`.`Τύπος επισκεψης` LIKE '%εκδηλωση%'
              ORDER BY `ΕΚΔΗΛΩΣΗ`.`Ημ. Εν. Εκδηλωσης`
              LIMIT 1"""

    results = query(conn, sql)
    results2 = query(conn, sql2)
    try:
        f = open("max_tickets.txt", "w")
        f.write(str(int(results2[0][0])))
    except Exception as e:
        print(e)
    finally:
        f.close()
    return column_names, results



def tickets_used():
    try:
        f = open("max_tickets.txt", "r")
        max_tickets = int(f.readline())
    except Exception as e:
        print(e)
    finally:
        f.close()

    try:
        f1 = open("tickets_used.txt", "r")
        used_tickets = int(f1.readline())
    except Exception as e:
        print(e)
    finally:
        f1.close()

    return (max_tickets - used_tickets)


def increase_tickets(tickets):
    try:
        f1 = open("tickets_used.txt", "r")
        used_tickets = int(f1.readline())
        used_tickets += tickets
    except Exception as e:
        print(e)
    finally:
        f1.close()


    try:
        f = open("tickets_used.txt", "w")
        f.write(str(used_tickets))
    except Exception as e:
        print(e)
    finally:
        f.close()
    

def allowed_tickets(tickets):
    try:
        f1 = open("tickets_used.txt", "r")
        used_tickets = int(f1.readline())
        used_tickets += tickets
    except Exception as e:
        print(e)
    finally:
        f1.close()

    try:
        f = open("max_tickets.txt", "r")
        max_tickets = int(f.readline())
    except Exception as e:
        print(e)
    finally:
        f.close()

    if used_tickets > max_tickets:
        return False
    else:
        return True