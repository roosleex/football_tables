import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import {
  translations,
  leagueNames,
  countryNames,
  teamNamesUk,
  teamNamesUkByName,
  type Language,
  type Translation,
} from './translations'
import { getCookie, setCookie } from '../utils/cookies'

interface LanguageContextValue {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: keyof Translation, params?: Record<string, string>) => string
  leagueName: (code: string) => string
  countryName: (code: string) => string
  teamName: (team: {
    id?: number | null
    name: string
    short_name?: string | null
  }) => string
}

const LanguageContext = createContext<LanguageContextValue | null>(null)

const LANGUAGE_COOKIE = 'language'

function loadLanguage(): Language {
  const stored = getCookie(LANGUAGE_COOKIE)
  return stored === 'en' || stored === 'uk' ? stored : 'en'
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>(loadLanguage)

  useEffect(() => {
    setCookie(LANGUAGE_COOKIE, language)
  }, [language])

  const value = useMemo<LanguageContextValue>(
    () => ({
      language,
      setLanguage,
      t: (key, params) => {
        let text: string = translations[language][key]
        if (params) {
          for (const [k, v] of Object.entries(params)) {
            text = text.split(`{${k}}`).join(v)
          }
        }
        return text
      },
      leagueName: (code) => leagueNames[language][code] ?? code,
      countryName: (code) => countryNames[language][code] ?? code,
      teamName: (team) => {
        const fallback = team.short_name || team.name
        if (language !== 'uk') return fallback
        const byId = team.id != null ? teamNamesUk[String(team.id)] : undefined
        const byName =
          teamNamesUkByName[team.name] ??
          (team.short_name ? teamNamesUkByName[team.short_name] : undefined)
        return byId ?? byName ?? fallback
      },
    }),
    [language],
  )

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>
}

export function useLanguage(): LanguageContextValue {
  const ctx = useContext(LanguageContext)
  if (!ctx) throw new Error('useLanguage must be used within a LanguageProvider')
  return ctx
}