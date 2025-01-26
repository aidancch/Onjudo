import axios from "axios"

const API_URL = "http://localhost:4000/api"

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

export async function getProperties(): Promise<Property[]> {
  const response = await axios.get(`${API_URL}/properties`)
  return response.data
}

export async function addProperty(property: Omit<Property, "id">): Promise<Property> {
  const response = await axios.post(`${API_URL}/properties`, property)
  return response.data
}

