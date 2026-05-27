import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ModuleSummary } from '@/data/course'
import Link from 'next/link'
import { getModuleLabel, getSkillLabel } from './language-labels'

type Props = {
    module: ModuleSummary
    sourceCode: string
    targetCode: string
}

export default function ModuleCard(props: Props) {
    const { module: module_, sourceCode, targetCode } = props
    const moduleTitle = getModuleLabel(module_.title)

    return (
        <Card className="mb-6">
            <CardHeader>
                <CardTitle className="text-xl">{moduleTitle}</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col gap-2">
                    {module_.skills.map((skill, index) => (
                        <Link
                            key={index}
                            href={`/${sourceCode}/courses/${targetCode}/skill/${skill.practiceHref}`}
                            className="flex justify-between items-center p-3 rounded-md border border-border hover:bg-accent transition"
                        >
                            <span className="font-medium">{getSkillLabel(skill.practiceHref)}</span>
                            <span className="text-sm text-muted-foreground">
                                {skill.summary.length} 个短语 · {skill.levels} 个等级
                            </span>
                        </Link>
                    ))}
                </div>
            </CardContent>
        </Card>
    )
}
