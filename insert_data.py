from app import app, db, User, Agent, bcrypt

# Create users
with app.app_context():
    user1 = User(username='user1', password=bcrypt.generate_password_hash('password1').decode('utf-8'))
    user2 = User(username='user2', password=bcrypt.generate_password_hash('password2').decode('utf-8'))

    # Create agents
    agent1 = Agent(username='agent1', password=bcrypt.generate_password_hash('agentpass1').decode('utf-8'))
    agent2 = Agent(username='agent2', password=bcrypt.generate_password_hash('agentpass2').decode('utf-8'))

    # Add entries to the session
    db.session.add_all([user1, user2, agent1, agent2])

    # Commit the session to save to the database
    db.session.commit()
    print("Data inserted successfully!")
