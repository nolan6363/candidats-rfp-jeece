from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Candidate, Voeu, ActionLog

candidates_bp = Blueprint('candidates', __name__)


@candidates_bp.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.order_by(Candidate.nom).all()
    return jsonify([c.to_dict() for c in candidates])


@candidates_bp.route('/candidates/<int:candidate_id>/abandon', methods=['PUT'])
@jwt_required()
def toggle_abandon(candidate_id):
    candidate = db.get_or_404(Candidate, candidate_id)
    candidate.abandoned = not candidate.abandoned
    action = 'abandoned' if candidate.abandoned else 'restored'
    db.session.add(ActionLog(candidate_id=candidate_id, action=action))
    db.session.commit()
    return jsonify(candidate.to_dict())


@candidates_bp.route('/candidates/<int:candidate_id>/voeux/<int:rank>', methods=['PUT'])
@jwt_required()
def restore_voeu(candidate_id, rank):
    from flask import request
    data = request.get_json() or {}
    role = data.get('role', '')
    if not role:
        return jsonify({'error': 'role requis'}), 400
    candidate = db.get_or_404(Candidate, candidate_id)
    if Voeu.query.filter_by(candidate_id=candidate_id, rank=rank).first():
        return jsonify({'error': 'Ce vœu existe déjà'}), 409
    db.session.add(Voeu(candidate_id=candidate_id, rank=rank, role=role))
    db.session.add(ActionLog(candidate_id=candidate_id, action='voeu_restored', voeu_rank=rank, voeu_role=role))
    db.session.commit()
    db.session.refresh(candidate)
    return jsonify(candidate.to_dict())


@candidates_bp.route('/candidates/<int:candidate_id>/voeux/<int:rank>', methods=['DELETE'])
@jwt_required()
def delete_voeu(candidate_id, rank):
    voeu = Voeu.query.filter_by(candidate_id=candidate_id, rank=rank).first_or_404()
    role = voeu.role
    db.session.delete(voeu)
    db.session.add(ActionLog(candidate_id=candidate_id, action='voeu_deleted', voeu_rank=rank, voeu_role=role))
    db.session.commit()
    candidate = db.get_or_404(Candidate, candidate_id)
    return jsonify(candidate.to_dict())
