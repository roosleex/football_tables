export interface League {
  code: string
  name: string
  country: string
  country_code: string
  emblem: string | null
}

export interface Team {
  id?: number | null
  name: string
  short_name?: string | null
  tla?: string | null
  crest?: string | null
}

export interface StandingRow {
  position: number
  team: Team
  played: number
  won: number
  drawn: number
  lost: number
  goals_for: number
  goals_against: number
  goal_difference: number
  points: number
  form?: string | null
}

export interface LeagueStandings {
  league: League
  table: StandingRow[]
  season?: string | null
  source: string
  updated_at?: string | null
}