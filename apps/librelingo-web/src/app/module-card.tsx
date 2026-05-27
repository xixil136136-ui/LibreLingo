import { ModuleSummary } from '@/data/course'
import Link from 'next/link'
import { getModuleLabel, getSkillLabel } from './language-labels'

type Props = {
    module: ModuleSummary
    sourceCode: string
    targetCode: string
}

const moduleIcons: Record<string, string> = {
    Basics: '📖',
    'Food & Drink': '🍽️',
    Conversations: '💬',
    'Numbers': '🔢',
}

export default function ModuleCard(props: Props) {
    const { module: module_, sourceCode, targetCode } = props
    const moduleTitle = getModuleLabel(module_.title)
    const icon = moduleIcons[module_.title] || '📚'

    return (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-50 flex items-center gap-3">
                <span className="text-2xl">{icon}</span>
                <h3 className="text-lg font-bold text-gray-800">{moduleTitle}</h3>
            </div>
            <div className="p-3 space-y-2">
                {module_.skills.map((skill, index) => (
                    <Link
                        key={index}
                        href={`/${sourceCode}/courses/${targetCode}/skill/${skill.practiceHref}`}
                        className="flex items-center justify-between px-4 py-3 rounded-xl hover:bg-indigo-50 hover:border-indigo-100 border border-transparent transition-all duration-200 group"
                    >
                        <div className="flex items-center gap-3">
                            <div className="w-9 h-9 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-500 font-bold text-sm group-hover:bg-indigo-100 transition-colors">
                                {index + 1}
                            </div>
                            <div>
                                <div className="font-medium text-gray-700 group-hover:text-indigo-600 transition-colors">
                                    {getSkillLabel(skill.practiceHref)}
                                </div>
                                <div className="text-xs text-gray-400 mt-0.5">
                                    {skill.summary.length} 个短语
                                </div>
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="flex gap-1">
                                {Array.from({ length: skill.levels }, (_, index_) => (
                                    <div
                                        key={index_}
                                        className="w-2 h-2 rounded-full bg-emerald-400"
                                    />
                                ))}
                            </div>
                            <svg className="w-4 h-4 text-gray-300 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                            </svg>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    )
}
