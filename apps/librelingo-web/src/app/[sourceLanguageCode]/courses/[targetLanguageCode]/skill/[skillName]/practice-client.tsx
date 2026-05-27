'use client'

/* eslint-disable unicorn/no-array-for-each, unicorn/prefer-spread, unicorn/new-for-builtins, unicorn/no-new-array, unicorn/no-null */

import { useState, useEffect, useCallback } from 'react'

type Challenge = {
    type: string
    formInTargetLanguage?: string
    meaningInSourceLanguage?: string
    answer?: string
    meaning?: string
}

type Props = {
    challenges: Challenge[]
}

const STORAGE_PREFIX = 'librelingo_learned_'

export default function PracticeClient({ challenges }: Props) {
    const [currentPath, setCurrentPath] = useState('')
    const [learnedSet, setLearnedSet] = useState<Set<string>>(new Set())
    const [revealedSet, setRevealedSet] = useState<Set<number>>(new Set())
    const [showNativeFirst, setShowNativeFirst] = useState(false)
    const [showAll, setShowAll] = useState(false)

    useEffect(() => {
        setCurrentPath(window.location.pathname)
    }, [])

    useEffect(() => {
        if (!currentPath) return
        const stored = localStorage.getItem(STORAGE_PREFIX + currentPath)
        if (stored) {
            setLearnedSet(new Set(JSON.parse(stored)))
        }
    }, [currentPath])

    const saveLearned = useCallback((updated: Set<string>) => {
        const array: string[] = []
        updated.forEach(value => { array.push(value) })
        localStorage.setItem(STORAGE_PREFIX + currentPath, JSON.stringify(array))
    }, [currentPath])

    const toggleLearned = useCallback((key: string) => {
        setLearnedSet((previous) => {
            const updated = new Set(previous)
            if (updated.has(key)) {
                updated.delete(key)
            } else {
                updated.add(key)
            }
            saveLearned(updated)
            return updated
        })
    }, [saveLearned])

    const toggleReveal = useCallback((index: number) => {
        setRevealedSet((previous) => {
            const updated = new Set(previous)
            if (updated.has(index)) {
                updated.delete(index)
            } else {
                updated.add(index)
            }
            return updated
        })
    }, [])

    const toggleShowAll = useCallback(() => {
        setShowAll((previous) => {
            if (previous) {
                setRevealedSet(new Set())
            } else {
                setRevealedSet(new Set(challenges.map((_, index) => index)))
            }
            return !previous
        })
    }, [challenges])

    const toggleNativeFirst = useCallback(() => {
        setShowNativeFirst((previous) => !previous)
    }, [])

    const learnedCount = learnedSet.size
    const totalCount = challenges.length

    return (
        <div>
            {/* Controls bar */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 mb-6 flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400" />
                    <span className="text-sm text-gray-600 font-medium">
                        学习进度 {learnedCount} / {totalCount}
                    </span>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={toggleShowAll}
                        className={`px-4 py-1.5 text-sm rounded-full border transition-all ${
                            showAll
                                ? 'bg-indigo-50 border-indigo-200 text-indigo-600'
                                : 'border-gray-200 text-gray-600 hover:border-gray-300'
                        }`}
                    >
                        {showAll ? '隐藏全部翻译' : '显示全部翻译'}
                    </button>
                    <button
                        onClick={toggleNativeFirst}
                        className={`px-4 py-1.5 text-sm rounded-full border transition-all ${
                            showNativeFirst
                                ? 'bg-indigo-50 border-indigo-200 text-indigo-600'
                                : 'border-gray-200 text-gray-600 hover:border-gray-300'
                        }`}
                    >
                        先显示中文
                    </button>
                </div>
            </div>

            {/* Challenge cards */}
            <div className="space-y-4">
                {challenges.map((challenge, index) => {
                    const isLearned = learnedSet.has(`${challenge.formInTargetLanguage}-${challenge.meaningInSourceLanguage}-${index}`)
                    const isRevealed = revealedSet.has(index)

                    // Generate a unique color based on index
                    const colors = ['from-indigo-50 to-white', 'from-purple-50 to-white', 'from-blue-50 to-white', 'from-pink-50 to-white', 'from-emerald-50 to-white']
                    const colorClass = colors[index % colors.length]

                    const foreign = challenge.formInTargetLanguage || challenge.answer || ''
                    const native = challenge.meaningInSourceLanguage || challenge.meaning || ''

                    return (
                        <div
                            key={index}
                            className={`bg-white rounded-xl border shadow-sm overflow-hidden transition-all duration-200 ${
                                isLearned ? 'border-emerald-200 bg-emerald-50/30' : 'border-gray-100'
                            }`}
                        >
                            <div className={`p-5 bg-gradient-to-br ${colorClass}`}>
                                <div className="flex items-start justify-between gap-4">
                                    <div className="flex-1 min-w-0">
                                        {/* Show foreign text first (or native if toggled) */}
                                        {!showNativeFirst && (
                                            <p className="text-xl font-semibold text-gray-800 mb-2 break-words">
                                                {foreign}
                                            </p>
                                        )}
                                        {showNativeFirst && isRevealed && (
                                            <p className="text-xl font-semibold text-gray-800 mb-2 break-words">
                                                {foreign}
                                            </p>
                                        )}

                                        {/* Translation */}
                                        {isRevealed ? (
                                            <p className="text-base text-gray-500 border-t border-gray-100 pt-2 mt-1">
                                                {native}
                                            </p>
                                        ) : (
                                            <button
                                                onClick={() => toggleReveal(index)}
                                                className="text-sm text-gray-400 hover:text-indigo-500 transition-colors mt-1"
                                            >
                                                点击显示翻译 →
                                            </button>
                                        )}

                                        {/* Show native first mode */}
                                        {showNativeFirst && !isRevealed && (
                                            <div>
                                                <p className="text-xl font-semibold text-gray-500 mb-2 break-words">
                                                    {native}
                                                </p>
                                                <button
                                                    onClick={() => toggleReveal(index)}
                                                    className="text-sm text-gray-400 hover:text-indigo-500 transition-colors"
                                                >
                                                    点击显示外语 →
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                    <div className="flex flex-col gap-1.5 shrink-0">
                                        <button
                                            onClick={() => toggleReveal(index)}
                                            className={`px-3 py-1 text-xs rounded-lg border transition-all ${
                                                isRevealed
                                                    ? 'bg-gray-50 border-gray-200 text-gray-500'
                                                    : 'border-gray-200 text-gray-400 hover:border-indigo-200 hover:text-indigo-500'
                                            }`}
                                        >
                                            {isRevealed ? '隐藏' : '显示'}
                                        </button>
                                        <button
                                            onClick={() => toggleLearned(`${challenge.formInTargetLanguage}-${challenge.meaningInSourceLanguage}-${index}`)}
                                            className={`px-3 py-1 text-xs rounded-lg border transition-all ${
                                                isLearned
                                                    ? 'bg-emerald-50 border-emerald-200 text-emerald-600'
                                                    : 'border-gray-200 text-gray-400 hover:border-emerald-200 hover:text-emerald-600'
                                            }`}
                                        >
                                            {isLearned ? '已掌握 ✓' : '标记已学'}
                                        </button>
                                    </div>
                                </div>
                            </div>
                            {/* Progress bar at bottom */}
                            {isLearned && (
                                <div className="h-1 bg-emerald-400 w-full" />
                            )}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
