from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mydaddy45@localhost/baby-tracker'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Event: {self.description}"
    
    def __init__(self, description) -> None:
        self.description = description

def format_event(event):
    return {
        #"message": "successful",
        "id": event.id,
        "description": event.description,
        "created_at": event.created_at,
    }


@app.route('/hello')
def hello():
    return 'Hello world'

@app.route('/event/create', methods=['POST'])
def create_event():
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return jsonify(format_event(event))


@app.route('/event/all', methods=['GET'])
def get_event():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list}


@app.route('/event/<id>')
def get_single(id):
    event = Event.query.filter_by(id=id).one()
    formatted_evt = format_event(event)
    return {'event': formatted_evt}

@app.route('/event/delete/<id>', methods=['DELETE'])
def env_delete(id):
    event = Event.query.filter_by(id=id).one()
    db.session.delete(event)
    db.session.commit()
    return f"Event with id={id} deleted"


@app.route('/event/update/<id>', methods=['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    description = request.json['description']
    event.update(dict(description=description, created_at=datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)