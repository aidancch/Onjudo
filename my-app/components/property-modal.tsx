"use client"

import { X, Bed, Bath, Maximize, Calendar, User, Mail, Phone, Building } from "lucide-react"
import Image from "next/image"
import { Dialog, DialogContent, DialogHeader } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import type { Property } from "@/lib/socket"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface PropertyModalProps {
  property: Property | null
  isOpen: boolean
  onClose: () => void
}

export function PropertyModal({ property, isOpen, onClose }: PropertyModalProps) {
  if (!property) return null

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-3xl font-bold">{property.address}</h2>
            </div>
            <Button variant="ghost" size="icon" className="h-6 w-6 rounded-full" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        </DialogHeader>

        <div className="space-y-6">
          {/* Property Image */}
          <div className="relative h-[400px] w-full rounded-lg overflow-hidden">
            <Image
              src={property.primary_photo || "/placeholder.svg"}
              alt={property.address}
              fill
              className="object-cover"
            />
          </div>

          {/* Price */}
          

          {/* Details */}
          <div className="flex gap-3 mt-2">
            <div className="text-3xl font-bold">${property.list_price}</div>
                <div>

                </div>
                <div className="flex items-center gap-2">
                  <Bed className="h-5 w-5" />
                  <span>{property.beds} beds</span>
                </div>
                <div className="flex items-center gap-2">
                  <Bath className="h-5 w-5" />
                  <span>{property.baths} baths</span>
                </div>
                <div className="flex items-center gap-2">
                  <Maximize className="h-5 w-5" />
                  <span>{property.sqft.toLocaleString()} sqft</span>
                </div>
              </div>

          {/* Description */}
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm">{property.text || "No description provided."}</p>
            </CardContent>
          </Card>

          {/* Listing Details */}
          <Card>
            <CardHeader>
              <CardTitle>Listing Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">Listed on {property.list_date}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <User className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">
                      Agent: {property.agent_name} ({property.agent_id})
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">{property.agent_email}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="h-4 w-4 text-muted-foreground" />
                    <div className="text-sm">
                      {property.agent_phones}
                    </div>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Building className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">Broker ID: {property.broker_id}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Building className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">Office: {property.office_name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">{property.office_email}</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Nearby Schools */}
          <Card>
            <CardHeader>
              <CardTitle>Nearby Schools</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm">{property.nearby_schools || "No nearby schools listed."}</p>
            </CardContent>
          </Card>

          {/* Google Maps */}
          <div className="rounded-lg overflow-hidden border h-[300px] mx-4">
            <iframe
              width="100%"
              height="100%"
              frameBorder="0"
              style={{ border: 0 }}
              src={`https://www.google.com/maps/embed/v1/place?key=YOUR_API_KEY&q=${encodeURIComponent(
                property.address,
              )}`}
              allowFullScreen
            />
          </div>

          {/* Schools Map */}
        <div className="rounded-lg overflow-hidden border h-[300px] mx-4">
          <iframe
            width="100%"
            height="100%"
            frameBorder="0"
            style={{ border: 0 }}
            src={`https://www.google.com/maps/embed/v1/search?key=YOUR_API_KEY&zoom=12&q=schools+${encodeURIComponent(
              property.address,
            )}`}
            allowFullScreen
          />
        </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

