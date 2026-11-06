// Convert football-data.org's ISO 3166-1 alpha-3 area codes to alpha-2 so we
// can build the matching flag emoji.
const ALPHA2: Record<string, string> = {
  ENG: 'GB', SCO: 'GB', WAL: 'GB', NIR: 'GB',
  DEU: 'DE', ESP: 'ES', ITA: 'IT', FRA: 'FR', NLD: 'NL', POR: 'PT',
  BEL: 'BE', AUT: 'AT', CHE: 'CH', TUR: 'TR', RUS: 'RU', UKR: 'UA',
  POL: 'PL', CZE: 'CZ', SVK: 'SK', HUN: 'HU', ROU: 'RO', BGR: 'BG',
  HRV: 'HR', SRB: 'RS', SVN: 'SI', BIH: 'BA', MNE: 'ME', MKD: 'MK',
  ALB: 'AL', GRC: 'GR', CYP: 'CY', DNK: 'DK', SWE: 'SE', NOR: 'NO',
  FIN: 'FI', ISL: 'IS', IRL: 'IE', LUX: 'LU', MLT: 'MT', EST: 'EE',
  LVA: 'LV', LTU: 'LT', BLR: 'BY', MDA: 'MD', ARM: 'AM', AZE: 'AZ',
  GEO: 'GE', ISR: 'IL', KAZ: 'KZ', FRO: 'FO', GIB: 'GI', AND: 'AD',
  SMR: 'SM', LIE: 'LI', KOS: 'XK',
}

function toAlpha2(countryCode: string): string | null {
  const code = countryCode.trim().toUpperCase()
  if (/^[A-Z]{2}$/.test(code)) return code
  return ALPHA2[code] ?? null
}

function flagEmoji(alpha2: string): string {
  return Array.from(alpha2.toUpperCase())
    .map((ch) => String.fromCodePoint(0x1f1e6 + ch.charCodeAt(0) - 65))
    .join('')
}

export function Flag({ countryCode }: { countryCode: string }) {
  const alpha2 = toAlpha2(countryCode)
  return (
    <span className="flag" aria-hidden="true">
      {alpha2 ? flagEmoji(alpha2) : '🏳️'}
    </span>
  )
}