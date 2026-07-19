import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { MessageSquare, Trash2, Clock } from 'lucide-react'
import { listConversations, deleteConversation } from '../api/conversations'
import Sidebar from '../components/Sidebar'
import type { Conversation } from '../types'

function formatDate(iso: string) {
  return new Date(iso).toLocaleString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

export default function History() {
  const navigate = useNavigate()
  const qc = useQueryClient()

  const { data: conversations = [], isLoading } = useQuery({
    queryKey: ['conversations'],
    queryFn: listConversations,
  })

  const deleteMutation = useMutation({
    mutationFn: deleteConversation,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['conversations'] }),
  })

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-6 py-6">
          <div className="mb-6">
            <h1 className="text-xl font-bold text-white">Conversation History</h1>
            <p className="text-sm text-slate-500">Your previous AI data queries</p>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-20">
              <div className="w-6 h-6 border-2 border-slate-700 border-t-indigo-500 rounded-full animate-spin" />
            </div>
          ) : conversations.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-center">
              <MessageSquare size={40} className="text-slate-700 mb-4" />
              <p className="text-slate-400 font-medium">No conversations yet</p>
              <p className="text-sm text-slate-600 mt-1">
                Go to Chat and ask your first question.
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {conversations.map((c: Conversation) => (
                <div
                  key={c.id}
                  className="group flex items-center gap-4 bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl px-5 py-4 cursor-pointer transition-colors"
                  onClick={() => navigate(`/chat/${c.id}`)}
                >
                  <div className="w-9 h-9 rounded-xl bg-indigo-600/20 flex items-center justify-center shrink-0">
                    <MessageSquare size={16} className="text-indigo-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-200 truncate">{c.title}</p>
                    <div className="flex items-center gap-1.5 mt-0.5">
                      <Clock size={11} className="text-slate-600" />
                      <p className="text-xs text-slate-500">{formatDate(c.updated_at)}</p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); deleteMutation.mutate(c.id) }}
                    className="opacity-0 group-hover:opacity-100 p-2 rounded-lg text-slate-600 hover:text-red-400 hover:bg-slate-800 transition-all"
                    title="Delete conversation"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
