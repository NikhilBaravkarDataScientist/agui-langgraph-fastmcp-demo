'use client'
import { useState } from 'react'

export default function ToolCard({
	tool,
	args,
	result,
}: {
	tool: string
	args?: unknown
	result?: unknown
}) {
	const [expanded, setExpanded] = useState(false)
	const isComplete = result !== undefined

	return (
		<div className="bg-gray-100 border border-gray-300 rounded px-3 py-2 text-sm my-1">
			<button
				onClick={() => setExpanded(!expanded)}
				className="flex items-center gap-2 w-full hover:opacity-75 transition-opacity"
			>
				<span className="text-lg">
					{expanded ? '▼' : '▶'}
				</span>
				<span className="font-mono font-semibold text-gray-800">{tool}</span>
				{isComplete && (
					<span className="ml-auto text-xs bg-green-200 text-green-800 px-2 py-1 rounded">
						Complete
					</span>
				)}
			</button>

			{expanded && (
				<div className="mt-2 space-y-2 ml-6 border-l-2 border-gray-300 pl-3">
					{args !== undefined && (
						<div>
							<p className="text-gray-700 font-semibold text-xs uppercase tracking-wide">Arguments</p>
							<pre className="bg-white p-2 rounded text-xs overflow-x-auto border border-gray-200">
								{JSON.stringify(args, null, 2)}
							</pre>
						</div>
					)}

					{result !== undefined && (
						<div>
							<p className="text-gray-700 font-semibold text-xs uppercase tracking-wide">Result</p>
							<pre className="bg-white p-2 rounded text-xs overflow-x-auto border border-gray-200">
								{JSON.stringify(result, null, 2)}
							</pre>
						</div>
					)}
				</div>
			)}
		</div>
	)
}
