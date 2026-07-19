import { Link, useNavigate } from 'react-router-dom'
import { MessageSquarePlus, Trash2, LayoutDashboard, History, LogOut, Bot } from 'lucide-react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { listConversations, deleteConversation } from '../api/conversations'
import { useAuth } from '../context/AuthContext'
import type { Conversation } from '../types'

function timeAgo(iso: string) {
  const diff = Date.now() - new Date(iso).getTime()
  const m = Math.floor(diff / 60_000)
  if (m < 1) return 'just now'
  if (m < 60) return `${m}m ago`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h}h ago`
  return `${Math.floor(h / 24)}d ago`
}

interface Props {
  activeConversationId?: string
}

export default function Sidebar({ activeConversationId }: Props) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const qc = useQueryClient()

  const { data: conversations = [] } = useQuery({
    queryKey: ['conversations'],
    queryFn: listConversations,
  })

  const deleteMutation = useMutation({
    mutationFn: deleteConversation,
    onSuccess: (_, id) => {
      qc.invalidateQueries({ queryKey: ['conversations'] })
      if (activeConversationId === id) navigate('/chat')
    },
  })

  return (
    <aside className="flex flex-col w-72 shrink-0 bg-slate-900 border-r border-slate-800 h-screen">
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-slate-800">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-600">
          <Bot size={16} className="text-white" />
        </div>
        <div>
          <p className="text-sm font-semibold text-slate-100">EAIDA</p>
          <p className="text-xs text-slate-500">Enterprise AI Assistant</p>
        </div>
      </div>

      {/* New Chat */}
      <div className="px-3 pt-3">
        <Link
          to="/chat"
          className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
        >
          <MessageSquarePlus size={16} />
          New Chat
        </Link>
      </div>

      {/* Conversations */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-0.5">
        {conversations.length === 0 ? (
          <p className="text-xs text-slate-600 px-3 py-4 text-center">No conversations yet.<br />Start a new chat!</p>
        ) : (
          conversations.map((c: Conversation) => (
            <div
              key={c.id}
              className={`group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
                activeConversationId === c.id
                  ? 'bg-slate-800 text-white'
                  : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
              }`}
              onClick={() => navigate(`/chat/${c.id}`)}
            >
              <span className="flex-1 text-sm truncate">{c.title}</span>
              <span className="text-xs text-slate-600 shrink-0 group-hover:hidden">{timeAgo(c.updated_at)}</span>
              <button
                onClick={(e) => { e.stopPropagation(); deleteMutation.mutate(c.id) }}
                className="hidden group-hover:flex p-1 rounded text-slate-600 hover:text-red-400 transition-colors"
              >
                <Trash2 size={12} />
              </button>
            </div>
          ))
        )}
      </div>

      {/* Nav links */}
      <div className="px-3 py-2 border-t border-slate-800 space-y-0.5">
        <Link
          to="/dashboard"
          className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-slate-400 hover:bg-slate-800 hover:text-white transition-colors"
        >
          <LayoutDashboard size={16} />
          Dashboard
        </Link>
        <Link
          to="/history"
          className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-slate-400 hover:bg-slate-800 hover:text-white transition-colors"
        >
          <History size={16} />
          History
        </Link>
      </div>

      {/* User info */}
      <div className="px-3 py-3 border-t border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-indigo-600/30 flex items-center justify-center text-xs font-semibold text-indigo-400 shrink-0">
            {user?.display_name?.[0]?.toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-slate-200 truncate">{user?.display_name}</p>
            <p className="text-xs text-slate-500 capitalize">{user?.role?.name}</p>
          </div>
          <button
            onClick={logout}
            className="p-1.5 rounded-lg text-slate-500 hover:text-red-400 hover:bg-slate-800 transition-colors"
            title="Sign out"
          >
            <LogOut size={14} />
          </button>
        </div>
      </div>
    </aside>
  )
}
