import { useState } from 'react'
import type { League } from '../types'
import { Flag } from './Flag'
import { useLanguage } from '../i18n/LanguageContext'

const REGIONS = ['Europe', 'Asia', 'North America'] as const

const REGION_LABELS: Record<(typeof REGIONS)[number], 'europe' | 'asia' | 'northAmerica'> = {
  Europe: 'europe',
  Asia: 'asia',
  'North America': 'northAmerica',
}

interface LeagueListProps {
  leagues: League[]
  selectedCode: string | null
  activeRegion: string
  onSelectLeague: (code: string) => void
  onSelectRegion: (region: string) => void
}

export function LeagueList({
  leagues,
  selectedCode,
  activeRegion,
  onSelectLeague,
  onSelectRegion,
}: LeagueListProps) {
  const { t, leagueName, countryName } = useLanguage()
  const [openRegion, setOpenRegion] = useState<string | null>(null)

  const handleRegionClick = (region: string) => {
    // Selecting a region opens its overview (top-3 board) and toggles its submenu.
    onSelectRegion(region)
    setOpenRegion((prev) => (prev === region ? null : region))
  }

  return (
    <nav className="league-list" aria-label="Leagues">
      {REGIONS.map((region) => (
        <div key={region} className="league-group">
          <button
            type="button"
            className={`group-item ${selectedCode === null && activeRegion === region ? 'active' : ''}`}
            onClick={() => handleRegionClick(region)}
            aria-expanded={openRegion === region}
          >
            <span className="group-label">{t(REGION_LABELS[region])}</span>
            <span className="group-arrow" aria-hidden="true">
              {openRegion === region ? '▾' : '▸'}
            </span>
          </button>
          {openRegion === region && (
            <div className="league-sublist">
              {leagues
                .filter((league) => league.region === region)
                .map((league) => (
                  <button
                    key={league.code}
                    type="button"
                    className={`league-item ${league.code === selectedCode ? 'active' : ''}`}
                    onClick={() => onSelectLeague(league.code)}
                  >
                    <Flag countryCode={league.country_code} />
                    <span className="league-name">{leagueName(league.code)}</span>
                    <span className="league-country">{countryName(league.country_code)}</span>
                  </button>
                ))}
            </div>
          )}
        </div>
      ))}
    </nav>
  )
}