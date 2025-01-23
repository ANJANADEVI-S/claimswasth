from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False, unique=True)

# Define the Agent model
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False, unique=True)

# Route for the homepage (login page)
@app.route('/')
def home():
    return render_template('frontpage.html')

# Route for user login
@app.route('/user_login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "username", "message": "Username does not exist"}), 400
    elif not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "password", "message": "Incorrect password"}), 400
    
    session['user_id'] = user.id
    return redirect(url_for('user_dashboard'))

# Route for agent login
@app.route('/agent_login', methods=['POST'])
def agent_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    agent = Agent.query.filter_by(username=username).first()

    if not agent:
        return jsonify({"error": "username", "message": "Username does not exist"}), 400
    elif not bcrypt.check_password_hash(agent.password, password):
        return jsonify({"error": "password", "message": "Incorrect password"}), 400

    session['agent_id'] = agent.id
    return redirect(url_for('agent_dashboard'))

'''@app.route('/agent_logout',methods=['POST'])
def logout():
    if 'agent_id' in session:
        session.pop('agent_id',None)
        return redirect(url_for('home'))'''

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')  
    else:
        return redirect(url_for('home'))

@app.route('/need_to_submit_claim', methods=['POST'])
def need_to_submit_claim():
    return render_template('submit_claim.html')  # Your new page template

class Claim(db.Model):
    __tablename__ = 'claims'
    
    id = db.Column(db.Integer, primary_key=True)
    claim_type = db.Column(db.String(50), nullable=False)
    claim_date = db.Column(db.Date, nullable=False)
    proposer_name = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.String(100), nullable=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_gender = db.Column(db.String(10), nullable=False)
    patient_dob = db.Column(db.Date, nullable=False)
    patient_relationship = db.Column(db.String(50), nullable=False)
    accident_date = db.Column(db.Date, nullable=True)
    accident_time = db.Column(db.Time, nullable=True)
    reported_to_police = db.Column(db.String(10), nullable=False)
    previous_claims = db.Column(db.String(10), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    procedure_type = db.Column(db.String(50), nullable=False)
    admission_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date, nullable=False)
    admission_type = db.Column(db.String(50), nullable=False)
    hospitalization_expenses = db.Column(db.Float, nullable=False)
    pre_hospitalization_expenses = db.Column(db.Float, nullable=True)
    post_hospitalization_expenses = db.Column(db.Float, nullable=True)
    ambulance_charges = db.Column(db.Float, nullable=True)
    other_expenses = db.Column(db.Float, nullable=True)
    total_expenses = db.Column(db.Float, nullable=True)
    hospital_name = db.Column(db.String(200), nullable=False)
    hospital_city = db.Column(db.String(100), nullable=False)
    hospital_type = db.Column(db.String(50), nullable=False)
    treating_doctor_name = db.Column(db.String(100), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/submit_claim', methods=['POST'])
def submit_claim():
    # Get data from the form
    claim_type = request.form.get('claim_type')
    claim_date = request.form.get('claim_date')
    proposer_name = request.form.get('proposer_name')
    customer_id = request.form.get('customer_id')
    patient_name = request.form.get('patient_name')
    patient_gender = request.form.get('patient_gender')
    patient_dob = request.form.get('patient_dob')
    patient_relationship = request.form.get('patient_relationship')
    accident_date = request.form.get('accident_date')
    accident_time = request.form.get('accident_time')
    reported_to_police = request.form.get('reported_to_police')
    previous_claims = request.form.get('previous_claims')
    diagnosis = request.form.get('diagnosis')
    procedure_type = request.form.get('procedure_type')
    admission_date = request.form.get('admission_date')
    discharge_date = request.form.get('discharge_date')
    admission_type = request.form.get('admission_type')
    hospitalization_expenses = request.form.get('hospitalization_expenses')
    pre_hospitalization_expenses = request.form.get('pre_hospitalization_expenses')
    post_hospitalization_expenses = request.form.get('post_hospitalization_expenses')
    ambulance_charges = request.form.get('ambulance_charges')
    other_expenses = request.form.get('other_expenses')
    total_expenses = request.form.get('total_expenses')
    hospital_name = request.form.get('hospital_name')
    hospital_city = request.form.get('hospital_city')
    hospital_type = request.form.get('hospital_type')
    treating_doctor_name = request.form.get('treating_doctor_name')

    # Create a new Claim object
    new_claim = Claim(
        claim_type=claim_type,
        claim_date=datetime.strptime(claim_date, '%Y-%m-%d'),
        proposer_name=proposer_name,
        customer_id=customer_id,
        patient_name=patient_name,
        patient_gender=patient_gender,
        patient_dob=datetime.strptime(patient_dob, '%Y-%m-%d'),
        patient_relationship=patient_relationship,
        accident_date=datetime.strptime(accident_date, '%Y-%m-%d') if accident_date else None,
        accident_time=datetime.strptime(accident_time, '%H:%M') if accident_time else None,
        reported_to_police=reported_to_police,
        previous_claims=previous_claims,
        diagnosis=diagnosis,
        procedure_type=procedure_type,
        admission_date=datetime.strptime(admission_date, '%Y-%m-%d'),
        discharge_date=datetime.strptime(discharge_date, '%Y-%m-%d'),
        admission_type=admission_type,
        hospitalization_expenses=float(hospitalization_expenses),
        pre_hospitalization_expenses=float(pre_hospitalization_expenses) if pre_hospitalization_expenses else 0,
        post_hospitalization_expenses=float(post_hospitalization_expenses) if post_hospitalization_expenses else 0,
        ambulance_charges=float(ambulance_charges) if ambulance_charges else 0,
        other_expenses=float(other_expenses) if other_expenses else 0,
        total_expenses=float(total_expenses) if total_expenses else 0,
        hospital_name=hospital_name,
        hospital_city=hospital_city,
        hospital_type=hospital_type,
        treating_doctor_name=treating_doctor_name
    )

    # Add to session and commit to the database
    db.session.add(new_claim)
    db.session.commit()

    # redirect to confirmation page
    return redirect(url_for('claim_submitted', claim_id=new_claim.id))

@app.route('/claim_submitted')
def claim_submitted():
    claim_id = request.args.get('claim_id', type=int)
    claim = Claim.query.get_or_404(claim_id) 
    return render_template('claim_submitted.html',claim=claim)

@app.route('/agent_dashboard')
def agent_dashboard():
    if 'agent_id' in session:  
        # Fetch all claims from the database
        claims = Claim.query.order_by(Claim.claim_date.desc()).all()

        total_claims = len(claims)
        #claims_approved = len([claim for claim in claims if claim.status == "Approved"])
        #claims_rejected = len([claim for claim in claims if claim.status == "Rejected"])

        # Render the template with claims and summary data
        return render_template(
            'agent_dashboard.html', 
            claims=claims,
            total_claims=total_claims,
            #claims_approved=claims_approved,
            #claims_rejected=claims_rejected
        )
    else:
        return redirect(url_for('home'))  # Redirect if the agent isn't logged in

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
