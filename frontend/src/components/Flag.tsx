const FLAGS: Record<string, string> = {
  GB: '🇬🇧',
  ES: '🇪🇸',
  DE: '🇩🇪',
  IT: '🇮🇹',
  FR: '🇫🇷',
  NL: '🇳🇱',
}

export function Flag({ countryCode }: { countryCode: string }) {
  return (
    <span className="flag" aria-hidden="true">
      {FLAGS[countryCode] ?? '🏳️'}
    </span>
  )
}