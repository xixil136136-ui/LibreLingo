import { getCourseDetail, getCourseId, listAvailableCourses } from '@/data/course'
import ModuleCard from '../../../module-card'

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

    return (
        <div className="container mx-auto p-6">
            <h1 className="text-3xl font-bold mb-8">
                {detail.targetLanguage.name}
            </h1>
            {detail.modules && detail.modules.length > 0 ? (
                <div>
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
                <p className="text-muted-foreground">
                    No modules available for this course.
                </p>
            )}
        </div>
    )
}
