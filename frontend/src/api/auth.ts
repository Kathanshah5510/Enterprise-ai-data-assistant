import client from './client'
import type { TokenResponse, User } from '../types'

export const login = (username: string, password: string) =>
  client.post<TokenResponse>('/auth/login', { username, password }).then((r) => r.data)

export const getMe = () =>
  client.get<User>('/auth/me').then((r) => r.data)
