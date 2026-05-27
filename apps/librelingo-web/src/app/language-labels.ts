const languageLabels: Record<string, string> = {
    en: '英语',
    ja: '日语',
    ko: '韩语',
    fr: '法语',
    de: '德语',
    es: '西班牙语',
    it: '意大利语',
    pt: '葡萄牙语',
    ru: '俄语',
    'zh': '中文',
    'th': '泰语',
}

const languageFlags: Record<string, string> = {
    en: '🇬🇧',
    ja: '🇯🇵',
    ko: '🇰🇷',
    fr: '🇫🇷',
    de: '🇩🇪',
    es: '🇪🇸',
    it: '🇮🇹',
    pt: '🇵🇹',
    ru: '🇷🇺',
    'zh': '🇨🇳',
    'th': '🇹🇭',
}

const moduleLabels: Record<string, string> = {
    Basics: '基础入门',
    'Food & Drink': '饮食',
    Conversations: '对话练习',
    'Numbers': '数字',
}

const skillLabels: Record<string, string> = {
    greetings: '问候',
    numbers: '数字',
    'basic-foods': '基础食物',
    'restaurant-dialogues': '餐厅对话',
    'shopping-dialogues': '购物对话',
    'travel-dialogues': '旅行对话',
    'hotel-accommodation': '酒店住宿',
    animals: '动物',
    'cards-test': '卡片测试',
    'chips-test-0': '筹码测试',
}

export function getLanguageLabel(code: string): string {
    return languageLabels[code] || code
}

export function getSourceLabel(code: string): string {
    if (code === 'zh') return '中文'
    return languageLabels[code] || code
}

export function getLanguageFlag(code: string): string {
    return languageFlags[code] || '🌐'
}

export function getModuleLabel(title: string): string {
    return moduleLabels[title] || title
}

export function getSkillLabel(href: string): string {
    return skillLabels[href] || href
}
