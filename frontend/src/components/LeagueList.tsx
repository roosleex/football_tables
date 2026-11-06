import type { League } from '../types'
import { Flag } from './Flag'
import { useLanguage } from '../i18n/LanguageContext'

interface LeagueListProps {
  leagues: League[]
  selectedCode: string
  onSelect: (code: string) => void
}

export function LeagueList({ leagues, selectedCode, onSelect }: LeagueListProps) {
  const { leagueName, countryName } = useLanguage()
  return (
    <nav className="league-list" aria-label="Leagues">
      {leagues.map((league) => (
        <button
          key={league.code}
          className={`league-item ${league.code === selectedCode ? 'active' : ''}`}
          onClick={() => onSelect(league.code)}
        >
          <Flag countryCode={league.country_code} />
          <span className="league-name">{leagueName(league.code)}</span>
          <span className="league-country">{countryName(league.country_code)}</span>
        </button>
      ))}
    </nav>
  )
}