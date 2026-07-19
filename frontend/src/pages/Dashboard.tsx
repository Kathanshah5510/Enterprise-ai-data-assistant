import { useQuery } from '@tanstack/react-query'
import { Users, Building2, FolderKanban, DollarSign, TrendingUp, AlertTriangle } from 'lucide-react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, PieChart, Pie, Legend,
} from 'recharts'
import Sidebar from '../components/Sidebar'
import { listDepartments } from '../api/departments'
import { listEmployees } from '../api/employees'
import { listProjects } from '../api/projects'
import { listBudgets } from '../api/budgets'
import type { Employee, Budget } from '../types'

const COLORS = ['#6366f1', '#22d3ee', '#a78bfa', '#34d399', '#f59e0b', '#f87171', '#fb923c']

function KpiCard({ icon: Icon, label, value, sub, color = 'indigo' }: {
  icon: React.ElementType; label: string; value: string | number; sub?: string; color?: string
}) {
  const colors: Record<string, string> = {
    indigo: 'bg-indigo-600/20 text-indigo-400',
    cyan: 'bg-cyan-600/20 text-cyan-400',
    violet: 'bg-violet-600/20 text-violet-400',
    emerald: 'bg-emerald-600/20 text-emerald-400',
  }
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-slate-400">{label}</span>
        <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${colors[color]}`}>
          <Icon size={18} />
        </div>
      </div>
      <p className="text-2xl font-bold text-white">{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-1">{sub}</p>}
    </div>
  )
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">{title}</h3>
      {children}
    </div>
  )
}

function tooltipStyle() {
  return { background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#f1f5f9' }
}

export default function Dashboard() {
  const depts = useQuery({ queryKey: ['departments'], queryFn: listDepartments })
  const employees = useQuery({ queryKey: ['employees'], queryFn: () => listEmployees(100), retry: 0 })
  const projects = useQuery({ queryKey: ['projects'], queryFn: () => listProjects(100) })
  const budgets = useQuery({ queryKey: ['budgets'], queryFn: () => listBudgets(100), retry: 0 })

  // Employees per department
  const empByDept = (() => {
    if (!employees.data || !depts.data) return []
    const map = new Map(depts.data.map((d) => [d.id, d.name]))
    const counts: Record<string, number> = {}
    employees.data.forEach((e: Employee) => {
      const name = map.get(e.department_id) ?? 'Unknown'
      counts[name] = (counts[name] ?? 0) + 1
    })
    return Object.entries(counts).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count)
  })()

  // Avg salary per department
  const salaryByDept = (() => {
    if (!employees.data || !depts.data) return []
    const map = new Map(depts.data.map((d) => [d.id, d.name]))
    const sums: Record<string, { total: number; count: number }> = {}
    employees.data.forEach((e: Employee) => {
      const name = map.get(e.department_id) ?? 'Unknown'
      if (!sums[name]) sums[name] = { total: 0, count: 0 }
      sums[name].total += Number(e.salary)
      sums[name].count += 1
    })
    return Object.entries(sums)
      .map(([name, { total, count }]) => ({ name, avg_salary: Math.round(total / count) }))
      .sort((a, b) => b.avg_salary - a.avg_salary)
  })()

  // Projects by status
  const projectsByStatus = (() => {
    if (!projects.data) return []
    const counts: Record<string, number> = {}
    projects.data.forEach((p) => { counts[p.status] = (counts[p.status] ?? 0) + 1 })
    return Object.entries(counts).map(([status, count]) => ({ status, count }))
  })()

  // Budget summary
  const budgetSummary = (() => {
    if (!budgets.data) return null
    const total = budgets.data.reduce((s: number, b: Budget) => s + Number(b.total_amount), 0)
    const spent = budgets.data.reduce((s: number, b: Budget) => s + Number(b.spent_amount), 0)
    const overBudget = budgets.data.filter((b: Budget) => b.is_over_budget).length
    return { total, spent, overBudget }
  })()

  const totalEmployees = employees.data?.length ?? '—'
  const totalDepts = depts.data?.length ?? '—'
  const totalProjects = projects.data?.length ?? '—'
  const totalBudget = budgetSummary ? `$${(budgetSummary.total / 1_000_000).toFixed(1)}M` : '—'

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="mb-6">
            <h1 className="text-xl font-bold text-white">Dashboard</h1>
            <p className="text-sm text-slate-500">NovaTech Solutions — live data overview</p>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <KpiCard icon={Users} label="Total Employees" value={totalEmployees} sub="Across all departments" color="indigo" />
            <KpiCard icon={Building2} label="Departments" value={totalDepts} sub="Active business units" color="cyan" />
            <KpiCard icon={FolderKanban} label="Projects" value={totalProjects} sub="All statuses" color="violet" />
            <KpiCard icon={DollarSign} label="Total Budget" value={totalBudget}
              sub={budgetSummary ? `${budgetSummary.overBudget} over budget` : undefined} color="emerald" />
          </div>

          {/* Charts row 1 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
            <ChartCard title="Employees by Department">
              {employees.isError ? (
                <div className="flex items-center gap-2 text-slate-500 text-sm py-8 justify-center">
                  <AlertTriangle size={16} /> Access restricted for your role
                </div>
              ) : empByDept.length > 0 ? (
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={empByDept} margin={{ top: 0, right: 0, left: -20, bottom: 50 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-35} textAnchor="end" interval={0} />
                    <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
                    <Tooltip contentStyle={tooltipStyle()} />
                    <Bar dataKey="count" name="Employees" radius={[4, 4, 0, 0]}>
                      {empByDept.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-40">
                  <div className="w-6 h-6 border-2 border-slate-700 border-t-indigo-500 rounded-full animate-spin" />
                </div>
              )}
            </ChartCard>

            <ChartCard title="Projects by Status">
              {projectsByStatus.length > 0 ? (
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie data={projectsByStatus} dataKey="count" nameKey="status" cx="50%" cy="45%"
                      outerRadius={95} label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      labelLine={false}>
                      {projectsByStatus.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                    </Pie>
                    <Tooltip contentStyle={tooltipStyle()} />
                    <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-40">
                  <div className="w-6 h-6 border-2 border-slate-700 border-t-indigo-500 rounded-full animate-spin" />
                </div>
              )}
            </ChartCard>
          </div>

          {/* Charts row 2 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <ChartCard title="Average Salary by Department">
              {employees.isError ? (
                <div className="flex items-center gap-2 text-slate-500 text-sm py-8 justify-center">
                  <AlertTriangle size={16} /> Access restricted for your role
                </div>
              ) : salaryByDept.length > 0 ? (
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={salaryByDept} margin={{ top: 0, right: 0, left: 10, bottom: 50 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-35} textAnchor="end" interval={0} />
                    <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                    <Tooltip contentStyle={tooltipStyle()} formatter={(v: number) => [`$${v.toLocaleString()}`, 'Avg Salary']} />
                    <Bar dataKey="avg_salary" name="Avg Salary" radius={[4, 4, 0, 0]}>
                      {salaryByDept.map((_, i) => <Cell key={i} fill={COLORS[(i + 2) % COLORS.length]} />)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : null}
            </ChartCard>

            <ChartCard title="Budget Utilization">
              {budgets.isError ? (
                <div className="flex items-center gap-2 text-slate-500 text-sm py-8 justify-center">
                  <AlertTriangle size={16} /> Access restricted for your role
                </div>
              ) : budgetSummary ? (
                <div className="space-y-4 py-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1.5">
                      <span className="text-slate-400">Budget utilization</span>
                      <span className="text-slate-300 font-medium">
                        {((budgetSummary.spent / budgetSummary.total) * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="h-3 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all"
                        style={{
                          width: `${Math.min((budgetSummary.spent / budgetSummary.total) * 100, 100)}%`,
                          background: budgetSummary.overBudget > 0 ? '#f87171' : '#6366f1',
                        }}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-4 pt-2">
                    {[
                      { label: 'Total Budget', value: `$${(budgetSummary.total / 1_000_000).toFixed(2)}M` },
                      { label: 'Total Spent', value: `$${(budgetSummary.spent / 1_000_000).toFixed(2)}M` },
                      { label: 'Over Budget', value: budgetSummary.overBudget, warn: budgetSummary.overBudget > 0 },
                    ].map(({ label, value, warn }) => (
                      <div key={label} className="text-center">
                        <p className={`text-lg font-bold ${warn ? 'text-red-400' : 'text-white'}`}>{value}</p>
                        <p className="text-xs text-slate-500">{label}</p>
                        {warn && <TrendingUp size={12} className="text-red-400 mx-auto mt-1" />}
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-40">
                  <div className="w-6 h-6 border-2 border-slate-700 border-t-indigo-500 rounded-full animate-spin" />
                </div>
              )}
            </ChartCard>
          </div>
        </div>
      </div>
    </div>
  )
}
