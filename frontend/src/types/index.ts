export interface Role {
  id: string
  name: string
  description: string | null
}

export interface User {
  id: string
  username: string
  email: string
  display_name: string
  is_active: boolean
  role: Role
  created_at: string
  updated_at: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface QueryRequest {
  question: string
  conversation_id?: string
}

export interface QueryResponse {
  question: string
  sql_query: string
  results: Record<string, unknown>[]
  row_count: number
  execution_time_ms: number
  chart_suggestion: string
  conversation_id: string
  message_id: string
  error: string | null
}

export interface Message {
  id: string
  conversation_id: string
  role: 'user' | 'assistant'
  content: string
  sql_query: string | null
  result_data: { rows: Record<string, unknown>[] } | null
  row_count: number | null
  execution_time_ms: number | null
  error: string | null
  chart_suggestion: string | null
  created_at: string
}

export interface Conversation {
  id: string
  user_id: string
  title: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ConversationDetail extends Conversation {
  messages: Message[]
}

export interface Department {
  id: string
  name: string
  code: string
  description: string | null
  created_at: string
  updated_at: string
}

export interface Employee {
  id: string
  employee_number: string
  first_name: string
  last_name: string
  email: string
  job_title: string
  salary: number
  employment_type: string
  status: string
  department_id: string
  created_at: string
  updated_at: string
}

export interface Project {
  id: string
  name: string
  description: string | null
  status: string
  start_date: string
  end_date: string | null
  department_id: string
  created_at: string
  updated_at: string
}

export interface Budget {
  id: string
  project_id: string
  total_amount: number
  spent_amount: number
  fiscal_year: number
  is_over_budget: boolean
  created_at: string
  updated_at: string
}
