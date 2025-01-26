"use client"

import { useEffect, useState } from "react"
import Image from "next/image"
import { Card, CardContent } from "@/components/ui/card"
import { Bed, Bath, Maximize } from "lucide-react"
import { socketService, type Property } from "@/lib/socket"
import { PropertyModal } from "./property-modal"

const truncateDescription = (description: string | null | undefined, maxLength = 200) => {
  if (!description) return "" // Return an empty string if description is missing
  if (description.length <= maxLength) return description
  return description.slice(0, maxLength).trim() + "..."
}

export function PropertyGrid() {
  const [properties, setProperties] = useState<Property[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null)

  useEffect(() => {
    const checkConnection = setInterval(() => {
      setIsConnected(socketService.isConnected())
    }, 1000)

    socketService.connect(
      () => {}, // We don't need chat updates in this component
      (updatedListings) => setProperties(updatedListings),
    )

    return () => {
      clearInterval(checkConnection)
      socketService.disconnect()
    }
  }, [])

  if (!isConnected) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-lg text-gray-500">Connecting to server...</p>
      </div>
    )
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4 auto-rows-min">
        {properties.map((property) => (
          <Card
            key={property.id}
            className="overflow-hidden flex flex-col cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => setSelectedProperty(property)}
          >
            <div className="relative h-48 md:h-40 lg:h-48">
              <Image
                src={property.primary_photo || "/placeholder.svg"}
                alt={`${property.address} property`}
                fill
                className="object-cover"
              />
            </div>
            <CardContent className="p-4 flex flex-col gap-2">
              <h3 className="text-xl md:text-2xl font-bold">${property.list_price}</h3>

              <p className="text-sm md:text-base text-muted-foreground">{property.address}</p>

              <div className="flex flex-col sm:flex-row gap-2 sm:gap-4 text-sm text-muted-foreground">
                <span className="flex items-center gap-1">
                  <Bed className="h-4 w-4 shrink-0" />
                  <span>{property.beds} beds</span>
                </span>
                <span className="flex items-center gap-1">
                  <Bath className="h-4 w-4 shrink-0" />
                  <span>{property.baths} baths</span>
                </span>
                <span className="flex items-center gap-1">
                  <Maximize className="h-4 w-4 shrink-0" />
                  <span>{property.sqft} sqft</span>
                </span>
              </div>

              <p className="text-sm hidden md:block">{truncateDescription(property.text)}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <PropertyModal
        property={selectedProperty}
        isOpen={selectedProperty !== null}
        onClose={() => setSelectedProperty(null)}
      />
    </>
  )
}

