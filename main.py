

from flask import Flask,render_template,redirect,url_for,request,session,flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection
from auth import login_required
import re


app=Flask(__name__)

app.secret_key="mysupersecretkey"

#To check in correct format
def is_valid_email(email):
   pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
   return re.match(pattern,email)

#To check if password is strong

def is_strong_password(password):

   if len(password) < 8:
      return False
   
   if not re.search(r"[A-Z]",password):
      return False
   
   if not re.search(r"[a-z]",password):
      return False
   
   if not re.search(r"[0-9]", password):
        return False

   if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
 
   return True



@app.route("/register" , methods=["GET","POST"])
def register():
   if request.method=="POST":
      username = request.form['username']
      email=  request.form['email']
      password = request.form['password']
      confirm_pass=request.form['cpassword']

      
      if not is_valid_email(email):
         flash("Please use valid email format","error")
         return redirect(url_for('register'))
      
      

      if not is_strong_password(password):
       flash(
        "Password must be at least 8 characters and include uppercase, lowercase, number, and special character",
        "error"
    )
      return redirect(url_for("register"))


      if password != confirm_pass:
            # return "Passwords do not match"
            flash("Password doesn't matched","error")
            return redirect(url_for('register'))
      
      
      hashed_password=generate_password_hash(password)
      
      conn=get_connection()
      cursor=conn.cursor(dictionary=True)

      # to check if user exits

      cursor.execute("SELECT id FROM users where email= %s" ,(email,))

      existing_user = cursor.fetchone()

      if existing_user:
         cursor.close()
         conn.close()
         flash("User Already Registered",'error')
         return redirect(url_for('register'))



      #Insert new user Value to Database

      cursor.execute('INSERT INTO users (username , email , password) values (%s , %s, %s)',(username,email,hashed_password))
      
      
      conn.commit()
      cursor.close()
      conn.close()

      return redirect(url_for('login'))   

   

 

   return render_template('register.html')



@app.route("/login" , methods=["GET","POST"])
def login():
   if request.method=="POST":
      email=request.form['email']
      password=request.form['password']

      conn=get_connection()
      cursor=conn.cursor(dictionary=True)

      #to check if user already registered
      cursor.execute("SELECT id , username , password FROM users WHERE email=%s",(email,))
      user =cursor.fetchone()

      cursor.close()
      conn.close()
      
      #if user not registered
      if not user:
         # return "Please Register"
         flash("Please register","error")
         return redirect(url_for('login'))
      
      #if password doesnt match
      if not check_password_hash(user['password'],password):
         # return "Passwod don't matched"
         flash("Incorrect Password","error")
         return redirect(url_for('login'))
      
      #Store data in session
      session["user_id"]=user["id"]
      session["user_name"]=user["username"]

      return redirect(url_for('dashboard'))

   return render_template('login.html')

@app.route("/")
def home():
   return render_template('home.html')

@app.route("/dashboard" , methods=["GET","POST"])
@login_required
def dashboard():
   if request.method=="POST":
      user_note=request.form['user_note']

      # print("User ID & UserName",session['user_id'],session['user_name'])
      # print(user_note)
      conn=get_connection()
      cursor=conn.cursor()

      cursor.execute("INSERT INTO notes (user_id , note_content) values (%s,%s)",(session["user_id"],user_note))
      conn.commit()

      cursor.close()
      conn.close()

      return redirect(url_for('dashboard'))
       
      # Read notes data and store somehwere

   conn=get_connection()
   cursor=conn.cursor(dictionary=True)

   cursor.execute("SELECT id , note_content,created_at FROM notes where user_id=%s ORDER BY created_at DESC",(session['user_id'],))
   usernotes=cursor.fetchall()

   cursor.close()
   conn.close()

   return render_template('dashboard.html',notes=usernotes)

#delete specific note using note_id & user_id

@app.route("/delete_note/<int:note_id>")
@login_required
def delete_note(note_id):

   conn=get_connection()
   cursor=conn.cursor()

   cursor.execute("DELETE FROM notes where id=%s and user_id=%s",(note_id,session['user_id']))

   conn.commit()
   cursor.close()
   conn.close()

   return redirect(url_for('dashboard'))

#Edit specific note using note_id & user_id
@app.route("/edit_note/<int:note_id>",methods=["GET","POST"])
@login_required
def edit_note(note_id):

   conn=get_connection()
   cursor=conn.cursor(dictionary=True)

   if request.method=="POST":
      
      updated_content=request.form['note_content']
      cursor.execute("UPDATE notes SET note_content=%s WHERE id=%s and user_id=%s",(updated_content,note_id,session['user_id']))
      
      conn.commit()
      cursor.close()
      conn.close()

      return redirect(url_for("dashboard"))


   #Read updated data

   cursor.execute("SELECT id ,note_content FROM notes WHERE id=%s AND user_id=%s",(note_id,session['user_id']))
   note=cursor.fetchone()
   cursor.close()
   conn.close()

   if not note:
        # Note not found or doesn't belong to user
        return "Note not found or access denied"


   
   return render_template('edit_note.html',note=note)


@app.route("/logout")
def logout():
   session.clear()
   return redirect(url_for('login'))



if __name__ == '__main__':
   app.run(debug=True)

