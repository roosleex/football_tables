export function getCookie(name: string): string | null {
  const prefix = `${name}=`
  const entry = document.cookie.split('; ').find((item) => item.startsWith(prefix))
  if (entry === undefined) return null
  return decodeURIComponent(entry.slice(prefix.length))
}

export function setCookie(name: string, value: string, days = 365): void {
  const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString()
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`
}

export function deleteCookie(name: string): void {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax`
}