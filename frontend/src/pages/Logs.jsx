import { useState, useEffect } from 'react'
import { Link, Navigate } from 'react-router-dom'
import { useAuth } from '../App'
import api from '../api'

function formatDate(iso) {
  const d = new Date(iso)
  return d.toLocaleDateString('fr-FR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  })
}

export default function Logs() {
  const { isAdmin, logout } = useAuth()
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  if (!isAdmin) return <Navigate to="/admin/login" />

  const fetchLogs = () => {
    api.get('/api/logs')
      .then(r => { setLogs(r.data); setLoading(false) })
      .catch(() => { setError('Erreur lors du chargement.'); setLoading(false) })
  }

  useEffect(() => { fetchLogs() }, [])

  const handleUndoAbandon = (candidateId) => {
    api.put(`/api/candidates/${candidateId}/abandon`)
      .then(() => fetchLogs())
      .catch(() => {})
  }

  const handleRestoreVoeu = (candidateId, rank, role) => {
    api.put(`/api/candidates/${candidateId}/voeux/${rank}`, { role })
      .then(() => fetchLogs())
      .catch(() => {})
  }

  return (
    <>
      <header className="header">
        <div>
          <div className="header-title"><span>JEECE</span> — Historique des actions</div>
          <div className="header-meta">Abandons et suppressions de vœux</div>
        </div>
        <div className="header-right">
          <span className="admin-badge">Admin</span>
          <button className="btn btn-outline" onClick={logout}>Déconnexion</button>
        </div>
      </header>

      <div className="admin-nav">
        <Link to="/" className="admin-nav-link">← Liste des candidats</Link>
      </div>

      <div className="table-wrapper">
        {loading ? (
          <p className="empty-state">Chargement…</p>
        ) : error ? (
          <p className="empty-state">{error}</p>
        ) : logs.length === 0 ? (
          <p className="empty-state">Aucune action enregistrée.</p>
        ) : (
          <div className="table-block">
            <table>
              <thead>
                <tr>
                  <th>Date / Heure</th>
                  <th>Candidat</th>
                  <th>Action</th>
                  <th>Détail</th>
                  <th className="col-actions"></th>
                </tr>
              </thead>
              <tbody>
                {logs.map(log => (
                  <tr key={log.id}>
                    <td className="log-date">{formatDate(log.created_at)}</td>
                    <td>
                      <div className="candidate-name">
                        <span className="candidate-prenom">{log.candidate_prenom}</span>
                        <span className="candidate-nom">{log.candidate_nom}</span>
                      </div>
                    </td>
                    <td>
                      <span className={`log-action-badge log-action-${log.action}`}>
                        {log.action === 'abandoned'      && 'Abandonné'}
                        {log.action === 'restored'       && 'Réactivé'}
                        {log.action === 'voeu_deleted'   && 'Vœu supprimé'}
                        {log.action === 'voeu_restored'  && 'Vœu restauré'}
                      </span>
                    </td>
                    <td>
                      {(log.action === 'voeu_deleted' || log.action === 'voeu_restored') && (
                        <span className="log-voeu-detail">
                          <span className="log-voeu-rank">Vœu {log.voeu_rank}</span>
                          {' — '}
                          <span className="log-voeu-role">{log.voeu_role}</span>
                        </span>
                      )}
                    </td>
                    <td>
                      {log.action === 'abandoned' && log.candidate_abandoned && (
                        <button className="btn btn-restore" onClick={() => handleUndoAbandon(log.candidate_id)}>
                          Annuler
                        </button>
                      )}
                      {log.action === 'voeu_deleted' && (
                        <button className="btn btn-restore" onClick={() => handleRestoreVoeu(log.candidate_id, log.voeu_rank, log.voeu_role)}>
                          Restaurer
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  )
}
