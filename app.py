from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_score.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def safe_characters(text):
    # Allow only letters, numbers, spaces, hyphens, underscores
    return re.sub(r'[^a-zA-Z0-9 \-_]', '', text).strip()

# Model pro hráče
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_score.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model pro hráče
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    total_score = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    scores = db.relationship('Score', backref='player', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'total_score': self.total_score,
            'games_played': self.games_played,
            'average_score': round(self.total_score / self.games_played, 2) if self.games_played > 0 else 0
        }

# Model pro skóre (relace s hráčem)
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    game_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    notes = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'player_name': self.player.name,
            'score': self.score,
            'game_date': self.game_date.strftime('%d.%m.%Y %H:%M:%S'),
            'notes': self.notes
        }

# Vytvoření databází
with app.app_context():
    db.create_all()

# Rutiny
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([p.to_dict() for p in players])

@app.route('/api/players', methods=['POST'])
def add_player():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Jméno je povinné'}), 400
    
    sanitized_name = safe_characters(data['name'])
    if not sanitized_name:
        return jsonify({'error': 'Jméno obsahuje neplatné znaky'}), 400
    
    if Player.query.filter_by(name=sanitized_name).first():
        return jsonify({'error': 'Hráč s tímto jménem již existuje'}), 400
    
    player = Player(name=sanitized_name)
    db.session.add(player)
    db.session.commit()
    return jsonify(player.to_dict()), 201

@app.route('/api/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return '', 204

@app.route('/api/scores', methods=['POST'])
def add_score():
    data = request.get_json()
    if not data or not data.get('player_id') or data.get('score') is None:
        return jsonify({'error': 'player_id a score jsou povinné'}), 400
    
    player = Player.query.get_or_404(data['player_id'])
    score = Score(
        player_id=data['player_id'],
        score=data['score'],
        notes=data.get('notes', '')
    )
    
    player.total_score += data['score']
    player.games_played += 1
    
    db.session.add(score)
    db.session.commit()
    
    return jsonify(score.to_dict()), 201

@app.route('/api/players/<int:player_id>/scores', methods=['GET'])
def get_player_scores(player_id):
    player = Player.query.get_or_404(player_id)
    scores = Score.query.filter_by(player_id=player_id).order_by(Score.game_date.desc()).all()
    return jsonify([s.to_dict() for s in scores])

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    players = Player.query.order_by(Player.total_score.desc()).all()
    return jsonify([p.to_dict() for p in players])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
