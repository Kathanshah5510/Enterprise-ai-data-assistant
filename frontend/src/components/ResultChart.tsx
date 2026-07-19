import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import ResultTable from './ResultTable'

const COLORS = [
  '#6366f1', '#22d3ee', '#a78bfa', '#34d399', '#f59e0b',
  '#f87171', '#fb923c', '#e879f9',
]

interface Props {
  rows: Record<string, unknown>[]
  type: string
}

function getColumns(rows: Record<string, unknown>[]) {
  if (!rows.length) return { categoryKey: '', numericKeys: [] as string[] }
  const entries = Object.entries(rows[0])
  const numericKeys = entries
    .filter(([, v]) => typeof v === 'number')
    .map(([k]) => k)
  const categoryKey =
    entries.find(([, v]) => typeof v === 'string')?.[0] ?? Object.keys(rows[0])[0]
  return { categoryKey, numericKeys }
}

export default function ResultChart({ rows, type }: Props) {
  const { categoryKey, numericKeys } = getColumns(rows)

  if (!rows.length || !numericKeys.length) {
    return <ResultTable rows={rows} />
  }

  if (type === 'bar') {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={rows} margin={{ top: 10, right: 10, left: 0, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey={categoryKey}
            tick={{ fill: '#94a3b8', fontSize: 11 }}
            angle={-35}
            textAnchor="end"
            interval={0}
          />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
            labelStyle={{ color: '#f1f5f9' }}
          />
          <Legend wrapperStyle={{ color: '#94a3b8', paddingTop: 16 }} />
          {numericKeys.map((key, i) => (
            <Bar key={key} dataKey={key} fill={COLORS[i % COLORS.length]} radius={[4, 4, 0, 0]} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    )
  }

  if (type === 'line') {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={rows} margin={{ top: 10, right: 10, left: 0, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey={categoryKey} tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-35} textAnchor="end" />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }} />
          <Legend wrapperStyle={{ color: '#94a3b8' }} />
          {numericKeys.map((key, i) => (
            <Line key={key} type="monotone" dataKey={key} stroke={COLORS[i % COLORS.length]} strokeWidth={2} dot={false} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    )
  }

  if (type === 'pie') {
    const nameKey = categoryKey
    const valueKey = numericKeys[0]
    return (
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={rows}
            dataKey={valueKey}
            nameKey={nameKey}
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
            labelLine={false}
          >
            {rows.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }} />
          <Legend wrapperStyle={{ color: '#94a3b8' }} />
        </PieChart>
      </ResponsiveContainer>
    )
  }

  return <ResultTable rows={rows} />
}
