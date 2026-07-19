import client from './client'
import type { Employee } from '../types'

export const listEmployees = (limit = 50) =>
  client.get<Employee[]>(`/api/v1/employees/?limit=${Math.min(limit, 100)}`).then((r) => r.data)
