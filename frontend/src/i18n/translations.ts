export type Language = 'en' | 'uk'

export interface Translation {
  appTitle: string
  loading: string
  loadError: string
  standingsError: string
  selectHint: string
  lastUpdated: string
  currentSeason: string
  season: string
  team: string
  played: string
  won: string
  drawn: string
  lost: string
  goalsFor: string
  goalsAgainst: string
  goalDifference: string
  points: string
  form: string
  playedFull: string
  wonFull: string
  drawnFull: string
  lostFull: string
  goalsForFull: string
  goalsAgainstFull: string
  goalDifferenceFull: string
  pointsFull: string
  formWin: string
  formDraw: string
  formLoss: string
  live: string
  demo: string
}

export const translations: Record<Language, Translation> = {
  en: {
    appTitle: 'Football Tables',
    loading: 'Loading…',
    loadError: 'Could not load leagues. Is the backend running?',
    standingsError: 'Could not load standings.',
    selectHint: 'Select a league to begin.',
    lastUpdated: 'Last updated',
    currentSeason: 'Current season',
    season: '{season} season',
    team: 'Team',
    played: 'P',
    won: 'W',
    drawn: 'D',
    lost: 'L',
    goalsFor: 'GF',
    goalsAgainst: 'GA',
    goalDifference: 'GD',
    points: 'Pts',
    form: 'Form',
    playedFull: 'Played',
    wonFull: 'Won',
    drawnFull: 'Drawn',
    lostFull: 'Lost',
    goalsForFull: 'Goals for',
    goalsAgainstFull: 'Goals against',
    goalDifferenceFull: 'Goal difference',
    pointsFull: 'Points',
    formWin: 'W',
    formDraw: 'D',
    formLoss: 'L',
    live: 'live',
    demo: 'demo',
  },
  uk: {
    appTitle: 'Футбольні таблиці',
    loading: 'Завантаження…',
    loadError: 'Не вдалося завантажити ліги. Перевірте, чи запущено сервер.',
    standingsError: 'Не вдалося завантажити турнірну таблицю.',
    selectHint: 'Оберіть лігу, щоб розпочати.',
    lastUpdated: 'Останнє оновлення',
    currentSeason: 'Поточний сезон',
    season: 'Сезон {season}',
    team: 'Команда',
    played: 'І',
    won: 'В',
    drawn: 'Н',
    lost: 'П',
    goalsFor: 'ГЗ',
    goalsAgainst: 'ГП',
    goalDifference: 'РМ',
    points: 'О',
    form: 'Форма',
    playedFull: 'Ігри',
    wonFull: 'Виграші',
    drawnFull: 'Нічиї',
    lostFull: 'Поразки',
    goalsForFull: 'Голи забиті',
    goalsAgainstFull: 'Голи пропущені',
    goalDifferenceFull: "Різниця м'ячів",
    pointsFull: 'Очки',
    formWin: 'В',
    formDraw: 'Н',
    formLoss: 'П',
    live: 'реальні',
    demo: 'демо',
  },
}

export const leagueNames: Record<Language, Record<string, string>> = {
  en: {
    PL: 'Premier League',
    PD: 'La Liga',
    BL1: 'Bundesliga',
    SA: 'Serie A',
    FL1: 'Ligue 1',
    DED: 'Eredivisie',
    comp_premier_league_ukr: 'Ukrainian Premier League',
    comp_pro_league_be: 'Belgian Pro League',
    comp_super_lig_tr: 'Turkish Süper Lig',
  },
  uk: {
    PL: "Прем'єр-ліга",
    PD: 'Ла Ліга',
    BL1: 'Бундесліга',
    SA: 'Серія А',
    FL1: 'Ліга 1',
    DED: 'Ередивізі',
    comp_premier_league_ukr: "Українська Прем'єр-ліга",
    comp_pro_league_be: 'Бельгійська Про-ліга',
    comp_super_lig_tr: 'Турецька Суперліга',
  },
}

export const countryNames: Record<Language, Record<string, string>> = {
  en: {
    GB: 'England',
    ES: 'Spain',
    DE: 'Germany',
    IT: 'Italy',
    FR: 'France',
    NL: 'Netherlands',
    UKR: 'Ukraine',
    BEL: 'Belgium',
    TUR: 'Turkey',
  },
  uk: {
    GB: 'Англія',
    ES: 'Іспанія',
    DE: 'Німеччина',
    IT: 'Італія',
    FR: 'Франція',
    NL: 'Нідерланди',
    UKR: 'Україна',
    BEL: 'Бельгія',
    TUR: 'Туреччина',
  },
}

// football-data.org team id -> Ukrainian name (English is shown unchanged).
// Any team not listed here simply falls back to its original name.
export const teamNamesUk: Record<string, string> = {
  // Premier League
  '1044': 'Борнмут',
  '57': 'Арсенал',
  '58': 'Астон Вілла',
  '402': 'Брентфорд',
  '397': 'Брайтон',
  '61': 'Челсі',
  '1076': 'Ковентрі Сіті',
  '354': 'Крістал Пелес',
  '62': 'Евертон',
  '63': 'Фулгем',
  '322': 'Галл Сіті',
  '349': 'Іпсвіч Таун',
  '341': 'Лідс Юнайтед',
  '64': 'Ліверпуль',
  '65': 'Манчестер Сіті',
  '66': 'Манчестер Юнайтед',
  '67': 'Ньюкасл Юнайтед',
  '351': 'Ноттінгем Форест',
  '71': 'Сандерленд',
  '73': 'Тоттенгем',
  // La Liga
  '77': 'Атлетік Більбао',
  '79': 'Осасуна',
  '78': 'Атлетіко Мадрид',
  '263': 'Алавес',
  '285': 'Ельче',
  '81': 'Барселона',
  '82': 'Хетафе',
  '88': 'Леванте',
  '84': 'Малага',
  '87': 'Райо Вальєкано',
  '558': 'Сельта',
  '560': 'Депортіво Ла-Корунья',
  '80': 'Еспаньйол',
  '90': 'Реал Бетіс',
  '86': 'Реал Мадрид',
  '5335': 'Расінг Сантандер',
  '92': 'Реал Сосьєдад',
  '559': 'Севілья',
  '95': 'Валенсія',
  '94': 'Вільярреал',
  // Serie A
  '98': 'Мілан',
  '5911': 'Монца',
  '99': 'Фіорентина',
  '100': 'Рома',
  '102': 'Аталанта',
  '103': 'Болонья',
  '104': 'Кальярі',
  '7397': 'Комо',
  '108': 'Інтер',
  '470': 'Фрозіноне',
  '107': 'Дженоа',
  '109': 'Ювентус',
  '112': 'Парма',
  '110': 'Лаціо',
  '113': 'Наполі',
  '586': 'Торіно',
  '115': 'Удінезе',
  '5890': 'Лечче',
  '471': 'Сассуоло',
  '454': 'Венеція',
  // Ligue 1
  '519': 'Осер',
  '532': 'Анже',
  '548': 'Монако',
  '531': 'Труа',
  '525': "Лор'ян",
  '533': 'Гавр',
  '535': 'Ле-Ман',
  '521': 'Лілль',
  '522': 'Ніцца',
  '516': 'Марсель',
  '523': 'Ліон',
  '1045': 'Парі ФК',
  '524': 'Парі Сен-Жермен',
  '546': 'Ланс',
  '576': 'Страсбур',
  '512': 'Брест',
  '529': 'Ренн',
  '511': 'Тулуза',
  // Eredivisie
  '680': 'АДО Ден Хааг',
  '678': 'Аякс',
  '682': 'АЗ Алкмар',
  '677': 'Гронінген',
  '666': 'Твенте',
  '676': 'Утрехт',
  '675': 'Феєнорд',
  '1920': 'Фортуна Сіттард',
  '718': 'Гоу Ехед Іглз',
  '1915': 'НЕК Неймеген',
  '684': 'ПЕК Зволле',
  '674': 'ПСВ',
  '670': 'Ексельсіор',
  '1909': 'Камбуур',
  '673': 'Геренвен',
  '6806': 'Спарта Роттердам',
  '1912': 'Телстар',
  '672': 'Віллем II',
  // Bundesliga (well-known clubs by their stable ids)
  '5': 'Баварія',
  '4': 'Боруссія Дортмунд',
  '721': 'РБ Лейпциг',
  '3': 'Баєр Леверкузен',
  '19': 'Айнтрахт Франкфурт',
  '10': 'Штутгарт',
  '18': 'Боруссія Менхенгладбах',
  '17': 'Фрайбург',
  '11': 'Вольфсбург',
  '12': 'Вердер Бремен',
  '2': 'Гоффенгайм',
  '15': 'Майнц',
  '28': 'Уніон Берлін',
  '16': 'Аугсбург',
  '6': 'Бохум',
}

// openfootapi Ukrainian Premier League team name -> Ukrainian name (Cyrillic).
export const teamNamesUkByName: Record<string, string> = {
  'Polissya Zhytomyr': 'Полісся Житомир',
  'Shakhtar Donetsk': 'Шахтар Донецьк',
  'Dynamo Kyiv': 'Динамо Київ',
  'FC Kharkiv': 'ФК Харків',
  'Karpaty': 'Карпати',
  'Zorya': 'Зоря',
  'LNZ Cherkasy': 'ЛНЗ Черкаси',
  'FC Kolos Kovalivka': 'Колос Ковалівка',
  'Livyi Bereh': 'Лівий Берег',
  'Chornomorets Odesa': 'Чорноморець Одеса',
  'Epitsentr Kamianets-Podilskyi': "Епіцентр Кам'янець-Подільський",
  'Bukovyna Chernivtsi': 'Буковина Чернівці',
  'Veres Rivne': 'Верес Рівне',
  'Obolon Kyiv': 'Оболонь Київ',
  'Kryvbas': 'Кривбас',
  'Kudrivka': 'Кудрівка',
  // Belgian Pro League
  'Club Brugge': 'Брюгге',
  'St. Gilloise': 'Юніон Сен-Жилуаз',
  'Gent': 'Гент',
  'Charleroi': 'Шарлеруа',
  'Anderlecht': 'Андерлехт',
  'Genk': 'Генк',
  'Lommel SK': 'Ломмел',
  'Westerlo': 'Вестерло',
  'Standard': 'Стандард Льєж',
  'Mechelen': 'Мехелен',
  'Waregem': 'Варегем',
  'Antwerp': 'Антверпен',
  'Beveren': 'Беверен',
  'Oud-Heverlee Leuven': 'Ауд-Геверле Левен',
  'St Truiden': 'Сінт-Трейден',
  "RAAL La Louviere": "Ла-Лув'єр",
  'Cercle Brugge': 'Серкль Брюгге',
  'Kortrijk': 'Кортрейк',
  // Turkish Süper Lig
  'Galatasaray': 'Галатасарай',
  'Amedspor': 'Амедспор',
  'Trabzonspor': 'Трабзонспор',
  'Besiktas': 'Бешикташ',
  'Kasimpasa': 'Касимпаша',
  'Fenerbahce': 'Фенербахче',
  'Corum': 'Чорум',
  'Kocaelispor': 'Коджаеліспор',
  'Goztep': 'Гезтепе',
  'Buyuksehyr': 'Бююкшехір',
  'Erzurumspor': 'Ерзурумспор',
  'Alanyaspor': 'Аланьяспор',
  'Rizespor': 'Ризеспор',
  'Genclerbirligi': 'Генчлербірлігі',
  'Konyaspor': 'Коньяспор',
  'Gaziantep': 'Газіантеп',
  'Samsunspor': 'Самсунспор',
  'Eyupspor': 'Еюпспор',
}