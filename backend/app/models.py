from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(150), nullable=False)
    abandoned = db.Column(db.Boolean, default=False, nullable=False)
    voeux = db.relationship(
        'Voeu', backref='candidate',
        cascade='all, delete-orphan',
        order_by='Voeu.rank'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'prenom': self.prenom,
            'nom': self.nom,
            'abandoned': self.abandoned,
            'voeux': [v.to_dict() for v in self.voeux],
        }


class Voeu(db.Model):
    __tablename__ = 'voeux'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'rank': self.rank, 'role': self.role}


class ActionLog(db.Model):
    __tablename__ = 'action_logs'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    action = db.Column(db.Enum('abandoned', 'restored', 'voeu_deleted', 'voeu_restored'), nullable=False)
    voeu_rank = db.Column(db.SmallInteger, nullable=True)
    voeu_role = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    candidate = db.relationship('Candidate')

    def to_dict(self):
        d = {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'candidate_prenom': self.candidate.prenom,
            'candidate_nom': self.candidate.nom,
            'candidate_abandoned': self.candidate.abandoned,
            'action': self.action,
            'created_at': self.created_at.isoformat(),
        }
        if self.action == 'voeu_deleted':
            d['voeu_rank'] = self.voeu_rank
            d['voeu_role'] = self.voeu_role
        return d
