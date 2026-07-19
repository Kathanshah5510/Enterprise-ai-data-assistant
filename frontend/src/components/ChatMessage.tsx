import { useState } from 'react'
import { ChevronDown, ChevronRight, AlertCircle, Clock, Database } from 'lucide-react'
import type { Message } from '../types'
import ResultTable from './ResultTable'
import ResultChart from './ResultChart'

function SQLBlock({ sql }: { sql: string }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="mt-2 rounded-lg border border-slate-700 overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-2 px-3 py-2 bg-slate-800 text-xs text-slate-400 hover:bg-slate-750 transition-colors"
      >
        {open ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
        <Database size={12} />
        <span>Generated SQL</span>
      </button>
      {open && (
        <pre className="p-3 text-xs text-cyan-300 font-mono overflow-x-auto bg-slate-900 leading-relaxed">
          {sql}
        </pre>
      )}
    </div>
  )
}

export default function ChatMessage({ message }: { message: Message }) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="bg-indigo-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-2xl text-sm leading-relaxed shadow-lg">
          {message.content}
        </div>
      </div>
    )
  }

  // Assistant message
  return (
    <div className="flex justify-start">
      <div className="bg-slate-800/80 border border-slate-700/50 rounded-2xl rounded-tl-sm px-4 py-3 max-w-4xl w-full shadow-lg">
        {message.error ? (
          <div className="flex items-start gap-2 text-red-400 text-sm">
            <AlertCircle size={16} className="mt-0.5 shrink-0" />
            <span>{message.error}</span>
          </div>
        ) : (
          <>
            {message.sql_query && <SQLBlock sql={message.sql_query} />}

            {(message.row_count !== null || message.execution_time_ms !== null) && (
              <div className="flex items-center gap-4 mt-2 text-xs text-slate-500">
                {message.row_count !== null && (
                  <span className="flex items-center gap-1">
                    <Database size={10} />
                    {message.row_count} row{message.row_count !== 1 ? 's' : ''}
                  </span>
                )}
                {message.execution_time_ms !== null && (
                  <span className="flex items-center gap-1">
                    <Clock size={10} />
                    {message.execution_time_ms}ms
                  </span>
                )}
              </div>
            )}

            {message.result_data?.rows && message.result_data.rows.length > 0 && (
              <div className="mt-2">
                {message.chart_suggestion && message.chart_suggestion !== 'none' && message.chart_suggestion !== 'table' ? (
                  <ResultChart rows={message.result_data.rows} type={message.chart_suggestion} />
                ) : (
                  <ResultTable rows={message.result_data.rows} />
                )}
              </div>
            )}

            {message.result_data?.rows?.length === 0 && (
              <p className="mt-2 text-sm text-slate-500">Query returned no results.</p>
            )}
          </>
        )}
      </div>
    </div>
  )
}
