interface WebSocketCallbacks {
  onConnect?: () => void
  onDisconnect?: () => void
  onError?: (error: string) => void
}

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/chat"
const RECONNECT_INTERVAL = 3000
const MAX_RECONNECT_ATTEMPTS = 5

export function connect(
  onMessage: (data: any) => void,
  callbacks?: WebSocketCallbacks
): WebSocket {
  let reconnectAttempts = 0
  let isIntentionallyClosed = false

  function createWebSocket(): WebSocket {
    const ws = new WebSocket(WS_URL)

    ws.onopen = () => {
      console.log("WebSocket connected")
      reconnectAttempts = 0
      callbacks?.onConnect?.()
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage(data)
      } catch (err) {
        console.error("Failed to parse message:", err)
        callbacks?.onError?.("Failed to parse server response")
      }
    }

    ws.onerror = () => {
      console.error("WebSocket error")
      callbacks?.onError?.("Connection error occurred")
    }

    ws.onclose = () => {
      console.log("WebSocket closed")
      callbacks?.onDisconnect?.()

      // Reconnect logic
      if (!isIntentionallyClosed && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
        reconnectAttempts++
        console.log(`Attempting to reconnect (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})...`)
        setTimeout(() => {
          const newWs = createWebSocket()
          // Replace the original ws reference
          Object.assign(ws, newWs)
        }, RECONNECT_INTERVAL)
      } else if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
        callbacks?.onError?.("Failed to connect after multiple attempts")
      }
    }

    return ws
  }

  const ws = createWebSocket()

  // Override close method to mark intentional closure
  const originalClose = ws.close.bind(ws)
  ws.close = function () {
    isIntentionallyClosed = true
    originalClose()
  }

  return ws
}
