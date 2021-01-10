from project import *

def simple_school_trip_calculation(conn, number_of_students):
    sql = """ SELECT `ΕΠΙΣΚΕΨΗ`.`Εισητηριο` 
              FROM `ΕΠΙΣΚΕΨΗ` 
              WHERE `ΕΠΙΣΚΕΨΗ`.`Τύπος επισκεψης` LIKE '%Σχολικη%'  """

    results = query(conn, sql)
    ticket = (int(results[0][0]))
    return ticket * number_of_students


def school_trip_for_exhibition_calculation(conn, number_of_students):
    sql = """ SELECT `ΕΠΙΣΚΕΨΗ`.`Εισητηριο` 
              FROM `ΕΠΙΣΚΕΨΗ` 
              WHERE `ΕΠΙΣΚΕΨΗ`.`Τύπος επισκεψης` LIKE '%Σχολικη%'  """

    results = query(conn, sql)
    ticket = 2 * (int(results[0][0]))
    return ticket * number_of_students