'use client'

import { useState } from 'react'

type Challenge = {
    type: string
    formInTargetLanguage?: string
    meaningInSourceLanguage?: string
    answer?: string
    meaning?: string
    group?: string
    id: string
    priority?: number
}

type Props = {
    challenges: Challenge[]
}

export default function PracticeClient(props: Props) {
    const { challenges } = props
    const [revealedIds, setRevealedIds] = useState<Set<string>>(new Set())
    const [knownIds, setKnownIds] = useState<Set<string>>(new Set())
    const [showAll, setShowAll] = useState(false)

    const toggleReveal = (id: string) => {
        setRevealedIds((previous) => {
            const next = new Set(previous)
            if (next.has(id)) {
                next.delete(id)
            } else {
                next.add(id)
            }
            return next
        })
    }

    const toggleKnown = (id: string) => {
        setKnownIds((previous) => {
            const next = new Set(previous)
            if (next.has(id)) {
                next.delete(id)
            } else {
                next.add(id)
            }
            return next
        })
    }

    const pairs: Array<{ foreign: string; native: string; id: string }> = []
    for (const c of challenges) {
        if (c.type === 'options' && c.formInTargetLanguage && c.meaningInSourceLanguage) {
            pairs.push({
                foreign: c.formInTargetLanguage,
                native: c.meaningInSourceLanguage,
                id: c.id,
            })
        } else if (c.type === 'listeningExercise' && c.answer && c.meaning) {
            pairs.push({
                foreign: c.answer,
                native: c.meaning,
                id: c.id,
            })
        }
    }

    const [showNativeFirst, setShowNativeFirst] = useState(false)

    return (
        <div>
            {/* Controls */}
            <div className="flex flex-wrap gap-3 mb-6">
                <button
                    onClick={() => setShowAll(!showAll)}
                    className="px-4 py-2 text-sm rounded-md border border-border hover:bg-accent transition"
                >
                    {showAll ? '隐藏全部翻译' : '显示全部翻译'}
                </button>
                <button
                    onClick={() => setShowNativeFirst(!showNativeFirst)}
                    className="px-4 py-2 text-sm rounded-md border border-border hover:bg-accent transition"
                >
                    {showNativeFirst ? '先显示外语' : '先显示中文'}
                </button>
            </div>

            {/* Progress bar */}
            <div className="mb-6">
                <div className="flex justify-between text-sm mb-1">
                    <span>学习进度</span>
                    <span>已学 {knownIds.size} / {pairs.length}</span>
                </div>
                <div className="h-2 bg-secondary rounded-full overflow-hidden">
                    <div
                        className="h-full bg-green-500 rounded-full transition-all"
                        style={{ width: `${(knownIds.size / Math.max(pairs.length, 1)) * 100}%` }}
                    />
                </div>
            </div>

            {/* Challenge Cards */}
            <div className="grid grid-cols-1 gap-4">
                {pairs.map((pair) => {
                    const isRevealed = showAll || revealedIds.has(pair.id)
                    const isKnown = knownIds.has(pair.id)

                    const displayTarget = showNativeFirst ? pair.native : pair.foreign
                    const displayHidden = showNativeFirst ? pair.foreign : pair.native

                    return (
                        <div
                            key={pair.id}
                            className={`rounded-lg border p-4 transition-colors ${
                                isKnown
                                    ? 'border-green-300 bg-green-50 dark:bg-green-950/20 dark:border-green-800'
                                    : 'border-border bg-card'
                            }`}
                        >
                            <div className="flex items-start justify-between">
                                <div className="flex-1">
                                    <p className="text-lg font-medium mb-1">
                                        {displayTarget}
                                    </p>
                                    {isRevealed ? (
                                        <p className="text-muted-foreground">
                                            {displayHidden}
                                        </p>
                                    ) : (
                                        <button
                                            onClick={() => toggleReveal(pair.id)}
                                            className="text-sm text-blue-500 hover:underline"
                                        >
                                            点击显示翻译
                                        </button>
                                    )}
                                </div>
                                <div className="flex gap-2 ml-4">
                                    <button
                                        onClick={() => toggleReveal(pair.id)}
                                        className="px-3 py-1 text-xs rounded-md border border-border hover:bg-accent transition"
                                    >
                                        {isRevealed ? '隐藏' : '显示'}
                                    </button>
                                    <button
                                        onClick={() => toggleKnown(pair.id)}
                                        className={`px-3 py-1 text-xs rounded-md border transition ${
                                            isKnown
                                                ? 'bg-green-500 text-white border-green-500'
                                                : 'border-border hover:bg-accent'
                                        }`}
                                    >
                                        {isKnown ? '已掌握' : '标记已学'}
                                    </button>
                                </div>
                            </div>
                        </div>
                    )
                })}
            </div>

            {/* Empty state */}
            {pairs.length === 0 && (
                <p className="text-center text-muted-foreground py-12">
                    暂无练习内容
                </p>
            )}
        </div>
    )
}
