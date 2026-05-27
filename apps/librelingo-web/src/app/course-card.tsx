import { Button } from '@/components/ui/button'
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import { Course } from '@/data/course'
import Link from 'next/link'
import { getLanguageLabel, getSourceLabel } from './language-labels'

type Props = {
    course: Course
}

export default function CourseCard(props: Props) {
    const { course } = props
    const coursePageUrl = `/${course.uiLanguage}/courses/${course.languageCode}`
    const targetLabel = getLanguageLabel(course.languageCode)
    const sourceLabel = getSourceLabel(course.uiLanguage)

    return (
        <Card>
            <CardHeader>
                <CardTitle>{sourceLabel} → {targetLabel}</CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-muted-foreground">
                    学习 {targetLabel} · 面向中文母语者
                </p>
            </CardContent>
            <CardFooter>
                <Button asChild>
                    <Link href={coursePageUrl}>开始学习</Link>
                </Button>
            </CardFooter>
        </Card>
    )
}
