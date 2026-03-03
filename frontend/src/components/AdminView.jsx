import { useState, useEffect } from "react";
import { getAdminDashboard } from "../api";

const AdminView = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = async () => {
        try {
            const res = await getAdminDashboard();
            if (res.success) setData(res.data);
        } catch (err) {
            console.error(err);
        }
        setLoading(false);
    };

    if (loading) return (
        <div className="flex items-center justify-center p-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
        </div>
    );

    return (
        <div className="space-y-8 animate-in fade-in duration-1000">
            <div className="flex justify-between items-end">
                <div>
                    <h2 className="text-3xl font-black text-white">Institutional Oversight</h2>
                    <p className="text-slate-400">Agentic performance metrics & student metrics.</p>
                </div>
                <button onClick={fetchDashboard} className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-lg text-sm border border-slate-700 transition-colors">
                    Refresh Real-time
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="glass-card p-6 !rounded-2xl border-b-4 border-b-indigo-500">
                    <div className="text-sm font-bold text-slate-500 uppercase">Active Students</div>
                    <div className="text-4xl font-black text-white mt-2">{data?.total_students || 0}</div>
                </div>
                <div className="glass-card p-6 !rounded-2xl border-b-4 border-b-emerald-500">
                    <div className="text-sm font-bold text-slate-500 uppercase">Avg. Accuracy</div>
                    <div className="text-4xl font-black text-white mt-2">{data?.average_score?.toFixed(1) || 0}%</div>
                </div>
                <div className="glass-card p-6 !rounded-2xl border-b-4 border-b-amber-500">
                    <div className="text-sm font-bold text-slate-500 uppercase">Agent Loop Speed</div>
                    <div className="text-4xl font-black text-white mt-2">0.8s</div>
                </div>
                <div className="glass-card p-6 !rounded-2xl border-b-4 border-b-purple-500">
                    <div className="text-sm font-bold text-slate-500 uppercase">Weak Concepts</div>
                    <div className="text-sm font-bold text-white mt-2 truncate">
                        {data?.weakest_topics?.join(", ") || "None identified"}
                    </div>
                </div>
            </div>

            <div className="glass-card !p-0 overflow-hidden">
                <div className="p-6 border-b border-slate-700 flex justify-between items-center bg-slate-800/20">
                    <h3 className="font-bold text-xl text-white">Granular Student History (Agent Logs)</h3>
                    <span className="text-xs font-mono text-slate-500">Connected to MySQL Production</span>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-400 text-xs font-black uppercase tracking-widest border-b border-slate-700">
                                <th className="px-6 py-4">Student ID</th>
                                <th className="px-6 py-4">Topic</th>
                                <th className="px-6 py-4">Conf. %</th>
                                <th className="px-6 py-4">Performance</th>
                                <th className="px-6 py-4">Agent Strategy</th>
                                <th className="px-6 py-4">Timestamp</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-700/50">
                            {data?.all_records?.map((record, i) => (
                                <tr key={i} className="hover:bg-white/[0.02] transition-colors">
                                    <td className="px-6 py-4 font-bold text-indigo-400 font-mono">{record.student_id}</td>
                                    <td className="px-6 py-4 text-slate-300 font-medium">{record.topic}</td>
                                    <td className="px-6 py-4">
                                        <div className="w-full bg-slate-900 rounded-full h-1.5 w-16">
                                            <div className="bg-indigo-500 h-1.5 rounded-full" style={{ width: `${record.confidence}%` }}></div>
                                        </div>
                                        <span className="text-[10px] text-slate-500 mt-1 block">{record.confidence}% confidence</span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={`px-2 py-1 rounded-md text-xs font-bold ${record.score === 100 ? 'bg-emerald-500/10 text-emerald-500' : 'bg-rose-500/10 text-rose-500'}`}>
                                            {record.score === 100 ? 'CORRECT' : 'INCORRECT'}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="text-slate-400 text-xs italic font-serif">"{record.strategy}"</span>
                                    </td>
                                    <td className="px-6 py-4 text-slate-500 text-xs font-mono">{record.date}</td>
                                </tr>
                            ))}
                            {(!data?.all_records || data.all_records.length === 0) && (
                                <tr>
                                    <td colSpan="6" className="px-6 py-10 text-center text-slate-500 italic">No historical data segments found in database.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default AdminView;
