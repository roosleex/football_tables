import { useEffect, useState } from 'react'
import type { League, StandingRow } from '../types'
import { fetchStandings } from '../api/client'
import { Flag } from './Flag'
import { useLanguage } from '../i18n/LanguageContext'

interface TopThreeBoardProps {
  leagues: League[]
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

export function TopThreeBoard({ leagues }: TopThreeBoardProps) {
  const { leagueName, teamName } = useLanguage()
  const [cards, setCards] = useState<LeagueTopThree[]>([])

  useEffect(() => {
    let active = true
    Promise.all(leagues.map(fetchTopThree)).then((result) => {
      if (active) setCards(result)
    })
    return () => {
      active = false
    }
  }, [leagues])

  if (cards.length === 0) return null

  return (
    <section className="top-three-board">
      {cards.map(({ league, top }) => (
        <article key={league.code} className="top-three-card">
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