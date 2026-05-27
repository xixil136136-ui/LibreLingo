import path from 'node:path'
import fs from 'node:fs'
import { notFound } from 'next/navigation'
import { listAvailableCourses } from '@/data/course'
import PracticeClient from './practice-client'
import { getLanguageLabel, getLanguageFlag, getSkillLabel } from '@/app/language-labels'

type Props = {
    params: {
        sourceLanguageCode: string
        targetLanguageCode: string
        skillName: string
    }
}

type Challenge = {
    type: string
    formInTargetLanguage?: string
    meaningInSourceLanguage?: string
    answer?: string
    meaning?: string
}

type SkillData = {
    challenges: Challenge[]
}

export async function generateStaticParams() {
    const courses = await listAvailableCourses()
    const parameters: Props['params'][] = []

    for (const course of courses) {
        const challengesDirectory = path.join(
            process.cwd(),
            'src',
            'courses',
            `${course.uiLanguage}-${course.languageCode}`,
            'challenges'
        )

        try {
            const files = await fs.promises.readdir(challengesDirectory)
            for (const file of files) {
                if (file.endsWith('.json')) {
                    parameters.push({
                        sourceLanguageCode: course.uiLanguage,
                        targetLanguageCode: course.languageCode,
                        skillName: file.replace('.json', ''),
                    })
                }
            }
        } catch {
            continue
        }
    }

    return parameters
}

export default async function SkillPage({ params }: Props) {
    const { sourceLanguageCode, targetLanguageCode, skillName } = params
    const langLabel = getLanguageLabel(targetLanguageCode)
    const flag = getLanguageFlag(targetLanguageCode)
    const skillLabel = getSkillLabel(skillName)

    const challengesPath = path.join(
        process.cwd(),
        'src',
        'courses',
        `${sourceLanguageCode}-${targetLanguageCode}`,
        'challenges',
        `${skillName}.json`
    )

    let skillData: SkillData

    try {
        const content = await fs.promises.readFile(challengesPath, 'utf8')
        skillData = JSON.parse(content)
    } catch {
        notFound()
    }

    if (!skillData.challenges || skillData.challenges.length === 0) {
        notFound()
    }

    return (
        <div className="mx-auto max-w-3xl px-4 py-8">
            {/* Skill header */}
            <div className="mb-8">
                <a
                    href={`/${sourceLanguageCode}/courses/${targetLanguageCode}`}
                    className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-indigo-500 transition-colors mb-4"
                >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
                    </svg>
                    返回课程
                </a>
                <div className="flex items-center gap-3">
                    <span className="text-3xl">{flag}</span>
                    <div>
                        <h1 className="text-2xl font-extrabold text-gray-800">{skillLabel}</h1>
                        <p className="text-sm text-gray-500">
                            {langLabel} · {skillData.challenges.length} 个练习
                        </p>
                    </div>
                </div>
            </div>

            <PracticeClient challenges={skillData.challenges} targetLanguageCode={targetLanguageCode} />
        </div>
    )
}
