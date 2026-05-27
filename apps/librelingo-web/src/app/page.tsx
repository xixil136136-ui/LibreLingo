import type { Metadata } from 'next'
import { listAvailableCourses } from '@/data/course'
import CourseCard from './course-card'

export const metadata: Metadata = {
    title: 'LibreLingo - 免费语言学习平台',
    description: '免费学习多种语言，面向中文母语者',
}

export default async function Home() {
    const courseData = await listAvailableCourses()

    return (
        <>
            {/* Hero */}
            <section className="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white">
                <div className="mx-auto max-w-6xl px-4 py-20 md:py-28 text-center">
                    <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
                        免费学习一门新语言
                    </h1>
                    <p className="text-lg md:text-xl text-white/80 max-w-2xl mx-auto">
                        通过有趣的互动课程，掌握实用词汇和日常对话
                    </p>
                </div>
            </section>

            {/* Course Grid */}
            <section className="mx-auto max-w-6xl px-4 -mt-8 pb-16">
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {courseData.map((course) => (
                        <CourseCard key={course.id} course={course} />
                    ))}
                </div>
            </section>
        </>
    )
}
