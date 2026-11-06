import { useEffect, useState } from 'react'
import type { League, LeagueStandings } from './types'
import { fetchLeagues, fetchStandings } from './api/client'
import { LeagueList } from './components/LeagueList'
import { StandingsTable } from './components/StandingsTable'
import { LanguageSelector } from './components/LanguageSelector'
import { useLanguage } from './i18n/LanguageContext'

const REFRESH_INTERVAL_MS = 60_000 // refresh standings every minute

export default function App() {
  const { t } = useLanguage()
  const [leagues, setLeagues] = useState<League[]>([])
  const [selectedCode, setSelectedCode] = useState<string | null>(null)
  const [standings, setStandings] = useState<LeagueStandings | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<'loadError' | 'standingsError' | null>(null)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)

  useEffect(() => {
    fetchLeagues()
      .then((data) => {
        setLeagues(data)
        if (data.length > 0) setSelectedCode(data[0].code)
      })
      .catch(() => setError('loadError'))
  }, [])

  useEffect(() => {
    if (!selectedCode) return
    let active = true
    setLoading(true)
    setError(null)

    const load = async () => {
      try {
        const data = await fetchStandings(selectedCode)
        if (!active) return
        setStandings(data)
        setLastUpdated(new Date())
      } catch {
        if (active) setError('standingsError')
      } finally {
        if (active) setLoading(false)
      }
    }

    load()
    const interval = window.setInterval(load, REFRESH_INTERVAL_MS)
    return () => {
      active = false
      window.clearInterval(interval)
    }
  }, [selectedCode])

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-ball">⚽</span>
          <span className="brand-title">{t('appTitle')}</span>
        </div>
        <LanguageSelector />
      </header>
      <div className="body">
        <aside className="sidebar">
          <LeagueList
            leagues={leagues}
            selectedCode={selectedCode ?? ''}
            onSelect={setSelectedCode}
          />
        </aside>
        <main className="content">
          {loading && !standings && <p className="muted">{t('loading')}</p>}
          {error && <p className="error">{t(error)}</p>}
          {standings && (
            <StandingsTable standings={standings} lastUpdated={lastUpdated} />
          )}
          {!loading && !error && !standings && (
            <p className="muted">{t('selectHint')}</p>
          )}
        </main>
      </div>
    </div>
  )
}