interface Props {
  rows: Record<string, unknown>[]
  maxRows?: number
}

export default function ResultTable({ rows, maxRows = 100 }: Props) {
  if (!rows.length) return <p className="text-slate-500 text-sm">No results.</p>

  const cols = Object.keys(rows[0])
  const visible = rows.slice(0, maxRows)

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-700 mt-3">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-slate-800">
            {cols.map((c) => (
              <th
                key={c}
                className="px-3 py-2 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider whitespace-nowrap"
              >
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {visible.map((row, i) => (
            <tr key={i} className="hover:bg-slate-800/50 transition-colors">
              {cols.map((c) => (
                <td key={c} className="px-3 py-2 text-slate-300 whitespace-nowrap">
                  {row[c] === null || row[c] === undefined
                    ? <span className="text-slate-600">null</span>
                    : String(row[c])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {rows.length > maxRows && (
        <p className="px-3 py-2 text-xs text-slate-500 border-t border-slate-700">
          Showing {maxRows} of {rows.length} rows
        </p>
      )}
    </div>
  )
}
