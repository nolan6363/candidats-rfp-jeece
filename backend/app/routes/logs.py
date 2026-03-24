from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from ..models import ActionLog

logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    logs = ActionLog.query.order_by(ActionLog.created_at.desc()).all()
    return jsonify([l.to_dict() for l in logs])
