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

@app.route("/bar_plot",methods=["POST","GET"])
def bar_plot():    #Function to create the base plot, make sure to make global the lines, axes, canvas and any part that you would want to update later
	if request.method=="POST":
		a1=request.form['c1']
		b1=request.form['c2']
		lab=[]
		val=[]
		val_p=[]
		if a1 in pop:
			lab.append(a1)
			val.append(pop[a1])
		if b1 in pop:
			lab.append(b1)
			val.append(pop[b1])
		if a1 in pro:
			val_p.append(pro[a1])
		if b1 in pro:
			val_p.append(pro[b1])
		if len(lab)<2 or len(val)<2:
			flash('Please select a country')
			return(render_template('bar_plot.html',l1=li))
		return render_template('bar_plot.html',labels=lab,values=val,max_po=max(val)+1000,max_pr=max(val_p)+0.2,values_p=val_p,a=a1,b=b1,l1=li,h1='Population',h2='Protiens',ch='Population Worldwide')
	else:
		return render_template('bar_plot.html',l1=li)


@app.route('/line',methods=["GET","POST"])
def line():
	if request.method=="POST":
		a=request.form['s1']
		if a in states:
			labels=list(states[a].keys())
			values=list(states[a].values())
			return render_template('line_graph.html', title='State Plots', max=max(values)+1000, labels=labels, values=values,l1=s_names,a=a)
		flash('Select a State')
		return render_template('line_graph.html',l1=s_names)
	else:
		return render_template('line_graph.html',l1=s_names)
@app.route("/tab")
def tab():
	return pop.to_html()

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
	dob=db.Column(db.String(100))
	email=db.Column(db.String(100))
	country=db.Column(db.String(100))
	def __init__(self,name,password,dob=None,email=None,country=None):
		self.name=name
		self.password=password
		self.dob=dob
		self.email=email
		self.country=country

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
				return render_template('profile.html',co1=users.query.filter_by(name=session["user"]).first(),se=session)
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
		return render_template('profile.html',co1=users.query.filter_by(name=session["user"]).first())
	else:
		flash("Kindly login to view your Profie")
		return redirect(url_for('login'))
@app.route("/update",methods=["POST","GET"])
def update():
	if request.method=="POST":
		if "user" in session:
			f=users.query.filter_by(name=session["user"]).first()
			d=request.form['do']
			e=request.form['em']
			co=request.form['co']
			f.dob=d
			f.email=e
			f.country=co
			db.session.commit()
			flash("Profile has been Updated Successfully")
			return redirect(url_for('profile'))
	return render_template('update.html',co1=users.query.filter_by(name=session["user"]).first(),l1=li)

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
li=['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bolivia (Plurinational State of)', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'China, Hong Kong SAR', 'China, Macao SAR', 'China, mainland', 'China, Taiwan Province of', 'Colombia', 'Congo', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', "Democratic People's Republic of Korea", 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Republic of Korea', 'Republic of Moldova', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovakia', 'Slovenia', 'Solomon Islands', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom of Great Britain and Northern Ireland', 'United Republic of Tanzania', 'United States of America', 'Uruguay', 'Vanuatu', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe']
pop={
		"Afghanistan":36296.11,
		"Albania":2884.17,
		"Algeria":41389.19,
		"Angola":29816.77,
		"Antigua and Barbuda":95.43,
		"Argentina":43937.14,
		"Armenia":2944.79,
		"Australia":24584.62,
		"Austria":8819.9,
		"Azerbaijan":9845.32,
		"Bahamas":381.75,
		"Bangladesh":159685.42,
		"Barbados":286.23,
		"Belarus":9450.23,
		"Belgium":11419.75,
		"Belize":375.77,
		"Benin":11175.2,
		"Bolivia (Plurinational State of)":11192.85,
		"Bosnia and Herzegovina":3351.53,
		"Botswana":2205.08,
		"Brazil":207833.82,
		"Bulgaria":7102.44,
		"Burkina Faso":19193.23,
		"Cabo Verde":537.5,
		"Cambodia":16009.41,
		"Cameroon":24566.07,
		"Canada":36732.1,
		"Central African Republic":4596.02,
		"Chad":15016.75,
		"Chile":18470.44,
		"China":1452625.24,
		"China, Hong Kong SAR":7306.32,
		"China, Macao SAR":622.59,
		"China, mainland":1421021.79,
		"China, Taiwan Province of":23674.55,
		"Colombia":48909.84,
		"Congo":5110.69,
		"Costa Rica":4949.95,
		"C�te d'Ivoire":24437.47,
		"Croatia":4182.86,
		"Cuba":11339.25,
		"Cyprus":1179.68,
		"Czechia":10641.03,
		"Democratic People's Republic of Korea":25429.83,
		"Denmark":5732.27,
		"Djibouti":944.1,
		"Dominica":71.46,
		"Dominican Republic":10513.1,
		"Ecuador":16785.36,
		"Egypt":96442.59,
		"El Salvador":6388.13,
		"Estonia":1319.39,
		"Eswatini":1124.81,
		"Ethiopia":106399.92,
		"Fiji":877.46,
		"Finland":5511.37,
		"France":64842.51,
		"French Polynesia":276.1,
		"Gabon":2064.82,
		"Gambia":2213.89,
		"Georgia":4008.72,
		"Germany":82658.41,
		"Ghana":29121.47,
		"Greece":10569.45,
		"Grenada":110.87,
		"Guatemala":16914.97,
		"Guinea":12067.52,
		"Guinea-Bissau":1828.14,
		"Guyana":775.22,
		"Haiti":10982.37,
		"Honduras":9429.01,
		"Hungary":9729.82,
		"Iceland":334.39,
		"India":1338676.78,
		"Indonesia":264650.96,
		"Iran (Islamic Republic of)":80673.88,
		"Iraq":37552.78,
		"Ireland":4753.28,
		"Israel":8243.85,
		"Italy":60673.7,
		"Jamaica":2920.85,
		"Japan":127502.73,
		"Jordan":9785.84,
		"Kazakhstan":18080.02,
		"Kenya":50221.14,
		"Kiribati":114.16,
		"Kuwait":4056.1,
		"Kyrgyzstan":6189.73,
		"Latvia":1951.1,
		"Lebanon":6819.37,
		"Lesotho":2091.53,
		"Liberia":4702.23,
		"Lithuania":2845.41,
		"Luxembourg":591.91,
		"Madagascar":25570.51,
		"Malawi":17670.2,
		"Malaysia":31104.65,
		"Maldives":496.4,
		"Mali":18512.43,
		"Malta":437.93,
		"Mauritania":4282.57,
		"Mauritius":1264.5,
		"Mexico":124777.32,
		"Mongolia":3113.79,
		"Montenegro":627.56,
		"Morocco":35581.25,
		"Mozambique":28649.02,
		"Myanmar":53382.52,
		"Namibia":2402.63,
		"Nepal":27632.68,
		"Netherlands":17021.35,
		"New Caledonia":277.15,
		"New Zealand":4702.03,
		"Nicaragua":6384.85,
		"Niger":21602.38,
		"Nigeria":190873.24,
		"North Macedonia":2082.0,
		"Norway":5296.33,
		"Oman":4665.93,
		"Pakistan":207906.21,
		"Panama":4106.77,
		"Paraguay":6867.06,
		"Peru":31444.3,
		"Philippines":105172.93,
		"Poland":37953.18,
		"Portugal":10288.53,
		"Republic of Korea":51096.42,
		"Republic of Moldova":4059.68,
		"Romania":19653.97,
		"Russian Federation":145530.08,
		"Rwanda":11980.96,
		"Saint Kitts and Nevis":52.05,
		"Saint Lucia":180.95,
		"Saint Vincent and the Grenadines":109.83,
		"Samoa":195.35,
		"Sao Tome and Principe":207.09,
		"Saudi Arabia":33101.18,
		"Senegal":15419.35,
		"Serbia":8829.63,
		"Sierra Leone":7488.42,
		"Slovakia":5447.9,
		"Slovenia":2076.39,
		"Solomon Islands":636.04,
		"South Africa":57009.76,
		"Spain":46647.43,
		"Sri Lanka":21128.03,
		"Sudan":40813.4,
		"Suriname":570.5,
		"Sweden":9904.9,
		"Switzerland":8455.8,
		"Tajikistan":8880.27,
		"Thailand":69209.81,
		"Timor-Leste":1243.26,
		"Togo":7698.47,
		"Trinidad and Tobago":1384.06,
		"Tunisia":11433.44,
		"Turkey":81116.45,
		"Turkmenistan":5757.67,
		"Uganda":41166.59,
		"Ukraine":44487.71,
		"United Arab Emirates":9487.2,
		"United Kingdom of Great Britain and Northern Ireland":66727.46,
		"United Republic of Tanzania":54660.34,
		"United States of America":325084.76,
		"Uruguay":3436.64,
		"Vanuatu":285.51,
		"Venezuela (Bolivarian Republic of)":29402.48,
		"Viet Nam":94600.65,
		"Yemen":27834.82,
		"Zambia":16853.6,
		"Zimbabwe":14236.59,
}
pro={
		"Afghanistan":0.44,
		"Albania":4.32,
		"Algeria":2.4,
		"Angola":0.19,
		"Antigua and Barbuda":0.79,
		"Argentina":4.23,
		"Armenia":3.42,
		"Australia":2.36,
		"Austria":4.64,
		"Azerbaijan":2.6,
		"Bahamas":2.06,
		"Bangladesh":0.87,
		"Barbados":2.59,
		"Belarus":4.31,
		"Belgium":3.98,
		"Belize":1.26,
		"Benin":0.29,
		"Bolivia (Plurinational State of)":2.0,
		"Bosnia and Herzegovina":1.5,
		"Botswana":0.43,
		"Brazil":2.15,
		"Bulgaria":2.68,
		"Burkina Faso":0.68,
		"Cabo Verde":1.39,
		"Cambodia":0.39,
		"Cameroon":0.1,
		"Canada":4.16,
		"Central African Republic":0.14,
		"Chad":0.1,
		"Chile":2.86,
		"China":7.13,
		"China, Hong Kong SAR":5.86,
		"China, Macao SAR":5.34,
		"China, mainland":7.19,
		"China, Taiwan Province of":4.13,
		"Colombia":3.47,
		"Congo":0.16,
		"Costa Rica":2.88,
		"C�te d'Ivoire":0.58,
		"Croatia":2.36,
		"Cuba":2.44,
		"Cyprus":2.36,
		"Czechia":2.56,
		"Democratic People's Republic of Korea":1.45,
		"Denmark":5.23,
		"Djibouti":0.32,
		"Dominica":0.67,
		"Dominican Republic":2.76,
		"Ecuador":2.11,
		"Egypt":1.01,
		"El Salvador":2.38,
		"Estonia":3.67,
		"Eswatini":0.5,
		"Ethiopia":0.13,
		"Fiji":1.24,
		"Finland":2.74,
		"France":3.59,
		"French Polynesia":2.3,
		"Gabon":0.27,
		"Gambia":0.41,
		"Georgia":1.79,
		"Germany":3.56,
		"Ghana":0.34,
		"Greece":2.68,
		"Grenada":2.63,
		"Guatemala":3.66,
		"Guinea":0.53,
		"Guinea-Bissau":0.24,
		"Guyana":0.51,
		"Haiti":0.13,
		"Honduras":1.18,
		"Hungary":4.23,
		"Iceland":3.43,
		"India":0.95,
		"Indonesia":1.76,
		"Iran (Islamic Republic of)":2.17,
		"Iraq":2.77,
		"Ireland":2.97,
		"Israel":3.13,
		"Italy":3.67,
		"Jamaica":0.57,
		"Japan":6.18,
		"Jordan":1.0,
		"Kazakhstan":2.53,
		"Kenya":0.38,
		"Kiribati":0.6,
		"Kuwait":5.37,
		"Kyrgyzstan":1.27,
		"Lao People's Democratic Republic":0.56,
		"Latvia":3.66,
		"Lebanon":0.62,
		"Lesotho":0.27,
		"Liberia":0.35,
		"Lithuania":4.42,
		"Luxembourg":4.91,
		"Madagascar":0.19,
		"Malawi":0.32,
		"Malaysia":5.64,
		"Maldives":3.45,
		"Mali":0.2,
		"Malta":3.74,
		"Mauritania":0.72,
		"Mauritius":1.82,
		"Mexico":5.34,
		"Mongolia":1.28,
		"Montenegro":3.53,
		"Morocco":1.94,
		"Mozambique":0.56,
		"Myanmar":1.59,
		"Namibia":0.4,
		"Nepal":0.58,
		"Netherlands":4.41,
		"New Caledonia":2.8,
		"New Zealand":3.05,
		"Nicaragua":1.48,
		"Niger":0.07,
		"Nigeria":0.71,
		"North Macedonia":1.65,
		"Norway":3.62,
		"Oman":2.41,
		"Pakistan":0.99,
		"Panama":1.64,
		"Paraguay":3.29,
		"Peru":2.43,
		"Philippines":1.28,
		"Poland":2.11,
		"Portugal":2.67,
		"Republic of Korea":3.24,
		"Republic of Moldova":2.33,
		"Romania":4.47,
		"Russian Federation":4.7,
		"Rwanda":0.11,
		"Saint Kitts and Nevis":1.2,
		"Saint Lucia":1.0,
		"Saint Vincent and the Grenadines":1.32,
		"Samoa":0.69,
		"Sao Tome and Principe":0.2,
		"Saudi Arabia":1.96,
		"Senegal":0.47,
		"Serbia":2.78,
		"Sierra Leone":0.4,
		"Slovakia":3.87,
		"Slovenia":2.97,
		"Solomon Islands":0.34,
		"South Africa":2.07,
		"Spain":4.31,
		"Sri Lanka":1.31,
		"Sudan":0.35,
		"Suriname":1.71,
		"Sweden":4.26,
		"Switzerland":3.2,
		"Tajikistan":0.72,
		"Thailand":3.89,
		"Timor-Leste":0.25,
		"Togo":0.27,
		"Trinidad and Tobago":1.26,
		"Tunisia":2.25,
		"Turkey":2.34,
		"Turkmenistan":2.08,
		"Uganda":0.25,
		"Ukraine":4.23,
		"United Arab Emirates":2.21,
		"United Kingdom of Great Britain and Northern Ireland":3.48,
		"United Republic of Tanzania":0.1,
		"United States of America":4.56,
		"Uruguay":3.24,
		"Uzbekistan":1.93,
		"Vanuatu":0.78,
		"Venezuela (Bolivarian Republic of)":0.98,
		"Viet Nam":1.38,
		"Yemen":0.46,
}
states={
 "Andaman And Nicobar":{
		"01-Mar-20":2,
		"15-Mar-20":6,
		"01-Apr-20":16,
		"15-Apr-20":17,
		"01-May-20":39,
		"15-May-20":39,
		"01-Jun-20":39,
		"15-Jun-20":47,
		"01-Jul-20":115,
		"15-Jul-20":186,
		"01-Aug-20":550,
		"15-Aug-20":2188
},
 "Andhra Pradesh":{
		"01-Mar-20":0,
		"15-Mar-20":100,
		"01-Apr-20":210,
		"15-Apr-20":624,
		"01-May-20":1562,
		"15-May-20":2406,
		"01-Jun-20":3775,
		"15-Jun-20":6555,
		"01-Jul-20":16196,
		"15-Jul-20":38143,
		"01-Aug-20":143634,
		"15-Aug-20":275786
},
 "Arunachal Pradesh":{
		"01-Mar-20":0,
		"15-Mar-20":6,
		"01-Apr-20":6,
		"15-Apr-20":7,
		"01-May-20":7,
		"15-May-20":7,
		"01-Jun-20":28,
		"15-Jun-20":101,
		"01-Jul-20":238,
		"15-Jul-20":549,
		"01-Aug-20":1663,
		"15-Aug-20":2679
},
 "Assam":{
		"01-Mar-20":0,
		"15-Mar-20":14,
		"01-Apr-20":30,
		"15-Apr-20":47,
		"01-May-20":57,
		"15-May-20":104,
		"01-Jun-20":1500,
		"15-Jun-20":4324,
		"01-Jul-20":9346,
		"15-Jul-20":20558,
		"01-Aug-20":41399,
		"15-Aug-20":75631
},
 "Bihar":{
		"01-Mar-20":0,
		"15-Mar-20":349,
		"01-Apr-20":373,
		"15-Apr-20":421,
		"01-May-20":815,
		"15-May-20":1382,
		"01-Jun-20":4294,
		"15-Jun-20":7011,
		"01-Jul-20":11031,
		"15-Jul-20":21907,
		"01-Aug-20":53078,
		"15-Aug-20":100461
},
 "Chandigarh":{
		"01-Mar-20":0,
		"15-Mar-20":18,
		"01-Apr-20":35,
		"15-Apr-20":39,
		"01-May-20":106,
		"15-May-20":209,
		"01-Jun-20":315,
		"15-Jun-20":375,
		"01-Jul-20":468,
		"15-Jul-20":653,
		"01-Aug-20":1094,
		"15-Aug-20":1971
},
 "Chattisgarh":{
		"01-Mar-20":0,
		"15-Mar-20":41,
		"01-Apr-20":50,
		"15-Apr-20":74,
		"01-May-20":84,
		"15-May-20":107,
		"01-Jun-20":588,
		"15-Jun-20":1756,
		"01-Jul-20":3054,
		"15-Jul-20":4795,
		"01-Aug-20":9482,
		"15-Aug-20":14849
},
 "Daman & Diu":{
		"01-Mar-20":0,
		"15-Mar-20":0,
		"01-Apr-20":0,
		"15-Apr-20":0,
		"01-May-20":0,
		"15-May-20":0,
		"01-Jun-20":0,
		"15-Jun-20":0,
		"01-Jul-20":0,
		"15-Jul-20":0,
		"01-Aug-20":0,
		"15-Aug-20":0
},
 "Delhi":{
		"01-Mar-20":0,
		"15-Mar-20":180,
		"01-Apr-20":325,
		"15-Apr-20":1751,
		"01-May-20":3911,
		"15-May-20":9068,
		"01-Jun-20":21007,
		"15-Jun-20":43002,
		"01-Jul-20":92348,
		"15-Jul-20":118818,
		"01-Aug-20":137233,
		"15-Aug-20":152287
},
 "Dardar and Nagar Haveli":{
		"01-Mar-20":0,
		"15-Mar-20":2,
		"01-Apr-20":2,
		"15-Apr-20":2,
		"01-May-20":2,
		"15-May-20":3,
		"01-Jun-20":5,
		"15-Jun-20":41,
		"01-Jul-20":258,
		"15-Jul-20":580,
		"01-Aug-20":1185,
		"15-Aug-20":1818
},
 "Goa":{
		"01-Mar-20":0,
		"15-Mar-20":54,
		"01-Apr-20":59,
		"15-Apr-20":61,
		"01-May-20":61,
		"15-May-20":69,
		"01-Jun-20":127,
		"15-Jun-20":646,
		"01-Jul-20":1536,
		"15-Jul-20":3162,
		"01-Aug-20":6163,
		"15-Aug-20":11220
},
 "Gujarath":{
		"01-Mar-20":0,
		"15-Mar-20":634,
		"01-Apr-20":721,
		"15-Apr-20":1400,
		"01-May-20":5355,
		"15-May-20":10566,
		"01-Jun-20":17851,
		"15-Jun-20":24738,
		"01-Jul-20":34633,
		"15-Jul-20":46201,
		"01-Aug-20":63021,
		"15-Aug-20":78152
},
 "Himachal Pradesh":{
		"01-Mar-20":0,
		"15-Mar-20":27,
		"01-Apr-20":30,
		"15-Apr-20":62,
		"01-May-20":67,
		"15-May-20":103,
		"01-Jun-20":367,
		"15-Jun-20":583,
		"01-Jul-20":1041,
		"15-Jul-20":1404,
		"01-Aug-20":2631,
		"15-Aug-20":3941
},
 "Haryana":{
		"01-Mar-20":0,
		"15-Mar-20":248,
		"01-Apr-20":277,
		"15-Apr-20":438,
		"01-May-20":591,
		"15-May-20":1088,
		"01-Jun-20":2590,
		"15-Jun-20":7956,
		"01-Jul-20":15743,
		"15-Jul-20":24236,
		"01-Aug-20":35994,
		"15-Aug-20":46643
},
 "Jarkhand":{
		"01-Mar-20":0,
		"15-Mar-20":3,
		"01-Apr-20":4,
		"15-Apr-20":31,
		"01-May-20":116,
		"15-May-20":214,
		"01-Jun-20":664,
		"15-Jun-20":1796,
		"01-Jul-20":2588,
		"15-Jul-20":4786,
		"01-Aug-20":11630,
		"15-Aug-20":22441
},
 "Jammu And Kashmir":{
		"01-Mar-20":0,
		"15-Mar-20":139,
		"01-Apr-20":199,
		"15-Apr-20":437,
		"01-May-20":776,
		"15-May-20":1150,
		"01-Jun-20":2738,
		"15-Jun-20":5357,
		"01-Jul-20":7986,
		"15-Jul-20":12293,
		"01-Aug-20":21097,
		"15-Aug-20":28227
},
 "Karnataka":{
		"01-Mar-20":0,
		"15-Mar-20":474,
		"01-Apr-20":578,
		"15-Apr-20":747,
		"01-May-20":1057,
		"15-May-20":1524,
		"01-Jun-20":3876,
		"15-Jun-20":7681,
		"01-Jul-20":18484,
		"15-Jul-20":51890,
		"01-Aug-20":128276,
		"15-Aug-20":215269
},
 "Kerala":{
		"01-Mar-20":0,
		"15-Mar-20":732,
		"01-Apr-20":973,
		"15-Apr-20":1096,
		"01-May-20":1206,
		"15-May-20":1285,
		"01-Jun-20":2035,
		"15-Jun-20":3252,
		"01-Jul-20":5462,
		"15-Jul-20":10984,
		"01-Aug-20":25113,
		"15-Aug-20":42776
},
 "Ladakh":{
		"01-Mar-20":0,
		"15-Mar-20":42,
		"01-Apr-20":55,
		"15-Apr-20":60,
		"01-May-20":64,
		"15-May-20":85,
		"01-Jun-20":119,
		"15-Jun-20":597,
		"01-Jul-20":1033,
		"15-Jul-20":1189,
		"01-Aug-20":1450,
		"15-Aug-20":1925
},
 "Lakshwadeep":{
		"01-Mar-20":0,
		"15-Mar-20":0,
		"01-Apr-20":0,
		"15-Apr-20":0,
		"01-May-20":0,
		"15-May-20":0,
		"01-Jun-20":0,
		"15-Jun-20":0,
		"01-Jul-20":0,
		"15-Jul-20":0,
		"01-Aug-20":0,
		"15-Aug-20":0
},
 "Maharashtra":{
		"01-Mar-20":0,
		"15-Mar-20":612,
		"01-Apr-20":915,
		"15-Apr-20":3496,
		"01-May-20":12086,
		"15-May-20":29680,
		"01-Jun-20":70593,
		"15-Jun-20":111324,
		"01-Jul-20":187206,
		"15-Jul-20":284861,
		"01-Aug-20":431006,
		"15-Aug-20":581622
},
 "Meghalaya":{
		"01-Mar-20":0,
		"15-Mar-20":0,
		"01-Apr-20":0,
		"15-Apr-20":7,
		"01-May-20":12,
		"15-May-20":13,
		"01-Jun-20":28,
		"15-Jun-20":44,
		"01-Jul-20":58,
		"15-Jul-20":377,
		"01-Aug-20":849,
		"15-Aug-20":1254
},
 "Manipur":{
		"01-Mar-20":0,
		"15-Mar-20":41,
		"01-Apr-20":42,
		"15-Apr-20":43,
		"01-May-20":43,
		"15-May-20":44,
		"01-Jun-20":124,
		"15-Jun-20":531,
		"01-Jul-20":1320,
		"15-Jul-20":1805,
		"01-Aug-20":2698,
		"15-Aug-20":4275
},
 "Madhya Pradesh":{
		"01-Mar-20":0,
		"15-Mar-20":262,
		"01-Apr-20":360,
		"15-Apr-20":1200,
		"01-May-20":2977,
		"15-May-20":4857,
		"01-Jun-20":8545,
		"15-Jun-20":11197,
		"01-Jul-20":14368,
		"15-Jul-20":20640,
		"01-Aug-20":32772,
		"15-Aug-20":44380
},
 "Mizoram":{
		"01-Mar-20":0,
		"15-Mar-20":3,
		"01-Apr-20":4,
		"15-Apr-20":4,
		"01-May-20":4,
		"15-May-20":4,
		"01-Jun-20":4,
		"15-Jun-20":120,
		"01-Jul-20":165,
		"15-Jul-20":275,
		"01-Aug-20":421,
		"15-Aug-20":670
},
 "Nagaland":{
		"01-Mar-20":0,
		"15-Mar-20":10,
		"01-Apr-20":10,
		"15-Apr-20":10,
		"01-May-20":10,
		"15-May-20":10,
		"01-Jun-20":53,
		"15-Jun-20":187,
		"01-Jul-20":545,
		"15-Jul-20":926,
		"01-Aug-20":1743,
		"15-Aug-20":3372
},
 "Orissa":{
		"01-Mar-20":0,
		"15-Mar-20":218,
		"01-Apr-20":223,
		"15-Apr-20":278,
		"01-May-20":372,
		"15-May-20":955,
		"01-Jun-20":2322,
		"15-Jun-20":4273,
		"01-Jul-20":7763,
		"15-Jul-20":15610,
		"01-Aug-20":32813,
		"15-Aug-20":55566
},
 "Punjab":{
		"01-Mar-20":0,
		"15-Mar-20":71,
		"01-Apr-20":116,
		"15-Apr-20":256,
		"01-May-20":655,
		"15-May-20":2002,
		"01-Jun-20":2371,
		"15-Jun-20":3337,
		"01-Jul-20":5854,
		"15-Jul-20":9164,
		"01-Aug-20":16537,
		"15-Aug-20":29431
},
 "Pondicherry":{
		"01-Mar-20":0,
		"15-Mar-20":19,
		"01-Apr-20":22,
		"15-Apr-20":26,
		"01-May-20":27,
		"15-May-20":35,
		"01-Jun-20":98,
		"15-Jun-20":221,
		"01-Jul-20":821,
		"15-Jul-20":1764,
		"01-Aug-20":3582,
		"15-Aug-20":7105
},
 "Rajasthan":{
		"01-Mar-20":0,
		"15-Mar-20":84,
		"01-Apr-20":200,
		"15-Apr-20":1156,
		"01-May-20":2746,
		"15-May-20":4827,
		"01-Jun-20":9180,
		"15-Jun-20":13061,
		"01-Jul-20":18742,
		"15-Jul-20":27254,
		"01-Aug-20":42778,
		"15-Aug-20":59387
},
 "Sikkim":{
		"01-Mar-20":0,
		"15-Mar-20":0,
		"01-Apr-20":0,
		"15-Apr-20":0,
		"01-May-20":0,
		"15-May-20":0,
		"01-Jun-20":1,
		"15-Jun-20":68,
		"01-Jul-20":101,
		"15-Jul-20":235,
		"01-Aug-20":684,
		"15-Aug-20":1125
},
 "Telangana":{
		"01-Mar-20":0,
		"15-Mar-20":101,
		"01-Apr-20":225,
		"15-Apr-20":748,
		"01-May-20":1142,
		"15-May-20":1552,
		"01-Jun-20":2890,
		"15-Jun-20":5291,
		"01-Jul-20":18668,
		"15-Jul-20":41116,
		"01-Aug-20":64279,
		"15-Aug-20":89972
},
 "TamilNadu":{
		"01-Mar-20":6,
		"15-Mar-20":101,
		"01-Apr-20":334,
		"15-Apr-20":1342,
		"01-May-20":2626,
		"15-May-20":10208,
		"01-Jun-20":23595,
		"15-Jun-20":46604,
		"01-Jul-20":98492,
		"15-Jul-20":156469,
		"01-Aug-20":250497,
		"15-Aug-20":330883
},
 "Tripura":{
		"01-Mar-20":0,
		"15-Mar-20":34,
		"01-Apr-20":34,
		"15-Apr-20":36,
		"01-May-20":37,
		"15-May-20":190,
		"01-Jun-20":457,
		"15-Jun-20":1123,
		"01-Jul-20":1474,
		"15-Jul-20":2413,
		"01-Aug-20":5148,
		"15-Aug-20":6934
},
 "UttarPradesh":{
		"01-Mar-20":0,
		"15-Mar-20":112,
		"01-Apr-20":216,
		"15-Apr-20":834,
		"01-May-20":2427,
		"15-May-20":4156,
		"01-Jun-20":8460,
		"15-Jun-20":14190,
		"01-Jul-20":24924,
		"15-Jul-20":43540,
		"01-Aug-20":87282,
		"15-Aug-20":147108
},
 "Uttarakand":{
		"01-Mar-20":0,
		"15-Mar-20":121,
		"01-Apr-20":128,
		"15-Apr-20":158,
		"01-May-20":178,
		"15-May-20":203,
		"01-Jun-20":1080,
		"15-Jun-20":1966,
		"01-Jul-20":3105,
		"15-Jul-20":4103,
		"01-Aug-20":7424,
		"15-Aug-20":11856
},
 "WestBengal":{
		"01-Mar-20":0,
		"15-Mar-20":47,
		"01-Apr-20":84,
		"15-Apr-20":260,
		"01-May-20":842,
		"15-May-20":2508,
		"01-Jun-20":5819,
		"15-Jun-20":11541,
		"01-Jul-20":19866,
		"15-Jul-20":36164,
		"01-Aug-20":72129,
		"15-Aug-20":112299
},
 "India":{
		"01-Mar-20":0,
		"15-Mar-20":322,
		"01-Apr-20":2273,
		"15-Apr-20":12584,
		"01-May-20":37476,
		"15-May-20":86069,
		"01-Jun-20":198582,
		"15-Jun-20":343282,
		"01-Jul-20":627278,
		"15-Jul-20":1005749,
		"01-Aug-20":1731995,
		"15-Aug-20":2560163
}
}
s_names=[ 'Andaman And Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 'Chandigarh', 'Chattisgarh', 'Daman & Diu', 'Delhi','Dardar and Nagar Haveli', 'Goa', 'Gujarath', 'Himachal Pradesh','Haryana', 'Jarkhand', 'Jammu And Kashmir', 'Karnataka', 'Kerala','Ladakh', 'Lakshwadeep', 'Maharashtra', 'Meghalaya', 'Manipur','Madhya Pradesh', 'Mizoram', 'Nagaland', 'Orissa', 'Punjab','Pondicherry', 'Rajasthan', 'Sikkim', 'Telangana', 'TamilNadu','Tripura', 'UttarPradesh', 'Uttarakand', 'WestBengal', 'India']
if __name__=='__main__':
	db.create_all()
	app.run(debug=True)
