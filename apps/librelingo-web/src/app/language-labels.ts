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
    th: '泰语',
    ar: '阿拉伯语',
    nl: '荷兰语',
    pl: '波兰语',
    sv: '瑞典语',
    tr: '土耳其语',
    vi: '越南语',
}

const moduleLabels: Record<string, string> = {
    Basics: '基础入门',
    'Food & Drink': '饮食',
    Conversations: '对话练习',
    Advanced: '进阶学习',
    Travel: '旅行',
    Business: '商务',
    Grammar: '语法',
    Vocabulary: '词汇',
    Pronunciation: '发音',
    Culture: '文化',
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
    'chips-test-0': '筹码测试1',
    'chips-test-1': '筹码测试2',
    'chips-test-2': '筹码测试3',
    'chips-test-3': '筹码测试4',
    colors: '颜色',
    'food-advanced': '食物进阶',
    introduction: '自我介绍',
    'numbers-advanced': '数字进阶',
    'phrases-0': '短语1',
    'phrases-1': '短语2',
    'phrases-2': '短语3',
    'phrases-3': '短语4',
    'phrases-4': '短语5',
    'phrases-5': '短语6',
    'story-0': '故事1',
    'story-1': '故事2',
    'story-2': '故事3',
    'story-3': '故事4',
    'story-4': '故事5',
    'story-5': '故事6',
    time: '时间',
}

export function getLanguageLabel(code: string): string {
    return languageLabels[code] || code
}

export function getSourceLabel(code: string): string {
    if (code === 'zh') return '中文'
    return getLanguageLabel(code)
}

export function getModuleLabel(englishName: string): string {
    return moduleLabels[englishName] || englishName
}

export function getSkillLabel(skillName: string): string {
    return skillLabels[skillName] || skillName.replaceAll('-', ' ')
}
