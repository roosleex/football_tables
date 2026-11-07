import { useEffect, useState } from 'react'
import type { League, StandingRow } from '../types'
import { fetchStandings } from '../api/client'
import { Flag } from './Flag'
import { useLanguage } from '../i18n/LanguageContext'

interface TopThreeBoardProps {
  leagues: League[]
  hiddenLeagues: Set<string>
  onSelect: (code: string) => void
  onClose: (code: string) => void
}

interface LeagueTopThree {
  league: League
  top: StandingRow[]
}

async function fetchTopThree(league: League): Promise<LeagueTopThree> {
  try {
    const standings = await fetchStandings(league.code)
    return { league, top: standings.table.slice(0, 3) }
  } catch {
    return { league, top: [] }
  }
}

export function TopThreeBoard({
  leagues,
  hiddenLeagues,
  onSelect,
  onClose,
}: TopThreeBoardProps) {
  const { t, leagueName, teamName } = useLanguage()
  const [cards, setCards] = useState<LeagueTopThree[]>([])

  useEffect(() => {
    const visibleLeagues = leagues.filter(
      (league) => !hiddenLeagues.has(league.code),
    )
    let active = true
    Promise.all(visibleLeagues.map(fetchTopThree)).then((result) => {
      if (active) setCards(result)
    })
    return () => {
      active = false
    }
  }, [leagues, hiddenLeagues])

  const visibleCards = cards.filter(
    ({ league }) => !hiddenLeagues.has(league.code),
  )

  if (visibleCards.length === 0) return null

  return (
    <section className="top-three-board">
      {visibleCards.map(({ league, top }) => (
        <article
          key={league.code}
          className="top-three-card"
          role="button"
          tabIndex={0}
          onClick={() => onSelect(league.code)}
          onKeyDown={(event) => {
            if (event.target !== event.currentTarget) return
            if (event.key === 'Enter' || event.key === ' ') {
              event.preventDefault()
              onSelect(league.code)
            }
          }}
        >
          <button
            type="button"
            className="top-three-close"
            aria-label={t('closeLeague')}
            title={t('closeLeague')}
            onClick={(event) => {
              event.stopPropagation()
              onClose(league.code)
            }}
          >
            ×
          </button>
          <header className="top-three-card-header">
            <Flag countryCode={league.country_code} />
            <h2 className="top-three-league">{leagueName(league.code)}</h2>
          </header>
          {top.length > 0 ? (
            <ol className="top-three-list">
              {top.map((row) => (
                <li
                  key={`${league.code}-${row.position}`}
                  className={`top-three-item top-three-item-${row.position}`}
                >
                  <span className="top-three-pos">{row.position}</span>
                  <span className="top-three-team">{teamName(row.team)}</span>
                  <span className="top-three-points">{row.points}</span>
                </li>
              ))}
            </ol>
          ) : (
            <p className="top-three-empty">—</p>
          )}
        </article>
      ))}
    </section>
  )
}