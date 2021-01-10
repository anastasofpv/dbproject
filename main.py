from flask import *
from project import *
from queries import *
from school_trip_calculations import *
app = Flask(__name__)
conn = create_connection()

table_name = str()

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('statues') == 'Statues':
            x,y = show_all_statues(conn)
            return render_template("results.html", table_name="ΕΚΘΕΜΑ",columns=x, rows=y) 
        elif  request.form.get('rooms') == 'Rooms':
            x,y = show_all_rooms(conn)
            return render_template("results.html", table_name="ΑΙΘΟΥΣΑ_ΜΟΥΣΕΙΟΥ",columns=x, rows=y)
        elif  request.form.get('views') == 'Views':
            x,y = show_all_views(conn)
            return render_template("results.html", table_name="ΕΠΙΣΚΕΨΗ",columns=x, rows=y)
        elif  request.form.get('exhibitions') == 'Exhibitions':
            x,y = show_all_exhibitions(conn)
            return render_template("results.html", table_name="ΕΚΔΗΛΩΣΗ",columns=x, rows=y)
        elif  request.form.get('immediate maintenance') == 'Immediate Maintenance':
            x,y = fast_maintenance(conn)
            return render_template("results.html", table_name="Προσεχείς Συντηρησεις",columns=x, rows=y)
        elif  request.form.get('immediate exhibitions') == 'Immediate Exhibitions':
            x,y = fast_exhibitions(conn)
            return render_template("results.html", table_name="Προσεχείς Εκδηλώσεις",columns=x, rows=y)
        elif  request.form.get('egyptian statues') == 'Egyptian Statues':
            x,y = egyptian_statues(conn)
            return render_template("results.html", table_name="Αιγυπτιακά Εκθέματα",columns=x, rows=y)
        elif  request.form.get('rome season statues') == 'Rome Season Statues':
            x,y = rome_season_statues(conn)
            return render_template("results.html", table_name="Ρωμαϊκής Εποχής Εκθέματα",columns=x, rows=y)
        elif  request.form.get('first three rooms') == 'First Three Rooms':
            x,y = first_three_rooms(conn)
            return render_template("results.html", table_name="Αιθουσες με τα περισσοτερα εκθεματα",columns=x, rows=y)
        elif  request.form.get('next exhibition') == 'Next Exhibition':
            x,y = next_exhibition(conn)
            return render_template("results2.html", table_name="Επόμενη Εκδήλωση",columns=x, rows=y)
        elif  request.form.get('school trip') == 'School trip':
            return redirect("/school_trip")
        
    
    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")

    return render_template('index.html')


@app.route("/sql", methods=['GET', 'POST'])
def sql():
    global table_name
    if request.method == 'POST':
        try:
            create_table_query = request.form["create"]
            create_table(conn,create_table_query)
            return redirect("/")
        except Exception as e:
            #print(e)
            pass
        try:
            view_query = request.form["view_table"]
            table_name = find_table_name(view_query)
            x = get_column_names(conn, table_name)
            y = query(conn, view_query)
            return render_template("results.html",columns=x,rows=y,table_name=table_name)
        except Exception as e:
            #print(e)
            pass
        
        try:
            table_name = request.form["tables"]
            return render_template("addrec.html", column_names=get_column_names(conn, table_name))
        except Exception as e:
            print(e)


    elif request.method == 'GET':
        print("No Post Back Call")
        return render_template("sql.html",table_names=get_table_names(conn))

    return render_template('sql.html',table_names=get_table_names(conn))


@app.route('/reserve_ticket', methods=['GET', 'POST'])
def reserve_ticket():
    number_of_tickets_left = tickets_used()
    if request.method == 'POST':
        if  request.form.get('next exhibition') == 'Next Exhibition':
            x,y = next_exhibition(conn)
            return render_template("results.html", table_name="Επόμενη Εκδήλωση",columns=x, rows=y)
        try:
            tickets = request.form["number"]
            tickets = int(tickets)
            if not allowed_tickets(tickets):
                return render_template("reserve_ticket.html", number_of_tickets_left=number_of_tickets_left)
            else:
                increase_tickets(tickets)
                return redirect("/")
        except Exception as e:
            print(e) 
    return render_template("reserve_ticket.html", number_of_tickets_left=number_of_tickets_left)


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    global table_name
    if request.method == 'POST':
        data = request.form.to_dict()
        for col_name , value in data.items():
        
            results = query(conn, """SELECT DATA_TYPE 
                                    FROM INFORMATION_SCHEMA.COLUMNS 
                                    WHERE table_name = '{}'
                                    AND COLUMN_NAME = '{}';""".format(table_name,col_name))
            datatype = results[0][0]
            if datatype == "int":
                data[col_name] = int(value)
        results = insert_table(conn,table_name,**data)
        return redirect("/sql")
    return render_template("addrec.html")


@app.route('/school_trip', methods=['GET', 'POST'])
def school_trip():
    if request.method == 'POST':
        if request.form.get('simple school trip') == 'Simple School Trip':
            return redirect("/simple_school_trip") 
        elif  request.form.get('school trip for exhibition') == 'School trip for exhibition':
            return redirect("school_trip_for_exhibition")
    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")
   
    return render_template("school_trip.html")


@app.route('/simple_school_trip', methods=['GET', 'POST'])
def simple_school_trip():
    if request.method == 'POST':
        try:
            number_of_students = request.form["number"]
            number_of_students = int(number_of_students)
            cost = simple_school_trip_calculation(conn, number_of_students)
            cost2 = [(str(cost),)]
            return render_template("results.html",columns=[('cost',)],rows=cost2,table_name="simple cost")
        except Exception as e:
            print(e)
    return render_template("simple_school_trip.html")


@app.route('/school_trip_for_exhibition', methods=['GET', 'POST'])
def school_trip_for_exhibition():
    if request.method == 'POST':
        try:
            number_of_students = request.form["number"]
            number_of_students = int(number_of_students)
            if number_of_students > 50:
                return render_template("school_trip_for_exhibition.html")
            else:
                cost = school_trip_for_exhibition_calculation(conn, number_of_students)
                cost2 = [(str(cost),)]
                return render_template("results.html",columns=[('cost',)],rows=cost2,table_name="simple cost")
        except Exception as e:
            print(e)
    return render_template("school_trip_for_exhibition.html")



if __name__ == '__main__':
    app.run(debug=True)
