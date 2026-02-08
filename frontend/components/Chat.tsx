"use client"
import { useState, useEffect } from "react"
import { connect } from "@/lib/websocket"

export default function Chat() {
  const [messages, setMessages] = useState<string[]>([])
  const [input, setInput] = useState("")
  const [ws, setWs] = useState<WebSocket | null>(null)

  useEffect(() => {
    setWs(connect(e => {
      if (e.type === "token") {
        setMessages(m => [...m, e.content])
      }
    }))
  }, [])

  return (
    <div>
      <div>{messages.join("")}</div>
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={() => ws?.send(input)}>Send</button>
    </div>
  )
}
