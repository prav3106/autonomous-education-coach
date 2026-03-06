import { useState } from 'react'
import StudentView from './components/StudentView'
import AdminView from './components/AdminView'
import AgentTerminal from './components/AgentTerminal'
import './index.css'

import Footer from './components/Footer'

function App() {
  const [activeTab, setActiveTab] = useState('student');
  const [isTerminalOpen, setIsTerminalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-dark text-slate-100 font-sans selection:bg-indigo-500/30 flex flex-col relative">
      <nav className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
              </div>
              <div>
                <span className="text-xl font-black bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                  Bay Harbor Coders
                </span>
                <p className="text-[10px] uppercase tracking-widest font-bold text-indigo-500">Autonomous Education Coach</p>
              </div>
            </div>

            <div className="flex space-x-2 bg-slate-950 p-1.5 rounded-2xl border border-slate-800">
              <button
                onClick={() => setActiveTab('student')}
                className={`px-6 py-2 rounded-xl text-sm font-bold transition-all ${activeTab === 'student'
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20'
                  : 'text-slate-400 hover:text-white'
                  }`}
              >
                Student Hub
              </button>
              <button
                onClick={() => setActiveTab('admin')}
                className={`px-6 py-2 rounded-xl text-sm font-bold transition-all ${activeTab === 'admin'
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20'
                  : 'text-slate-400 hover:text-white'
                  }`}
              >
                Admin Deck
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-grow">
        {activeTab === 'student' ? <StudentView /> : <AdminView />}
      </main>

      {/* Floating Toggle Button */}
      <button
        onClick={() => setIsTerminalOpen(!isTerminalOpen)}
        className={`fixed bottom-6 right-6 p-4 rounded-full shadow-2xl transition-all z-40 flex items-center justify-center ${isTerminalOpen ? 'bg-slate-800 text-slate-400 hover:text-white' : 'bg-emerald-600 text-emerald-50 hover:bg-emerald-500 shadow-emerald-500/30'
          }`}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 9l3 3-3 3m5 0h3M4 15V9a2 2 0 012-2h12a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2z" /></svg>
      </button>

      {/* Embedded Terminal */}
      <AgentTerminal isOpen={isTerminalOpen} onClose={() => setIsTerminalOpen(false)} />

      <Footer />
    </div>
  )
}

export default App
