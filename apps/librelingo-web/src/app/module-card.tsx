import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ModuleSummary } from '@/data/course'
import Link from 'next/link'

type Props = {
    module: ModuleSummary
    sourceCode: string
    targetCode: string
}

export default function ModuleCard(props: Props) {
    const { module: module_, sourceCode, targetCode } = props

    return (
        <Card className="mb-6">
            <CardHeader>
                <CardTitle className="text-xl">{module_.title}</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {module_.skills.map((skill) => (
                        <Button
                            key={skill.id}
                            variant="outline"
                            asChild
                            className="h-auto py-4 px-4 justify-start flex-col items-start gap-1"
                        >
                            <Link
                                href={`/${sourceCode}/courses/${targetCode}/skill/${skill.practiceHref}`}
                            >
                                <span className="font-medium text-sm">
                                    {skill.title}
                                </span>
                                <span className="text-xs text-muted-foreground">
                                    {skill.summary.length} phrases &middot;{' '}
                                    {skill.levels} levels
                                </span>
                            </Link>
                        </Button>
                    ))}
                </div>
            </CardContent>
        </Card>
    )
}
