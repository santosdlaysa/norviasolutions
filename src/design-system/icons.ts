export type NorviaIconName = 'code' | 'data' | 'cloud' | 'shield' | 'chart' | 'users' | 'gear'

export const NORVIA_ICONS: Record<NorviaIconName, string> = {
  code: 'M9 6 3 12l6 6M15 6l6 6-6 6',
  data: 'M4 6c0-2 16-2 16 0v12c0 2-16 2-16 0V6Zm0 0c0 2 16 2 16 0M4 12c0 2 16 2 16 0',
  cloud: 'M7 18h11a4 4 0 0 0 .5-7.97A6 6 0 0 0 7 9.5 4.25 4.25 0 0 0 7 18Z',
  shield: 'm12 3 8 4v5c0 5-3.4 8-8 9-4.6-1-8-4-8-9V7l8-4Zm-4 9 3 3 5-6',
  chart: 'M4 20V4M4 20h17M7 15l4-4 3 2 5-7',
  users: 'M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3 20a6 6 0 0 1 12 0M17 6a3 3 0 0 1 0 5M17 14a5 5 0 0 1 4 6',
  gear: 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm0-5v3m0 8v3m0 5v-3m0-8H9m6 0h3M4.9 4.9 7 7m10 10 2.1 2.1M4.9 19.1 7 17m10-10 2.1-2.1',
}

export const NORVIA_ICON_GUIDELINES = {
  grid: 24,
  stroke: 1.5,
  linecap: 'round' as const,
  linejoin: 'round' as const,
}
