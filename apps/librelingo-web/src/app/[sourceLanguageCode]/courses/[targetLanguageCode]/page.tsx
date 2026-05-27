import { getCourseDetail, getCourseId, listAvailableCourses } from '@/data/course'
import ModuleCard from '../../../module-card'
import { getLanguageLabel, getLanguageFlag } from '@/app/language-labels'

export async function generateStaticParams() {
    const courses = await listAvailableCourses()

    return courses.map((course) => ({
        sourceLanguageCode: course.uiLanguage,
        targetLanguageCode: course.languageCode,
    }))
}

type Props = {
    params: {
        sourceLanguageCode: string
        targetLanguageCode: string
    }
}

export default async function CourseHomePage({ params }: Props) {
    const courseId = await getCourseId(params)
    const detail = await getCourseDetail(courseId)
    const languageLabel = getLanguageLabel(params.targetLanguageCode)
    const flag = getLanguageFlag(params.targetLanguageCode)

    return (
        <div className="mx-auto max-w-4xl px-4 py-8">
            {/* Course header */}
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 mb-8 text-center">
                <div className="text-6xl mb-4">{flag}</div>
                <h1 className="text-3xl font-extrabold text-gray-800 mb-2">
                    {languageLabel}
                </h1>
                <p className="text-gray-500">
                    面向中文母语者 · {detail.modules?.length || 0} 个模块
                </p>
            </div>

            {/* Modules */}
            {detail.modules && detail.modules.length > 0 ? (
                <div className="space-y-6">
                    {detail.modules.map((module_, index) => (
                        <ModuleCard
                            key={index}
                            module={module_}
                            sourceCode={params.sourceLanguageCode}
                            targetCode={params.targetLanguageCode}
                        />
                    ))}
                </div>
            ) : (
                <div className="text-center py-16 text-gray-400">
                    <p className="text-lg">此课程暂无模块</p>
                </div>
            )}
        </div>
    )
}
