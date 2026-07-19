import { useEffect, useRef, useState, type KeyboardEvent } from 'react'
import { useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Send, Sparkles } from 'lucide-react'
import { getConversation } from '../api/conversations'
import { runQuery } from '../api/query'
import Sidebar from '../components/Sidebar'
import ChatMessage from '../components/ChatMessage'
import type { Message, QueryResponse } from '../types'

function queryResponseToMessage(res: QueryResponse): Message {
  return {
    id: res.message_id,
    conversation_id: res.conversation_id,
    role: 'assistant',
    content: res.question,
    sql_query: res.sql_query || null,
    result_data: res.results.length ? { rows: res.results } : null,
    row_count: res.row_count,
    execution_time_ms: res.execution_time_ms,
    error: res.error,
    chart_suggestion: res.chart_suggestion,
    created_at: new Date().toISOString(),
  }
}

const SUGGESTIONS = [
  'Which department has the highest average salary?',
  'Show all employees hired after 2023',
  'Which projects are over budget?',
  'Compare Engineering and Finance headcount',
  'List the top 5 highest-paid employees',
]

export default function Chat() {
  const { conversationId } = useParams<{ conversationId: string }>()
  const qc = useQueryClient()
  const bottomRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [activeConvId, setActiveConvId] = useState<string | undefined>(conversationId)

  // Load existing conversation
  const { data: conversation } = useQuery({
    queryKey: ['conversation', conversationId],
    queryFn: () => getConversation(conversationId!),
    enabled: !!conversationId,
  })

  useEffect(() => {
    if (conversation) {
      setMessages(conversation.messages)
      setActiveConvId(conversation.id)
    }
  }, [conversation])

  // Reset on new chat (no conversationId)
  useEffect(() => {
    if (!conversationId) {
      setMessages([])
      setActiveConvId(undefined)
    }
  }, [conversationId])

  // Scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const mutation = useMutation({
    mutationFn: runQuery,
    onSuccess: (res) => {
      setActiveConvId(res.conversation_id)
      const userMsg: Message = {
        id: `user-${Date.now()}`,
        conversation_id: res.conversation_id,
        role: 'user',
        content: res.question,
        sql_query: null,
        result_data: null,
        row_count: null,
        execution_time_ms: null,
        error: null,
        chart_suggestion: null,
        created_at: new Date().toISOString(),
      }
      // Replace optimistic user message with confirmed messages
      setMessages((prev) => {
        const withoutPending = prev.filter((m) => !m.id.startsWith('pending-'))
        return [...withoutPending, userMsg, queryResponseToMessage(res)]
      })
      qc.invalidateQueries({ queryKey: ['conversations'] })
    },
    onError: () => {
      setMessages((prev) => prev.filter((m) => !m.id.startsWith('pending-')))
    },
  })

  const handleSubmit = () => {
    const q = question.trim()
    if (!q || mutation.isPending) return
    setQuestion('')

    // Optimistic user message
    const pending: Message = {
      id: `pending-${Date.now()}`,
      conversation_id: activeConvId ?? '',
      role: 'user',
      content: q,
      sql_query: null, result_data: null, row_count: null,
      execution_time_ms: null, error: null, chart_suggestion: null,
      created_at: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, pending])

    mutation.mutate({ question: q, conversation_id: activeConvId })
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const isEmpty = messages.length === 0 && !mutation.isPending

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar activeConversationId={activeConvId} />

      <div className="flex flex-col flex-1 min-w-0">
        {/* Header */}
        <div className="flex items-center gap-3 px-6 py-4 border-b border-slate-800 bg-slate-900/50 backdrop-blur shrink-0">
          <Sparkles size={16} className="text-indigo-400" />
          <h1 className="text-sm font-semibold text-slate-200 truncate">
            {conversation?.title ?? 'New Conversation'}
          </h1>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
          {isEmpty ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 rounded-2xl bg-indigo-600/20 flex items-center justify-center mb-4">
                <Sparkles size={28} className="text-indigo-400" />
              </div>
              <h2 className="text-lg font-semibold text-slate-300 mb-1">Ask your data a question</h2>
              <p className="text-sm text-slate-500 max-w-sm mb-8">
                Describe what you want to know in plain English. The AI will write and run the SQL for you.
              </p>
              <div className="grid grid-cols-1 gap-2 w-full max-w-lg">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => { setQuestion(s); textareaRef.current?.focus() }}
                    className="text-left px-4 py-2.5 bg-slate-800/60 hover:bg-slate-800 border border-slate-700/50 rounded-xl text-sm text-slate-400 hover:text-slate-200 transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
          )}

          {mutation.isPending && (
            <div className="flex justify-start">
              <div className="bg-slate-800/80 border border-slate-700/50 rounded-2xl rounded-tl-sm px-4 py-3">
                <div className="flex items-center gap-1.5">
                  {[0, 1, 2].map((i) => (
                    <div
                      key={i}
                      className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce"
                      style={{ animationDelay: `${i * 0.15}s` }}
                    />
                  ))}
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="px-4 pb-4 pt-2 border-t border-slate-800 shrink-0">
          <div className="flex items-end gap-2 bg-slate-800 border border-slate-700 rounded-2xl px-4 py-2 focus-within:border-indigo-500/50 transition-colors">
            <textarea
              ref={textareaRef}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about your data… (Enter to send, Shift+Enter for newline)"
              rows={1}
              disabled={mutation.isPending}
              className="flex-1 bg-transparent text-sm text-slate-100 placeholder-slate-600 resize-none focus:outline-none py-1.5 max-h-32 overflow-y-auto"
              style={{ lineHeight: '1.5' }}
            />
            <button
              onClick={handleSubmit}
              disabled={!question.trim() || mutation.isPending}
              className="flex items-center justify-center w-8 h-8 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shrink-0 mb-0.5"
            >
              <Send size={14} className="text-white" />
            </button>
          </div>
          <p className="text-center text-xs text-slate-700 mt-2">
            Results are AI-generated. Always verify critical data.
          </p>
        </div>
      </div>
    </div>
  )
}
