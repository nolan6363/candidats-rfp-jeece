import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../App'
import api from '../api'

const ROLE_COLORS = {
  'Président':      { bg: 'rgba(63,173,93,0.18)',   color: '#1a6e30' },
  'Trésorerie':     { bg: 'rgba(7,31,50,0.15)',      color: '#071F32' },
  'DirOps':         { bg: 'rgba(50,100,160,0.16)',   color: '#1a3e6e' },
  'DirCo':          { bg: 'rgba(122,4,35,0.15)',     color: '#7A0423' },
  'SG':             { bg: 'rgba(155,89,182,0.17)',   color: '#6c3483' },
  'Chef de Projet': { bg: 'rgba(41,128,185,0.17)',   color: '#1a5276' },
  'CDM Perf':       { bg: 'rgba(230,126,34,0.18)',   color: '#8a4000' },
  'CDM RH':         { bg: 'rgba(231,76,60,0.16)',    color: '#922b21' },
  'CDM SI':         { bg: 'rgba(26,188,156,0.18)',   color: '#0e6655' },
  'CDM Comm':       { bg: 'rgba(52,152,219,0.18)',   color: '#1a5e8a' },
  'CDM Market':     { bg: 'rgba(243,156,18,0.18)',   color: '#7d5a00' },
  'RM':             { bg: 'rgba(192,57,43,0.16)',    color: '#7b241c' },
  'RC':             { bg: 'rgba(39,174,96,0.17)',    color: '#1a5e35' },
  'RTC':            { bg: 'rgba(142,68,173,0.16)',   color: '#5b2c8d' },
  'RTC Elec':       { bg: 'rgba(100,30,173,0.17)',   color: '#4a1a80' },
  'RDI':            { bg: 'rgba(22,160,133,0.18)',   color: '#0e6251' },
  'DSI':            { bg: 'rgba(44,62,80,0.16)',     color: '#2c3e50' },
}

const ALL_ROLES = Object.keys(ROLE_COLORS)

function RoleBadge({ role, onDelete }) {
  const c = ROLE_COLORS[role] || { bg: 'rgba(100,100,100,0.12)', color: '#444' }
  return (
    <span className="voeu-cell">
      <span className="badge" style={{ background: c.bg, color: c.color }}>{role}</span>
      {onDelete && (
        <button className="delete-voeu" onClick={onDelete} title="Supprimer ce vœu">×</button>
      )}
    </span>
  )
}

function VoeuCell({ candidate, rank, isAdmin, onDelete }) {
  const voeu = candidate.voeux.find(v => v.rank === rank)
  if (!voeu) return <span className="badge-empty">—</span>
  return (
    <RoleBadge
      role={voeu.role}
      onDelete={isAdmin ? () => onDelete(candidate.id, rank) : null}
    />
  )
}

export default function Home() {
  const { isAdmin, logout } = useAuth()
  const [candidates, setCandidates] = useState([])
  const [filterRole, setFilterRole] = useState('')
  const [showAbandoned, setShowAbandoned] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchCandidates = () => {
    api.get('/api/candidates')
      .then(r => { setCandidates(r.data); setLoading(false) })
      .catch(() => { setError('Erreur lors du chargement.'); setLoading(false) })
  }

  useEffect(() => { fetchCandidates() }, [])

  const handleAbandon = (id) => {
    api.put(`/api/candidates/${id}/abandon`)
      .then(r => setCandidates(prev => prev.map(c => c.id === id ? r.data : c)))
      .catch(() => {})
  }

  const handleDeleteVoeu = (candidateId, rank) => {
    if (!window.confirm('Supprimer ce vœu ?')) return
    api.delete(`/api/candidates/${candidateId}/voeux/${rank}`)
      .then(r => setCandidates(prev => prev.map(c => c.id === candidateId ? r.data : c)))
      .catch(() => {})
  }

  const filtered = candidates.filter(c => {
    if (!showAbandoned && c.abandoned) return false
    if (filterRole) return c.voeux.some(v => v.role === filterRole)
    return true
  })

  const activeCount = candidates.filter(c => !c.abandoned).length
  const abandonedCount = candidates.filter(c => c.abandoned).length

  return (
    <>
      <header className="header">
        <div>
          <div className="header-title"><span>JEECE</span> — Postulants RFP 25-26</div>
          <div className="header-meta">
            {activeCount} candidat{activeCount !== 1 ? 's' : ''} actif{activeCount !== 1 ? 's' : ''}
            {abandonedCount > 0 && ` · ${abandonedCount} abandonné${abandonedCount !== 1 ? 's' : ''}`}
          </div>
        </div>
        <div className="header-right">
          {isAdmin ? (
            <>
              <span className="admin-badge">Admin</span>
              <Link to="/admin/logs" className="btn btn-outline">Logs</Link>
              <button className="btn btn-outline" onClick={logout}>Déconnexion</button>
            </>
          ) : (
            <Link to="/admin/login" className="btn btn-outline">Admin</Link>
          )}
        </div>
      </header>

      <div className="controls">
        <label htmlFor="role-filter">Filtrer par poste :</label>
        <select
          id="role-filter"
          className="select-role"
          value={filterRole}
          onChange={e => setFilterRole(e.target.value)}
        >
          <option value="">Tous les postes</option>
          {ALL_ROLES.map(r => <option key={r} value={r}>{r}</option>)}
        </select>

        <label className="toggle-abandoned">
          <input
            type="checkbox"
            checked={showAbandoned}
            onChange={e => setShowAbandoned(e.target.checked)}
          />
          Afficher les abandons
        </label>

        <span className="count-label">
          {filtered.length} / {candidates.length} candidat{candidates.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="table-wrapper">
        {loading ? (
          <p className="empty-state">Chargement…</p>
        ) : error ? (
          <p className="empty-state">{error}</p>
        ) : (
          <div className="table-block">
            <table>
              <thead>
                <tr>
                  <th className="col-num">#</th>
                  <th>Candidat</th>
                  <th className="col-voeu">Vœu 1</th>
                  <th className="col-voeu">Vœu 2</th>
                  <th className="col-voeu">Vœu 3</th>
                  {isAdmin && <th className="col-actions">Actions</th>}
                </tr>
              </thead>
              <tbody>
                {filtered.length === 0 ? (
                  <tr>
                    <td colSpan={isAdmin ? 6 : 5} className="empty-state">
                      Aucun candidat trouvé.
                    </td>
                  </tr>
                ) : filtered.map((c, i) => (
                  <tr key={c.id} className={c.abandoned ? 'abandoned' : ''}>
                    <td className="col-num">{String(i + 1).padStart(2, '0')}</td>
                    <td>
                      <div className="candidate-name">
                        <span className="candidate-prenom">
                          {c.prenom}
                          {c.abandoned && <span className="abandoned-label">abandonné</span>}
                        </span>
                        <span className="candidate-nom">{c.nom}</span>
                      </div>
                    </td>
                    <td><VoeuCell candidate={c} rank={1} isAdmin={isAdmin} onDelete={handleDeleteVoeu} /></td>
                    <td><VoeuCell candidate={c} rank={2} isAdmin={isAdmin} onDelete={handleDeleteVoeu} /></td>
                    <td><VoeuCell candidate={c} rank={3} isAdmin={isAdmin} onDelete={handleDeleteVoeu} /></td>
                    {isAdmin && (
                      <td>
                        {c.abandoned ? (
                          <button className="btn btn-restore" onClick={() => handleAbandon(c.id)}>
                            Réactiver
                          </button>
                        ) : (
                          <button className="btn btn-danger" onClick={() => handleAbandon(c.id)}>
                            Abandonné
                          </button>
                        )}
                      </td>
                    )}
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
