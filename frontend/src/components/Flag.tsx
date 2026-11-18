import { useState } from 'react'

// Map ISO 3166-1 alpha-3 area codes (football-data.org / openfootapi) to the
// alpha-2 code used by flagcdn.com, and render the flag as a real image.
// Windows does not ship colour flag emoji, so the previous emoji approach
// rendered two regional-indicator letters (e.g. "GB" / "FR") on laptops.
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
  JPN: 'JP', KOR: 'KR', AUS: 'AU', CHN: 'CN', IND: 'IN', QAT: 'QA',
  ARE: 'AE', SAU: 'SA', IRN: 'IR', UZB: 'UZ', THA: 'TH', IRQ: 'IQ',
  VNM: 'VN', IDN: 'ID',
}

const FLAG_CDN = 'https://flagcdn.com'

function toAlpha2(countryCode: string): string | null {
  const code = countryCode.trim().toUpperCase()
  if (/^[A-Z]{2}$/.test(code)) return code
  return ALPHA2[code] ?? null
}

export function Flag({ countryCode }: { countryCode: string }) {
  const [failed, setFailed] = useState(false)
  const alpha2 = toAlpha2(countryCode)

  return (
    <span className="flag" aria-hidden="true">
      {alpha2 && !failed ? (
        <img
          className="flag-img"
          src={`${FLAG_CDN}/${alpha2.toLowerCase()}.svg`}
          alt=""
          loading="lazy"
          onError={() => setFailed(true)}
        />
      ) : (
        <span className="flag-emoji">🏳️</span>
      )}
    </span>
  )
}