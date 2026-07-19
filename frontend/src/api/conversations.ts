import client from './client'
import type { Conversation, ConversationDetail } from '../types'

export const listConversations = () =>
  client.get<Conversation[]>('/api/v1/conversations/').then((r) => r.data)

export const getConversation = (id: string) =>
  client.get<ConversationDetail>(`/api/v1/conversations/${id}`).then((r) => r.data)

export const createConversation = (title: string) =>
  client.post<Conversation>('/api/v1/conversations/', { title }).then((r) => r.data)

export const deleteConversation = (id: string) =>
  client.delete(`/api/v1/conversations/${id}`)
