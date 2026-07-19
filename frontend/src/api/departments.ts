import client from './client'
import type { Department } from '../types'

export const listDepartments = () =>
  client.get<Department[]>('/api/v1/departments/').then((r) => r.data)
