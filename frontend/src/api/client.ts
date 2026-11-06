import type { League, LeagueStandings } from '../types'

const API_BASE = '/api'

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`)
  if (!response.ok) {
    throw new Error(`Request failed (${response.status}) for ${path}`)
  }
  return (await response.json()) as T
}

export function fetchLeagues(): Promise<League[]> {
  return request<League[]>('/leagues')
}

export function fetchStandings(leagueCode: string): Promise<LeagueStandings> {
  return request<LeagueStandings>(`/leagues/${leagueCode}/standings`)
}