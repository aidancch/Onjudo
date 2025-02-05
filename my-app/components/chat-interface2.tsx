"use client"

import { useEffect, useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Send } from "lucide-react"
import { socketService, type Message } from "@/lib/socket"

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const chatContentRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const checkConnection = setInterval(() => {
      setIsConnected(socketService.isConnected())
    }, 1000)

    socketService.connect(
      (updatedMessages) => {
        console.log("Updating messages:", updatedMessages)
        setMessages(updatedMessages)
        setError(null)
        // Scroll to bottom after messages update
        setTimeout(() => {
          if (chatContentRef.current) {
            chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight
          }
        }, 0)
      },
      () => {}, // We don't need listings updates in this component
    )

    // Add event listener for AI responses
    socketService.onAIResponse((aiMessage) => {
      setMessages((prev) => [...prev, { content: aiMessage, sender: "assistant" }])
      setTimeout(() => {
        if (chatContentRef.current) {
          chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight
        }
      }, 1000)
    })

    return () => {
      clearInterval(checkConnection)
      socketService.disconnect()
    }
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    if (!isConnected) {
      setError("Not connected to server. Please try again later.")
      return
    }

    const newMessage: Message = {
      content: input,
      sender: "user",
    }
    setMessages((prev) => [...prev, newMessage])

    socketService.sendMessage(input)
    setInput("")

    // Scroll to bottom after sending a message
    setTimeout(() => {
      if (chatContentRef.current) {
        chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight
      }
    }, 0)
  }

  return (
    <Card className="h-full flex flex-col shadow-md">
      <CardHeader className="border-b p-4">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold">Property Assistant</h2>
          <div className={`h-2 w-2 rounded-full ${isConnected ? "bg-green-500" : "bg-red-500"}`} />
        </div>
      </CardHeader>
      <CardContent className="flex-1 overflow-auto p-4 space-y-4" ref={chatContentRef}>
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}
        {messages.map((message, index) => (
          <div key={index} className={`flex gap-2 ${message.sender === "user" ? "flex-row-reverse" : ""}`}>
            <Avatar className="h-8 w-8">
              <AvatarImage src={message.sender === "assistant" ? "/placeholder.svg" : undefined} />
              <AvatarFallback>{message.sender === "user" ? "U" : "A"}</AvatarFallback>
            </Avatar>
            <div
              className={`rounded-lg px-3 py-2 max-w-[80%] ${
                message.sender === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </CardContent>
      <CardFooter className="border-t p-4">
        <form onSubmit={handleSubmit} className="flex w-full gap-2">
          <Input placeholder="Type your message..." value={input} onChange={(e) => setInput(e.target.value)} />
          <Button type="submit" size="icon" disabled={!isConnected}>
            <Send className="h-4 w-4" />
            <span className="sr-only">Send message</span>
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
}

