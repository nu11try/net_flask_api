from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://:@localhost/netology_flask_api'
db = SQLAlchemy(app)


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.Column(db.String(50), nullable=False)


@app.route('/advertisements', methods=['POST'])
def create_advertisement():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    owner = data.get('owner')

    if not title or not description or not owner:
        return jsonify({'error': 'Missing fields'}), 400

    advertisement = Advertisement(title=title, description=description, owner=owner)
    db.session.add(advertisement)
    db.session.commit()

    return jsonify({'message': 'Advertisement created successfully'}), 201


@app.route('/advertisements/<int:advertisement_id>', methods=['GET'])
def get_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement is None:
        return jsonify({'error': 'Advertisement not found'}), 404

    return jsonify({
        'title': advertisement.title,
        'description': advertisement.description,
        'created_at': advertisement.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'owner': advertisement.owner
    })


@app.route('/advertisements/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement is None:
        return jsonify({'error': 'Advertisement not found'}), 404

    db.session.delete(advertisement)
    db.session.commit()

    return jsonify({'message': 'Advertisement deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
