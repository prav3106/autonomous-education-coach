import { useState, useEffect, useRef } from 'react';
import { getAgentLogs } from '../api';

const AgentTerminal = ({ isOpen, onClose }) => {
    const [logs, setLogs] = useState([]);
    const [lastTimestamp, setLastTimestamp] = useState(0);
    const bottomRef = useRef(null);

    useEffect(() => {
        if (!isOpen) return;

        let pollInterval = setInterval(async () => {
            const res = await getAgentLogs(lastTimestamp);
            if (res.success && res.data && res.data.length > 0) {
                // Find highest timestamp properly
                const maxTs = Math.max(...res.data.map(l => l.timestamp));
                setLastTimestamp(maxTs);
                setLogs(prev => [...prev, ...res.data]);
            }
        }, 1000);

        return () => clearInterval(pollInterval);
    }, [isOpen, lastTimestamp]);

    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [logs, isOpen]);

    if (!isOpen) return null;

    const getAgentColor = (agent) => {
        switch (agent) {
            case "Analyzer": return "text-indigo-400";
            case "Planner": return "text-amber-400";
            case "Teacher": return "text-emerald-400";
            case "Evaluator": return "text-rose-400";
            case "Memory": return "text-purple-400";
            case "System": return "text-cyan-400";
            default: return "text-slate-400";
        }
    };

    return (
        <div className="fixed bottom-0 right-0 w-full md:w-[600px] h-[40vh] md:h-[60vh] bg-slate-950 text-emerald-500 font-mono text-xs md:text-sm p-4 overflow-hidden flex flex-col shadow-2xl z-50 animate-in slide-in-from-bottom border-t md:border-l border-slate-800 rounded-tl-xl">
            <div className="flex justify-between items-center pb-2 border-b border-slate-800 mb-2 shrink-0">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                    <h3 className="text-white font-bold uppercase tracking-widest text-xs">Live Agent Observatory</h3>
                </div>
                <div className="flex gap-4 items-center">
                    <button onClick={() => setLogs([])} className="text-slate-500 hover:text-white transition-colors">Clear</button>
                    <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                </div>
            </div>
            <div className="flex-1 overflow-y-auto pr-2 space-y-1 agent-scroll">
                {logs.length === 0 ? (
                    <div className="text-slate-600 italic">Waiting for agents to begin processing...</div>
                ) : (
                    logs.map((log, i) => (
                        <div key={i} className="whitespace-pre-wrap break-words leading-tight">
                            <span className="text-slate-500 select-none">[{new Date(log.timestamp * 1000).toLocaleTimeString()}] </span>
                            <span className={`font-bold ${getAgentColor(log.agent)}`}>{log.agent}</span>
                            <span className="text-slate-400 cursor-text"> {log.payload}</span>
                        </div>
                    ))
                )}
                <div ref={bottomRef} className="h-1 shrink-0" />
            </div>
        </div>
    );
};

export default AgentTerminal;
