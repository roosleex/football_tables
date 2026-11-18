import { useState } from 'react'
import type { League } from '../types'
import { Flag } from './Flag'
import { useLanguage } from '../i18n/LanguageContext'

interface LeagueListProps {
  leagues: League[]
  selectedCode: string | null
  onSelect: (code: string | null) => void
}

export function LeagueList({ leagues, selectedCode, onSelect }: LeagueListProps) {
  const { t, leagueName, countryName } = useLanguage()
  const [open, setOpen] = useState(false)

  // "Europe" is the overview item: it is active whenever no specific league is
  // selected, and clicking it shows the top-3 board in the content area.
  const europeActive = selectedCode === null

  const handleEuropeClick = () => {
    if (selectedCode === null) {
      // Already on the Europe overview: just toggle the league submenu.
      setOpen((prev) => !prev)
    } else {
      // Coming from a specific league: show the overview and open the submenu.
      onSelect(null)
      setOpen(true)
    }
  }

  return (
    <nav className="league-list" aria-label="Leagues">
      <button
        type="button"
        className={`europe-item ${europeActive ? 'active' : ''}`}
        onClick={handleEuropeClick}
        aria-expanded={open}
      >
        <span className="europe-label">{t('europe')}</span>
        <span className="europe-arrow" aria-hidden="true">
          {open ? '▾' : '▸'}
        </span>
      </button>
      {open && (
        <div className="league-sublist">
          {leagues.map((league) => (
            <button
              key={league.code}
              type="button"
              className={`league-item ${league.code === selectedCode ? 'active' : ''}`}
              onClick={() => onSelect(league.code)}
            >
              <Flag countryCode={league.country_code} />
              <span className="league-name">{leagueName(league.code)}</span>
              <span className="league-country">{countryName(league.country_code)}</span>
            </button>
          ))}
        </div>
      )}
    </nav>
  )
}