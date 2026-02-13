"use client"
import { useState, useEffect, useRef } from "react"
import { connect } from "../lib/websocket"
import ToolCard from "./ToolCard"
import MessageBubble from "./MessageBubble"

type UIEvent =
  | { type: "token"; content: string }
  | { type: "message_complete"; content: string }
  | { type: "tool_start"; tool: string; args: unknown }
  | { type: "tool_end"; tool: string; result: unknown }

interface Message {
  role: "user" | "assistant"
  content: string
  events?: UIEvent[]
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [events, setEvents] = useState<UIEvent[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [connectionStatus, setConnectionStatus] = useState<"connected" | "disconnected" | "connecting">("connecting")
  const [ws, setWs] = useState<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, events])

  useEffect(() => {
    try {
      const newWs = connect(
        (e: UIEvent) => {
          setEvents(prev => [...prev, e])
          if (e.type === "token") {
            setMessages(prev => 
              prev.map((msg, idx) => 
                idx === prev.length - 1 ? { ...msg, content: msg.content + e.content } : msg
              )
            )
          } else if (e.type === "message_complete") {
            setMessages(prev => 
              prev.map((msg, idx) => 
                idx === prev.length - 1 ? { ...msg, content: e.content } : msg
              )
            )
            setIsLoading(false)
          } else if (e.type === "tool_start" || e.type === "tool_end") {
            // Tool events are already added to events array
          }
        },
        {
          onConnect: () => setConnectionStatus("connected"),
          onDisconnect: () => setConnectionStatus("disconnected"),
          onError: (err) => {
            setError(err)
            setIsLoading(false)
          },
        }
      )
      setWs(newWs)

      return () => {
        newWs.close()
      }
    } catch (err) {
      setConnectionStatus("disconnected")
      setError(err instanceof Error ? err.message : "Connection failed")
    }
  }, [])

  const handleSend = async () => {
    if (!input.trim() || !ws || isLoading) return

    setError(null)
    setIsLoading(true)
    setEvents([])

    try {
      setMessages(prev => [...prev, { role: "user", content: input }])
      setMessages(prev => [...prev, { role: "assistant", content: "", events: [] }])
      ws.send(input)
      setInput("")
      // isLoading will be set to false when message_complete event is received
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message")
      setMessages(prev => prev.slice(0, -1))
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-900 via-purple-900 to-pink-900 border-b border-gray-700 px-4 py-3 shadow-lg">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🚀</span>
            <div>
              <h1 className="text-2xl font-bold text-white">NASA Space Explorer</h1>
              <p className="text-xs text-gray-300">Powered by NASA APIs</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div
              className={`w-3 h-3 rounded-full ${
                connectionStatus === "connected"
                  ? "bg-green-500"
                  : connectionStatus === "connecting"
                  ? "bg-yellow-500"
                  : "bg-red-500"
              }`}
            />
            <span className="text-sm text-gray-300 capitalize">{connectionStatus}</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-300 py-12">
              <div className="text-6xl mb-4">🌌</div>
              <p className="text-lg font-semibold mb-2">Welcome to NASA Space Explorer!</p>
              <p className="text-sm mb-4">Ask me about space exploration, astronomy, Mars rovers, and more!</p>
              <div className="text-xs text-gray-400 space-y-1">
                <p>Try: "Show me today's astronomy picture"</p>
                <p>Try: "Get photos from Mars Curiosity rover"</p>
                <p>Try: "Are there any asteroids near Earth?"</p>
                <p>Try: "Search for images of the Hubble telescope"</p>
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div>
                <MessageBubble role={msg.role} content={msg.content} />
                {msg.role === "assistant" && events.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200 space-y-2">
                    {events.map((e, i) => (
                      <div key={i}>
                        {e.type === "tool_start" && (
                          <ToolCard tool={e.tool} args={e.args} />
                        )}
                        {e.type === "tool_end" && (
                          <ToolCard tool={e.tool} result={e.result} />
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border-t border-red-200 px-4 py-3">
          <div className="max-w-4xl mx-auto">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Input */}
      <div className="bg-gray-800 border-t border-gray-700 px-4 py-4">
        <div className="max-w-4xl mx-auto flex gap-2">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading || connectionStatus !== "connected"}
            placeholder={
              connectionStatus !== "connected"
                ? "Connecting..."
                : isLoading
                ? "Processing..."
                : "Ask about space exploration, NASA missions, Mars, asteroids..."
            }
            className="flex-1 px-4 py-2 border border-gray-600 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:bg-gray-800 disabled:cursor-not-allowed"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim() || connectionStatus !== "connected"}
            className="px-6 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed transition-all"
          >
            {isLoading ? "..." : "🚀 Send"}
          </button>
        </div>
      </div>
    </div>
  )
}

