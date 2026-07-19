import client from './client'
import type { Budget } from '../types'

export const listBudgets = (limit = 100) =>
  client.get<Budget[]>(`/api/v1/budgets/?limit=${limit}`).then((r) => r.data)
