from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import re
app = Flask(__name__)

app.secret_key = "xyzsdfg"
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootalok",
    database="pythonlogin"
)
db_cursor = db_connection.cursor()
app.config['SESSION_COOKIE_SECURE'] = True
def validate_email(email):
    # Define the regular expression pattern for valid email addresses
    pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com)$'
    return bool(re.match(pattern, email))
@app.route("/")
def index():
    return render_template('portfolio.html')

@app.route('/leave_comment', methods=['POST'])
def leave_comment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        if not validate_email(email):
            flash("Invalid email format. Please use a Gmail or Outlook email address.", "error")
            return render_template('portfolio.html')

        # Check if the email already exists in the database
        db_cursor.execute("SELECT id FROM comments WHERE email = %s", (email,))
        existing_comment = db_cursor.fetchone()

        if existing_comment:
            # If the email exists, update the existing comment
            comment_id = existing_comment[0]
            sql = "UPDATE usercomment SET name = %s, phone = %s, message = %s WHERE id = %s"
            values = (name, phone, message, comment_id)
            flash("Your comment has been updated successfully.", "success")
        else:
            # If the email doesn't exist, insert a new comment
            sql = "INSERT INTO usercomment (name, email, phone, message) VALUES (%s, %s, %s, %s)"
            values = (name, email, phone, message)
            flash("Your comment has been added successfully.", "success")

        db_cursor.execute(sql, values)
        db_connection.commit()

        return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
