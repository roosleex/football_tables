import { useEffect, useState } from 'react'
import type { League, LeagueStandings } from './types'
import { fetchLeagues, fetchStandings } from './api/client'
import { LeagueList } from './components/LeagueList'
import { StandingsTable } from './components/StandingsTable'
import { TopThreeBoard } from './components/TopThreeBoard'
import { LanguageSelector } from './components/LanguageSelector'
import { useLanguage } from './i18n/LanguageContext'
import { deleteCookie, getCookie, setCookie } from './utils/cookies'

const REFRESH_INTERVAL_MS = 60_000 // refresh standings every minute
const HIDDEN_LEAGUES_COOKIE = 'hidden_leagues'

function loadHiddenLeagues(): Set<string> {
  const raw = getCookie(HIDDEN_LEAGUES_COOKIE)
  if (!raw) return new Set()
  return new Set(
    raw
      .split(',')
      .map((code) => code.trim())
      .filter(Boolean),
  )
}

export default function App() {
  const { t } = useLanguage()
  const [leagues, setLeagues] = useState<League[]>([])
  const [selectedCode, setSelectedCode] = useState<string | null>(null)
  const [standings, setStandings] = useState<LeagueStandings | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<'loadError' | 'standingsError' | null>(null)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [hiddenLeagues, setHiddenLeagues] = useState<Set<string>>(loadHiddenLeagues)

  useEffect(() => {
    if (hiddenLeagues.size === 0) {
      deleteCookie(HIDDEN_LEAGUES_COOKIE)
    } else {
      setCookie(HIDDEN_LEAGUES_COOKIE, Array.from(hiddenLeagues).join(','))
    }
  }, [hiddenLeagues])

  useEffect(() => {
    fetchLeagues()
      .then((data) => setLeagues(data))
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

  const goHome = () => {
    setSelectedCode(null)
    setStandings(null)
    setError(null)
    setLoading(false)
  }

  const hideLeague = (code: string) => {
    setHiddenLeagues((prev) => {
      const next = new Set(prev)
      next.add(code)
      return next
    })
  }

  const resetSettings = () => {
    setHiddenLeagues(new Set())
  }

  return (
    <div className="app">
      <header className="topbar">
        <button
          type="button"
          className="brand"
          onClick={goHome}
          aria-label={t('appTitle')}
        >
          <span className="brand-ball">⚽</span>
          <span className="brand-title">{t('appTitle')}</span>
        </button>
        <div className="topbar-controls">
          <button
            type="button"
            className="reset-button"
            onClick={resetSettings}
          >
            {t('resetSettings')}
          </button>
          <LanguageSelector />
        </div>
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
          {error === 'loadError' ? (
            <p className="error">{t('loadError')}</p>
          ) : selectedCode ? (
            <>
              {loading && !standings && <p className="muted">{t('loading')}</p>}
              {error === 'standingsError' && (
                <p className="error">{t('standingsError')}</p>
              )}
              {standings && (
                <StandingsTable standings={standings} lastUpdated={lastUpdated} />
              )}
            </>
          ) : (
            <TopThreeBoard
              leagues={leagues}
              hiddenLeagues={hiddenLeagues}
              onSelect={setSelectedCode}
              onClose={hideLeague}
            />
          )}
        </main>
      </div>
    </div>
  )
}