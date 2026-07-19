import client from './client'
import type { QueryRequest, QueryResponse } from '../types'

export const runQuery = (body: QueryRequest) =>
  client.post<QueryResponse>('/api/v1/query/', body).then((r) => r.data)
