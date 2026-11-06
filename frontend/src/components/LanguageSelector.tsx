import { useLanguage } from '../i18n/LanguageContext'
import type { Language } from '../i18n/translations'

const OPTIONS: { value: Language; label: string }[] = [
  { value: 'en', label: 'English' },
  { value: 'uk', label: 'Українська' },
]

export function LanguageSelector() {
  const { language, setLanguage } = useLanguage()
  return (
    <select
      className="language-selector"
      value={language}
      onChange={(event) => setLanguage(event.target.value as Language)}
      aria-label="Language / Мова"
    >
      {OPTIONS.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  )
}