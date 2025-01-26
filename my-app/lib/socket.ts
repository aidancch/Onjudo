import { io, type Socket } from "socket.io-client"

export interface Message {
  content: string
  sender: "user" | "assistant"
}

export interface Property {
  id: number
  price: number
  beds: number
  baths: number
  sqft: number
  address: string
  description: string
  image: string
}

class SocketService {
  private socket: Socket | null = null
  private static instance: SocketService
  private aiResponseCallback: ((message: string) => void) | null = null

  private constructor() {}

  public static getInstance(): SocketService {
    if (!SocketService.instance) {
      SocketService.instance = new SocketService()
    }
    return SocketService.instance
  }

  public connect(onChatUpdate: (messages: Message[]) => void, onListingsUpdate: (listings: Property[]) => void) {
    if (this.socket) {
      console.log("Socket already connected")
      return
    }

    console.log("Initializing socket connection...")
    this.socket = io("http://localhost:4000", {
      transports: ["websocket"],
      upgrade: false,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    })

    this.socket.on("connect", () => {
      console.log("Connected to server with ID:", this.socket?.id)
    })

    this.socket.on("connect_error", (error) => {
      console.error("Connection error:", error)
    })

    this.socket.on("error", (error) => {
      console.error("Socket error:", error)
    })

    this.socket.on("initial_data", (data: { chat_history: Message[]; listings: Property[] }) => {
      console.log("Received initial data:", data)
      onChatUpdate(data.chat_history)
      onListingsUpdate(data.listings)
    })

    this.socket.on("chat_update", (data: { chat_history: Message[] }) => {
      console.log("Received chat update:", data)
      onChatUpdate(data.chat_history)
    })

    this.socket.on("listings_update", (data: { listings: Property[] }) => {
      console.log("Received listings update:", data)
      onListingsUpdate(data.listings)
    })

    this.socket.on("ai_response", (data: { message: string }) => {
      console.log("Received AI response:", data)
      if (this.aiResponseCallback) {
        this.aiResponseCallback(data.message)
      }
    })
  }

  public sendMessage(message: string) {
    if (!this.socket?.connected) {
      console.error("Socket not connected")
      return
    }
    console.log("Sending message:", message)
    this.socket.emit("user_message", { message })
  }

  public disconnect() {
    if (this.socket) {
      console.log("Disconnecting socket...")
      this.socket.disconnect()
      this.socket = null
    }
  }

  public isConnected(): boolean {
    return this.socket?.connected ?? false
  }

  public onAIResponse(callback: (message: string) => void) {
    this.aiResponseCallback = callback
  }
}

export const socketService = SocketService.getInstance()

export interface Property {
  property_id: number
  list_price: number
  beds: number
  baths: number
  sqft: number
  full_street_line: string
  text: string
  property_url: string
  status: string
  list_date: string
  neighborhoods: string[]
  agent_id: string
  agent_name: string
  agent_email: string
  agent_phones: string[]
  broker_id: string
  office_name: string
  office_email: string
  nearby_schools: string[]
  primary_photo: string
  latitute: number
  longitute: number
}

