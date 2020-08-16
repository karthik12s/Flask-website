from flask import Flask, redirect, url_for,session,request,render_template,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.secret_key='abc'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.permanent_session_lifetime=timedelta(days=1)
db=SQLAlchemy(app)
@app.route("/home")
@app.route("/")
def home():
	if "user" in session:
		return render_template('home.html',n=session["user"])
	return render_template('home.html')

@app.route("/<name>")
def page2(name):
	return (name)

@app.route("/main")
def main():
	return render_template('main.html')
class users(db.Model):
	_id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100))
	password=db.Column(db.String(100))
	def __init__(self,name,password):
		self.name=name
		self.password=password



@app.route("/login",methods=['POST','GET'])
def login():
	if request.method=="POST":
		a1=request.form["n1"]
		a2=request.form['n2']
		f=users.query.filter_by(name=a1).first()
		if f!=None:
			if f.password==a2:
				session["user"]=a1
				session[a1]=a2
				return render_template('profile.html',co1=[a1,a2],se=session)
		return render_template('login.html',er=True)
	else:
		return render_template('login.html')

@app.route("/signup",methods=['POST','GET'])
def signup():
	if "user" in session:
		flash('You are already signed in.Please Logout to Signup')
		return redirect(url_for('home'))
	if request.method=="POST":
			session["user"]=request.form["n3"]
			c=session["user"]
			a=request.form["n4"]
			b=request.form["n5"]
			f=users.query.filter_by(name=c).first()
			if f==None:
				if a==b:
					session[session["user"]]=a
					usr=users(c,a)
					db.session.add(usr)
					db.session.commit()
					return redirect(url_for('login'))
				else:
					return render_template('signup.html',con=True)
			else:
				flash("You already have an account")
				return redirect(url_for('login'))
	return render_template('signup.html')

@app.route("/profile")
def profile():
	if "user" in session:
		return render_template('profile.html',co1=[session["user"],session[session["user"]]],se=session)
	else:
		flash("Kindly login to view your Profie")
		return redirect(url_for('login'))

@app.route("/logout")
def logout():
	if "user" in session:
		session.pop(session["user"],None)
		session.pop("user",None)
		flash("You have been sucessfully logged out")
		return redirect(url_for("login"))
	else:
		flash("Kindly login to logout")
		return redirect(url_for("login"))

if __name__=='__main__':
	db.create_all()
	app.run(debug=True)
