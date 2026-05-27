import path from 'node:path'
import fs from 'node:fs'
import { notFound } from 'next/navigation'
import { listAvailableCourses } from '@/data/course'
import PracticeClient from './practice-client'

type Props = {
    params: {
        sourceLanguageCode: string
        targetLanguageCode: string
        skillName: string
    }
}

export async function generateStaticParams() {
    const courses = await listAvailableCourses()
    const parameters: Array<{
        sourceLanguageCode: string
        targetLanguageCode: string
        skillName: string
    }> = []

    for (const course of courses) {
        const challengeDirectory = path.join(
            process.cwd(),
            'src',
            'courses',
            course.id,
            'challenges'
        )
        try {
            const files = await fs.promises.readdir(challengeDirectory)
            for (const file of files) {
                if (file.endsWith('.json')) {
                    parameters.push({
                        sourceLanguageCode: course.uiLanguage,
                        targetLanguageCode: course.languageCode,
                        skillName: file.replaceAll('.json', ''),
                    })
                }
            }
        } catch {
            // No challenges directory for this course
        }
    }

    return parameters
}

async function loadChallenges(
    sourceLanguageCode: string,
    targetLanguageCode: string,
    skillName: string
) {
    const courses = await listAvailableCourses()
    const course = courses.find(
        (c) =>
            c.uiLanguage === sourceLanguageCode &&
            c.languageCode === targetLanguageCode
    )

    if (!course) {
        return
    }

    const challengePath = path.join(
        process.cwd(),
        'src',
        'courses',
        course.id,
        'challenges',
        `${skillName}.json`
    )

    try {
        const content = await fs.promises.readFile(challengePath, 'utf8')
        return JSON.parse(content)
    } catch {
        return
    }
}

export default async function SkillPracticePage(props: Props) {
    const { sourceLanguageCode, targetLanguageCode, skillName } = props.params
    const data = await loadChallenges(
        sourceLanguageCode,
        targetLanguageCode,
        skillName
    )

    if (!data) {
        notFound()
    }

    const challenges = data.challenges || []

    return (
        <div className="container mx-auto p-6">
            <h1 className="text-3xl font-bold mb-2 capitalize">{skillName.replaceAll('-', ' ')}</h1>
            <p className="text-muted-foreground mb-8">
                {challenges.length} challenges &middot; {data.levels} levels
            </p>
            <PracticeClient
                challenges={challenges}
                sourceCode={sourceLanguageCode}
                targetCode={targetLanguageCode}
            />
            <div className="mt-8">
                <a
                    href={`/${sourceLanguageCode}/courses/${targetLanguageCode}`}
                    className="text-sm text-muted-foreground hover:underline"
                >
                    &larr; Back to course
                </a>
            </div>
        </div>
    )
}
