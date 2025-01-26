import { PropertyGrid } from "@/components/property-grid"
import { ChatInterface } from "@/components/chat-interface"

export default function Home() {
  return (
    <div className="flex flex-col md:flex-row h-screen">
      <div className="flex-1 overflow-auto border-r">
        <PropertyGrid />
      </div>
      <div className="w-full md:w-[400px] h-[500px] md:h-auto">
        <ChatInterface />
      </div>
    </div>
  )
}

