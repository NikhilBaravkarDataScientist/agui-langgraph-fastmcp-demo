import React from "react"

type MessageRole = "user" | "assistant"

type BarChartSpec = {
	type: "bar"
	title?: string
	labels: string[]
	values: number[]
}

type LineChartSpec = {
	type: "line"
	title?: string
	labels: string[]
	values: number[]
}

type OpenJsonUiNode = {
	type: string
	text?: string
	items?: Array<string | OpenJsonUiNode>
	columns?: string[]
	rows?: Array<Array<string | number>>
	labels?: string[]
	values?: number[]
	title?: string
	props?: Record<string, unknown>
	children?: OpenJsonUiNode[]
}

type ParsedContent = {
	text: string
	chart?: BarChartSpec
	lineChart?: LineChartSpec
	ui?: OpenJsonUiNode | OpenJsonUiNode[]
}

function parseContent(content: string): ParsedContent {
	const uiBlock = /```open-json-ui\s*([\s\S]*?)```/i.exec(content)
	const uiAltBlock = /```json-ui\s*([\s\S]*?)```/i.exec(content)
	const matchedUi = uiBlock ?? uiAltBlock
	let ui: OpenJsonUiNode | OpenJsonUiNode[] | undefined

	if (matchedUi) {
		const jsonText = matchedUi[1].trim()
		try {
			const parsed = JSON.parse(jsonText)
			if (parsed) {
				ui = parsed as OpenJsonUiNode | OpenJsonUiNode[]
			}
		} catch {
			ui = undefined
		}
	}

	const chartBlock = /```chart\s*([\s\S]*?)```/i.exec(content)
	let chart: BarChartSpec | undefined
	let lineChart: LineChartSpec | undefined
	if (chartBlock) {
		const jsonText = chartBlock[1].trim()
		try {
			const parsed = JSON.parse(jsonText)
			if (
				parsed &&
				parsed.type === "bar" &&
				Array.isArray(parsed.labels) &&
				Array.isArray(parsed.values)
			) {
				chart = parsed as BarChartSpec
			} else if (
				parsed &&
				parsed.type === "line" &&
				Array.isArray(parsed.labels) &&
				Array.isArray(parsed.values)
			) {
				lineChart = parsed as LineChartSpec
			}
		} catch {
			chart = undefined
			lineChart = undefined
		}
	}

	let text = content
	if (matchedUi) {
		text = text.replace(matchedUi[0], "")
	}
	if (chartBlock) {
		text = text.replace(chartBlock[0], "")
	}
	text = text.trim()

	return { text, chart, lineChart, ui }
}

function BarChart({ spec }: { spec: BarChartSpec }) {
	const maxValue = Math.max(...spec.values, 1)
	return (
		<div className="mt-3 rounded-lg border border-gray-200 bg-white p-3">
			{spec.title && (
				<div className="text-sm font-semibold text-gray-800 mb-2">{spec.title}</div>
			)}
			<div className="flex items-end gap-3 h-40">
				{spec.values.map((value, idx) => {
					const height = Math.round((value / maxValue) * 100)
					const label = spec.labels[idx] ?? String(idx + 1)
					return (
						<div key={idx} className="flex-1 flex flex-col items-center gap-2">
							<div className="w-full flex items-end justify-center h-28">
								<div
									className="w-8 rounded-t bg-blue-500"
									style={{ height: `${height}%` }}
									title={`${label}: ${value}`}
								/>
							</div>
							<div className="text-xs text-gray-600 text-center leading-tight">
								{label}
							</div>
							<div className="text-xs text-gray-500">{value}</div>
						</div>
					)
				})}
			</div>
		</div>
	)
}

function LineChart({ spec }: { spec: LineChartSpec }) {
	const width = 520
	const height = 160
	const padding = 24
	const maxValue = Math.max(...spec.values, 1)
	const minValue = Math.min(...spec.values, 0)
	const range = Math.max(maxValue - minValue, 1)

	const points = spec.values.map((value, idx) => {
		const x = padding + (idx / Math.max(spec.values.length - 1, 1)) * (width - padding * 2)
		const y = padding + (1 - (value - minValue) / range) * (height - padding * 2)
		return [x, y]
	})

	const path = points
		.map((point, idx) => `${idx === 0 ? "M" : "L"}${point[0]},${point[1]}`)
		.join(" ")

	return (
		<div className="mt-3 rounded-lg border border-gray-200 bg-white p-3">
			{spec.title && (
				<div className="text-sm font-semibold text-gray-800 mb-2">{spec.title}</div>
			)}
			<svg viewBox={`0 0 ${width} ${height}`} className="w-full h-40">
				<path d={path} fill="none" stroke="#3b82f6" strokeWidth="2" />
				{points.map((point, idx) => (
					<circle key={idx} cx={point[0]} cy={point[1]} r={3} fill="#2563eb" />
				))}
			</svg>
			<div className="flex justify-between text-xs text-gray-600 mt-2">
				{spec.labels.map((label, idx) => (
					<span key={idx} className="flex-1 text-center truncate">
						{label}
					</span>
				))}
			</div>
		</div>
	)
}

function renderUiNode(node: OpenJsonUiNode, key?: number) {
	switch (node.type) {
		case "text":
			return (
				<p key={key} className="whitespace-pre-wrap">
					{node.text ?? String(node.props?.text ?? "")}
				</p>
			)
		case "list":
			return (
				<ul key={key} className="list-disc pl-6 space-y-1">
					{(node.items ?? []).map((item, idx) => (
						<li key={idx}>
							{typeof item === "string" ? item : renderUiNode(item)}
						</li>
					))}
				</ul>
			)
		case "table":
			return (
				<div key={key} className="overflow-x-auto">
					<table className="w-full text-sm border-collapse">
						{node.columns && (
							<thead>
								<tr>
									{node.columns.map((col, idx) => (
										<th
											key={idx}
											className="text-left border-b border-gray-200 pb-1 pr-3"
										>
											{col}
										</th>
									))}
								</tr>
							</thead>
						)}
						<tbody>
							{(node.rows ?? []).map((row, ridx) => (
								<tr key={ridx}>
									{row.map((cell, cidx) => (
										<td key={cidx} className="pt-2 pr-3 align-top">
											{cell}
										</td>
									))}
								</tr>
							))}
						</tbody>
					</table>
				</div>
			)
		case "bar_chart":
			if (Array.isArray(node.labels) && Array.isArray(node.values)) {
				return (
					<BarChart
						spec={{
							type: "bar",
							title: node.title,
							labels: node.labels,
							values: node.values,
						}}
					/>
				)
			}
			return null
		case "line_chart":
			if (Array.isArray(node.labels) && Array.isArray(node.values)) {
				return (
					<LineChart
						spec={{
							type: "line",
							title: node.title,
							labels: node.labels,
							values: node.values,
						}}
					/>
				)
			}
			return null
		case "container":
			return (
				<div key={key} className="space-y-3">
					{(node.children ?? []).map((child, idx) => renderUiNode(child, idx))}
				</div>
			)
		case "card":
			return (
				<div key={key} className="rounded-lg border border-gray-200 bg-gray-50 p-3">
					{(node.children ?? []).map((child, idx) => renderUiNode(child, idx))}
				</div>
			)
		default:
			return null
	}
}

function OpenJsonUi({ spec }: { spec: OpenJsonUiNode | OpenJsonUiNode[] }) {
	if (Array.isArray(spec)) {
		return <div className="space-y-3">{spec.map((n, i) => renderUiNode(n, i))}</div>
	}
	return <div className="space-y-3">{renderUiNode(spec)}</div>
}

// Image extensions to detect bare image URLs
const IMAGE_EXTENSIONS = /\.(jpg|jpeg|png|gif|webp|svg|bmp|tiff)(\?[^\s)]*)?$/i

/**
 * Lightweight markdown renderer that handles:
 * - ![alt](url) → <img>
 * - [text](url) → <a>
 * - **bold** → <strong>
 * - Bare image URLs → <img>
 * - Newlines → <br>
 */
function RichText({ text, isUser }: { text: string; isUser: boolean }) {
	const elements: React.ReactNode[] = []
	// Split into lines first to handle newlines
	const lines = text.split("\n")

	lines.forEach((line, lineIdx) => {
		if (lineIdx > 0) {
			elements.push(<br key={`br-${lineIdx}`} />)
		}

		// Combined regex for markdown images, markdown links, bold text, and bare URLs
		const tokenRegex =
			/!\[([^\]]*)\]\(([^)]+)\)|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|(https?:\/\/[^\s<>"{}|\\^`]+)/g

		let lastIndex = 0
		let match: RegExpExecArray | null

		while ((match = tokenRegex.exec(line)) !== null) {
			// Push any preceding plain text
			if (match.index > lastIndex) {
				elements.push(
					<React.Fragment key={`t-${lineIdx}-${lastIndex}`}>
						{line.slice(lastIndex, match.index)}
					</React.Fragment>
				)
			}

			if (match[1] !== undefined && match[2]) {
				// Markdown image: ![alt](url)
				elements.push(
					<img
						key={`img-${lineIdx}-${match.index}`}
						src={match[2]}
						alt={match[1] || "image"}
						className="max-w-full rounded-lg my-2 shadow-md"
						style={{ maxHeight: "400px", objectFit: "contain" }}
						loading="lazy"
					/>
				)
			} else if (match[3] !== undefined && match[4]) {
				// Markdown link: [text](url)
				elements.push(
					<a
						key={`a-${lineIdx}-${match.index}`}
						href={match[4]}
						target="_blank"
						rel="noopener noreferrer"
						className={`underline ${isUser ? "text-blue-200" : "text-blue-600 hover:text-blue-800"}`}
					>
						{match[3]}
					</a>
				)
			} else if (match[5] !== undefined) {
				// Bold: **text**
				elements.push(
					<strong key={`b-${lineIdx}-${match.index}`}>{match[5]}</strong>
				)
			} else if (match[6]) {
				// Bare URL — render as image if it looks like one, otherwise as a link
				const url = match[6]
				if (IMAGE_EXTENSIONS.test(url)) {
					elements.push(
						<img
							key={`bimg-${lineIdx}-${match.index}`}
							src={url}
							alt="image"
							className="max-w-full rounded-lg my-2 shadow-md"
							style={{ maxHeight: "400px", objectFit: "contain" }}
							loading="lazy"
						/>
					)
				} else {
					elements.push(
						<a
							key={`ba-${lineIdx}-${match.index}`}
							href={url}
							target="_blank"
							rel="noopener noreferrer"
							className={`underline break-all ${isUser ? "text-blue-200" : "text-blue-600 hover:text-blue-800"}`}
						>
							{url}
						</a>
					)
				}
			}

			lastIndex = match.index + match[0].length
		}

		// Push remaining plain text
		if (lastIndex < line.length) {
			elements.push(
				<React.Fragment key={`t-${lineIdx}-${lastIndex}`}>
					{line.slice(lastIndex)}
				</React.Fragment>
			)
		}
	})

	return <div className="whitespace-pre-wrap">{elements}</div>
}

export default function MessageBubble({
	role,
	content,
}: {
	role: MessageRole
	content: string
}) {
	const parsed = parseContent(content)
	const isUser = role === "user"
	return (
		<div
			className={`max-w-2xl rounded-lg px-4 py-2 ${
				isUser
					? "bg-blue-500 text-white"
					: "bg-white text-gray-900 border border-gray-200"
			}`}
		>
			{parsed.text && <RichText text={parsed.text} isUser={isUser} />}
			{parsed.ui && <OpenJsonUi spec={parsed.ui} />}
			{parsed.chart && <BarChart spec={parsed.chart} />}
			{parsed.lineChart && <LineChart spec={parsed.lineChart} />}
		</div>
	)
}
