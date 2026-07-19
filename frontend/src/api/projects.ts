import client from './client'
import type { Project } from '../types'

export const listProjects = (limit = 100) =>
  client.get<Project[]>(`/api/v1/projects/?limit=${limit}`).then((r) => r.data)
