import type { LeagueStandings } from '../types'

interface StandingsTableProps {
  standings: LeagueStandings
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

function formBadges(form?: string | null) {
  if (!form) return null
  return form
    .split(',')
    .slice(0, 5)
    .map((result, i) => (
      <span key={i} className={`form-badge form-${result.toLowerCase()}`}>
        {result}
      </span>
    ))
}

export function StandingsTable({ standings }: StandingsTableProps) {
  const total = standings.table.length
  return (
    <div className="standings-panel">
      <header className="standings-header">
        <h1>{standings.league.name}</h1>
        <p className="muted">
          {standings.season ? `${standings.season} season` : 'Current season'}
          <span className={`source-badge source-${standings.source}`}>
            {standings.source}
          </span>
        </p>
      </header>
      <div className="table-wrap">
        <table className="standings-table">
          <thead>
            <tr>
              <th className="col-pos">#</th>
              <th className="col-team">Team</th>
              <th title="Played">P</th>
              <th title="Won">W</th>
              <th title="Drawn">D</th>
              <th title="Lost">L</th>
              <th title="Goals for">GF</th>
              <th title="Goals against">GA</th>
              <th title="Goal difference">GD</th>
              <th title="Points">Pts</th>
              <th className="col-form">Form</th>
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
                    <span className="team-name">
                      {row.team.short_name || row.team.name}
                    </span>
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
                <td className="col-form">{formBadges(row.form)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}