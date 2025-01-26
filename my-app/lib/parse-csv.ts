import fs from "fs/promises"
import path from "path"
import { parse } from "csv-parse/sync"

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

export async function parseCSV(filePath: string): Promise<Property[]> {
  try {
    const fileContent = await fs.readFile(path.join(process.cwd(), filePath), "utf-8")
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
    })

    return records.map((record: any) => ({
      id: Number.parseInt(record.id),
      price: Number.parseInt(record.price),
      beds: Number.parseInt(record.beds),
      baths: Number.parseInt(record.baths),
      sqft: Number.parseInt(record.sqft),
      address: record.address,
      description: record.description,
      image: record.image,
    }))
  } catch (error) {
    console.error("Error parsing CSV:", error)
    return []
  }
}

