import './globals.css'
import { Inter as FontSans } from 'next/font/google'
import Link from 'next/link'

import { cn } from '@/lib/utils'

const fontSans = FontSans({
    subsets: ['latin'],
    variable: '--font-sans',
})

type RootLayoutProps = {
    children: React.ReactNode
}

export default function RootLayout({ children }: RootLayoutProps) {
    return (
        <html lang="zh">
            <head />
            <body className={cn('font-sans antialiased bg-[#f0f4f8]', fontSans.variable)}>
                <header className="sticky top-0 z-50 w-full bg-white/90 backdrop-blur-sm border-b border-gray-100">
                    <div className="mx-auto max-w-6xl px-4 h-16 flex items-center justify-between">
                        <Link href="/" className="flex items-center gap-2">
                            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm shadow-md">
                                L
                            </div>
                            <span className="text-xl font-bold text-gray-800">LibreLingo</span>
                        </Link>
                        <div className="flex items-center gap-3">
                            <span className="text-sm text-gray-500 bg-gray-100 px-3 py-1.5 rounded-full">
                                中文母语者
                            </span>
                        </div>
                    </div>
                </header>
                <main className="min-h-screen">
                    {children}
                </main>
                <footer className="bg-slate-800 text-slate-400 mt-20">
                    <div className="mx-auto max-w-6xl px-4 py-10">
                        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-xs shadow">
                                    L
                                </div>
                                <span className="text-lg font-bold text-white">LibreLingo</span>
                            </div>
                            <p className="text-sm text-slate-500">
                                免费语言学习平台 · 面向中文母语者
                            </p>
                        </div>
                    </div>
                </footer>
            </body>
        </html>
    )
}
