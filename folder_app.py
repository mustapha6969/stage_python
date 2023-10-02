from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM Folders")
    data = cur.fetchall()
    cur.close()




    return render_template('index_folders.html', folders=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Folders (name) VALUES (%s)", ((name,),))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Folders WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE Folders
               SET name=%s
               WHERE id=%s
            """, (name, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))



@app.route('/view_files/<int:folder_id>', methods=['GET', 'POST'])
def view():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM Files")
    data = cur.fetchall()
    cur.close()




    return render_template('index_files.html', files=data )





if __name__ == "__main__":
    app.run(debug=True)
