import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API = '/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({ total: 0, todo: 0, inProgress: 0, done: 0 });
  const [filter, setFilter] = useState('ALL');
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadData = async () => {
    try {
      setError('');
      const [tasksRes, statsRes] = await Promise.all([
        fetch(`${API}/tasks`),
        fetch(`${API}/tasks/stats`),
      ]);

      if (!tasksRes.ok || !statsRes.ok) {
        throw new Error('Backend service unavailable');
      }

      const tasksData = await tasksRes.json();
      const statsData = await statsRes.json();

      setTasks(tasksData);
      setStats(statsData);
    } catch (err) {
      setError(err.message || 'Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const visibleTasks =
    filter === 'ALL' ? tasks : tasks.filter((t) => t.status === filter);

  const cycleStatus = async (task) => {
    const nextStatus =
      task.status === 'TODO'
        ? 'IN_PROGRESS'
        : task.status === 'IN_PROGRESS'
        ? 'DONE'
        : 'TODO';

    try {
      await fetch(`${API}/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...task, status: nextStatus }),
      });
      loadData();
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  const deleteTask = async (id) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    try {
      await fetch(`${API}/tasks/${id}`, { method: 'DELETE' });
      loadData();
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    try {
      await fetch(`${API}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: form.get('title'),
          description: form.get('description'),
          priority: form.get('priority'),
          assignee: form.get('assignee') || 'Piyush Kumar Gupta',
          status: 'TODO',
        }),
      });
      e.currentTarget.reset();
      setShowForm(false);
      loadData();
    } catch (err) {
      console.error('Error creating task:', err);
    }
  };

  return (
    <div className="app">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">T</span>
          <div>
            <div className="brand-title">TaskBoard</div>
            <div className="brand-subtitle">DevOps Cloud Platform</div>
          </div>
        </div>

        <nav className="nav-menu">
          <div className="nav-item active">
            <span>▦</span>
            <span>Dashboard</span>
          </div>
          <div className="nav-item">
            <span>✓</span>
            <span>My Tasks</span>
          </div>
          <div className="nav-item">
            <span>◫</span>
            <span>Deployments</span>
          </div>
          <div className="nav-item">
            <span>◌</span>
            <span>Activity</span>
          </div>
        </nav>

        <div className="side-bottom">
          <div className="pipeline-card">
            <div className="pipeline-title">DevOps Pipeline Active</div>
            <div className="pipeline-desc">CI/CD & Kubernetes cluster status: Normal</div>
          </div>

          <div className="profile">
            <div className="avatar">PK</div>
            <div className="profile-info">
              <b>Piyush Kumar Gupta</b>
              <small>DevOps Engineer</small>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main">
        <header className="main-header">
          <div>
            <p className="eyebrow">WORKSPACE / OVERVIEW</p>
            <h1 className="page-title">Workspace Dashboard 👋</h1>
            <p className="page-subtitle">
              Monitor deployments, track deliverables, and manage microservices.
            </p>
          </div>
          <button className="btn-primary" onClick={() => setShowForm(true)}>
            <span>＋</span> New task
          </button>
        </header>

        {error && (
          <div className="alert-box">
            ⚠ {error}. Ensure backend and PostgreSQL database are running, then retry.
          </div>
        )}

        {/* Top KPI Cards */}
        <section className="stats-grid">
          <StatCard label="Total Tasks" value={stats.total} icon="▦" />
          <StatCard label="To Do" value={stats.todo} icon="○" />
          <StatCard label="In Progress" value={stats.inProgress} icon="◔" />
          <StatCard label="Completed" value={stats.done} icon="✓" />
        </section>

        {/* Content Section: Task Board + Activity Feed */}
        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <div>
                <h2 className="panel-title">Tasks</h2>
                <p className="panel-subtitle">Manage sprint backlog and active items.</p>
              </div>

              <div className="filter-group">
                {['ALL', 'TODO', 'IN_PROGRESS', 'DONE'].map((s) => (
                  <button
                    key={s}
                    className={`filter-btn ${filter === s ? 'active' : ''}`}
                    onClick={() => setFilter(s)}
                  >
                    {s === 'ALL' ? 'All' : s.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>

            {loading ? (
              <div className="empty-state">Loading tasks…</div>
            ) : (
              <div className="table-responsive">
                <table>
                  <thead>
                    <tr>
                      <th>Task</th>
                      <th>Assignee</th>
                      <th>Priority</th>
                      <th>Status</th>
                      <th style={{ textAlign: 'right' }}>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {visibleTasks.map((task) => (
                      <tr key={task.id}>
                        <td>
                          <div className="task-cell">
                            <span className={`status-dot ${task.status.toLowerCase()}`}></span>
                            <div className="task-cell-content">
                              <b>{task.title}</b>
                              {task.description && <small>{task.description}</small>}
                            </div>
                          </div>
                        </td>
                        <td>{task.assignee}</td>
                        <td>
                          <span className={`badge-priority ${task.priority.toLowerCase()}`}>
                            {task.priority}
                          </span>
                        </td>
                        <td>
                          <span className={`badge-status ${task.status.toLowerCase()}`}>
                            {task.status.replace('_', ' ')}
                          </span>
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          <div style={{ display: 'inline-flex', gap: '6px' }}>
                            <button
                              className="action-btn"
                              onClick={() => cycleStatus(task)}
                              title="Advance status"
                            >
                              ↻
                            </button>
                            <button
                              className="action-btn"
                              onClick={() => deleteTask(task.id)}
                              title="Delete task"
                            >
                              ×
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {!visibleTasks.length && (
                  <div className="empty-state">No tasks found for current filter.</div>
                )}
              </div>
            )}
          </div>

          {/* Activity Timeline */}
          <aside className="panel">
            <div className="panel-header">
              <div>
                <h2 className="panel-title">Recent Activity</h2>
                <p className="panel-subtitle">Live CI/CD and deployment logs.</p>
              </div>
            </div>

            <div className="activity-list">
              <ActivityItem icon="✓" text="Monitoring dashboard deployed" time="10 min ago" />
              <ActivityItem icon="◔" text="EKS cluster healthy in ap-south-1" time="25 min ago" />
              <ActivityItem icon="＋" text="Docker image pushed to GHCR" time="1 hr ago" />
              <ActivityItem icon="↗" text="GitHub Actions tests passing" time="2 hrs ago" />
            </div>

            <div className="ci-pipeline-bar">
              <span className="done">Test</span>
              <i></i>
              <span className="done">Build</span>
              <i></i>
              <span className="done">Scan</span>
              <i></i>
              <span>Deploy</span>
            </div>
          </aside>
        </section>

        {/* Modal Dialog */}
        {showForm && (
          <div className="modal-backdrop" onClick={() => setShowForm(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <div>
                  <p className="eyebrow">CREATE TASK</p>
                  <h2 className="panel-title" style={{ fontSize: '20px' }}>
                    Add a new task
                  </h2>
                </div>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowForm(false)}
                >
                  ×
                </button>
              </div>

              <form onSubmit={handleCreateTask}>
                <div className="form-field">
                  <label>Task Title</label>
                  <input
                    name="title"
                    required
                    placeholder="e.g. Configure production Ingress controller"
                  />
                </div>

                <div className="form-field">
                  <label>Description</label>
                  <textarea
                    name="description"
                    placeholder="What requirements or implementation details?"
                  />
                </div>

                <div className="form-row">
                  <div className="form-field">
                    <label>Priority</label>
                    <select name="priority" defaultValue="MEDIUM">
                      <option value="LOW">LOW</option>
                      <option value="MEDIUM">MEDIUM</option>
                      <option value="HIGH">HIGH</option>
                    </select>
                  </div>

                  <div className="form-field">
                    <label>Assignee</label>
                    <input name="assignee" defaultValue="Piyush Kumar Gupta" />
                  </div>
                </div>

                <button type="submit" className="btn-submit">
                  Create task
                </button>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function StatCard({ label, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div className="stat-info">
        <small>{label}</small>
        <strong>{value}</strong>
        <span>Realtime count</span>
      </div>
    </div>
  );
}

function ActivityItem({ icon, text, time }) {
  return (
    <div className="activity-item">
      <div className="activity-icon">{icon}</div>
      <div className="activity-content">
        <b>{text}</b>
        <small>{time}</small>
      </div>
    </div>
  );
}

const root = createRoot(document.getElementById('root'));
root.render(<App />);
