import type { LeagueStandings } from '../types'
import { useLanguage } from '../i18n/LanguageContext'

interface StandingsTableProps {
  standings: LeagueStandings
  lastUpdated: Date | null
}

function zoneClass(position: number, total: number): string {
  if (position <= 4) return 'zone-champions-league'
  if (position <= 6) return 'zone-europa'
  if (position > total - 3) return 'zone-relegation'
  return ''
}

function initials(name: string): string {
  const words = name.split(' ')
  if (words.length === 1) return name.slice(0, 3).toUpperCase()
  return words
    .map((w) => w[0])
    .join('')
    .slice(0, 3)
    .toUpperCase()
}

function formBadges(
  form: string | null | undefined,
  label: (result: string) => string,
) {
  if (!form) return null
  return form
    .split(',')
    .slice(0, 5)
    .map((result, i) => (
      <span key={i} className={`form-badge form-${result.toLowerCase()}`}>
        {label(result)}
      </span>
    ))
}

function formatDateTime(date: Date): string {
  return date.toLocaleString(undefined, {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

export function StandingsTable({ standings, lastUpdated }: StandingsTableProps) {
  const { t, leagueName, teamName } = useLanguage()
  const total = standings.table.length
  const updatedAt = standings.updated_at
    ? new Date(standings.updated_at)
    : lastUpdated

  const resultLabel = (result: string): string => {
    if (result === 'W') return t('formWin')
    if (result === 'D') return t('formDraw')
    if (result === 'L') return t('formLoss')
    return result
  }

  return (
    <div className="standings-panel">
      <header className="standings-header">
        <h1>{leagueName(standings.league.code)}</h1>
        <p className="muted">
          {standings.season
            ? t('season', { season: standings.season })
            : t('currentSeason')}
          <span className="source-badge source-live">
            LIVE
          </span>
        </p>
        {updatedAt && (
          <p className="updated-at">
            {t('lastUpdated')}: {formatDateTime(updatedAt)}
          </p>
        )}
      </header>
      <div className="table-wrap">
        <table className="standings-table">
          <thead>
            <tr>
              <th className="col-pos">#</th>
              <th className="col-team">{t('team')}</th>
              <th title={t('playedFull')}>{t('played')}</th>
              <th title={t('wonFull')}>{t('won')}</th>
              <th title={t('drawnFull')}>{t('drawn')}</th>
              <th title={t('lostFull')}>{t('lost')}</th>
              <th title={t('goalsForFull')}>{t('goalsFor')}</th>
              <th title={t('goalsAgainstFull')}>{t('goalsAgainst')}</th>
              <th title={t('goalDifferenceFull')}>{t('goalDifference')}</th>
              <th title={t('pointsFull')}>{t('points')}</th>
              <th className="col-form">{t('form')}</th>
            </tr>
          </thead>
          <tbody>
            {standings.table.map((row) => (
              <tr
                key={`${row.team.name}-${row.position}`}
                className={zoneClass(row.position, total)}
              >
                <td className="col-pos">{row.position}</td>
                <td className="col-team">
                  <span className="team-cell">
                    {row.team.crest ? (
                      <img
                        src={row.team.crest}
                        alt=""
                        className="crest"
                        loading="lazy"
                      />
                    ) : (
                      <span className="crest crest-fallback">
                        {row.team.tla || initials(row.team.name)}
                      </span>
                    )}
                    <span className="team-name">{teamName(row.team)}</span>
                  </span>
                </td>
                <td>{row.played}</td>
                <td>{row.won}</td>
                <td>{row.drawn}</td>
                <td>{row.lost}</td>
                <td>{row.goals_for}</td>
                <td>{row.goals_against}</td>
                <td
                  className={
                    row.goal_difference > 0
                      ? 'positive'
                      : row.goal_difference < 0
                        ? 'negative'
                        : ''
                  }
                >
                  {row.goal_difference > 0
                    ? `+${row.goal_difference}`
                    : row.goal_difference}
                </td>
                <td className="points">{row.points}</td>
                <td className="col-form">{formBadges(row.form, resultLabel)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}