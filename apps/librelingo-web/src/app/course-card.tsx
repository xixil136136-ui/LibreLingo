import { Course } from '@/data/course'
import Link from 'next/link'
import { getLanguageLabel, getLanguageFlag } from './language-labels'

type Props = {
    course: Course
}

export default function CourseCard(props: Props) {
    const { course } = props
    const targetLabel = getLanguageLabel(course.languageCode)
    const flag = getLanguageFlag(course.languageCode)
    const coursePageUrl = `/${course.uiLanguage}/courses/${course.languageCode}`

    return (
        <Link
            href={coursePageUrl}
            className="group block bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 ease-out overflow-hidden"
        >
            <div className="p-6 flex flex-col items-center text-center gap-3">
                <div className="text-5xl mb-1">{flag}</div>
                <h3 className="text-lg font-bold text-gray-800 group-hover:text-indigo-600 transition-colors">
                    {targetLabel}
                </h3>
                <p className="text-sm text-gray-500">
                    面向中文母语者
                </p>
                <div className="mt-2 inline-flex items-center gap-1.5 text-sm font-medium text-white bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full px-5 py-2 group-hover:shadow-lg group-hover:from-indigo-600 group-hover:to-purple-600 transition-all">
                    开始学习
                    <svg className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                </div>
            </div>
        </Link>
    )
}
