import { useEffect, useState } from 'react'
import type { League, LeagueStandings } from './types'
import { fetchLeagues, fetchStandings } from './api/client'
import { LeagueList } from './components/LeagueList'
import { StandingsTable } from './components/StandingsTable'

export default function App() {
  const [leagues, setLeagues] = useState<League[]>([])
  const [selectedCode, setSelectedCode] = useState<string | null>(null)
  const [standings, setStandings] = useState<LeagueStandings | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchLeagues()
      .then((data) => {
        setLeagues(data)
        if (data.length > 0) setSelectedCode(data[0].code)
      })
      .catch(() => setError('Could not load leagues. Is the backend running?'))
  }, [])

  useEffect(() => {
    if (!selectedCode) return
    let active = true
    setLoading(true)
    setError(null)
    fetchStandings(selectedCode)
      .then((data) => {
        if (active) setStandings(data)
      })
      .catch(() => {
        if (active) setError('Could not load standings.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [selectedCode])

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-ball">⚽</span>
          <span className="brand-title">Football Tables</span>
        </div>
        <LeagueList
          leagues={leagues}
          selectedCode={selectedCode ?? ''}
          onSelect={setSelectedCode}
        />
      </aside>
      <main className="content">
        {loading && <p className="muted">Loading…</p>}
        {error && <p className="error">{error}</p>}
        {!loading && !error && standings && <StandingsTable standings={standings} />}
        {!loading && !error && !standings && (
          <p className="muted">Select a league to begin.</p>
        )}
      </main>
    </div>
  )
}