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
            <div className="text-3xl font-bold">${property.price.toLocaleString()}</div>
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
          <div className="text-base leading-relaxed">{property.description}</div>

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
                      {property.agent_phones.map((phone, index) => (
                        <div key={index}>{phone}</div>
                      ))}
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
              <ul className="space-y-2">
                {property.nearby_schools.map((school, index) => (
                  <li key={index} className="text-sm">
                    {school}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Google Maps */}
          <div className="rounded-lg overflow-hidden border h-[300px] mx-4">
            <iframe
              width="100%"
              height="100%"
              frameBorder="0"
              style={{ border: 0 }}
              src={`https://www.google.com/maps/embed/v1/place?key=AIzaSyDL5_jBjWBIOTmwU7Q1svntONKY9SHrV_w&q=${encodeURIComponent(
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
            src={`https://www.google.com/maps/embed/v1/search?key=AIzaSyDL5_jBjWBIOTmwU7Q1svntONKY9SHrV_w&zoom=12&q=schools+${encodeURIComponent(
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

