import { useState, useEffect } from "react";
import { startLesson, submitAnswer, getStudentHistory, endSession } from "../api";
import ReactMarkdown from "react-markdown";

const StudentView = () => {
    const [studentId, setStudentId] = useState("");
    const [topic, setTopic] = useState("");
    const [sessionId, setSessionId] = useState(null);
    const [session, setSession] = useState(null);
    const [userAnswer, setUserAnswer] = useState("");
    const [confidence, setConfidence] = useState(50);
    const [feedback, setFeedback] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleStart = async (e) => {
        e.preventDefault();
        setLoading(true);
        setFeedback(null);
        try {
            const res = await startLesson(studentId, topic, confidence);
            if (res.success) {
                setSessionId(res.session_id);
                setSession(res.data);
            }
        } catch (err) {
            alert("Error starting lesson: " + err.message);
        }
        setLoading(false);
    };

    const handleSubmitAnswer = async () => {
        if (!userAnswer) return;
        setLoading(true);
        try {
            const res = await submitAnswer(sessionId, userAnswer, confidence);
            if (res.success) {
                setFeedback(res.data);
            }
        } catch (err) {
            alert("Error submitting answer");
        }
        setLoading(false);
    };

    const handleNext = () => {
        setFeedback(null);
        setUserAnswer("");
        if (feedback && feedback.has_next) {
            setSession(prev => ({
                ...prev,
                question: feedback.next_question,
                options: feedback.next_options,
                correct_option: feedback.next_correct_option
            }));
        }
    };

    const handleEndSession = async () => {
        setLoading(true);
        try {
            await endSession(sessionId);
            setSessionId(null);
            setSession(null);
            setFeedback(null);
            setUserAnswer("");
            fetchHistory();
        } catch (err) {
            alert("Error ending session");
        }
        setLoading(false);
    };

    const handleContinueTopic = async () => {
        setLoading(true);
        try {
            await endSession(sessionId);
            setSessionId(null);
            setSession(null);
            setFeedback(null);
            setUserAnswer("");
            fetchHistory();

            // Automatically start a new session with the same topic
            const res = await startLesson(studentId, topic, confidence);
            if (res.success) {
                setSessionId(res.session_id);
                setSession(res.data);
            }
        } catch (err) {
            alert("Error continuing topic: " + err.message);
        }
        setLoading(false);
    };

    const fetchHistory = async () => {
        if (!studentId) return;
        try {
            const res = await getStudentHistory(studentId);
            if (res.success) setHistory(res.history);
        } catch (err) { }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="text-center space-y-2">
                <h2 className="text-4xl font-black tracking-tight text-white sm:text-5xl bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
                    Personalized Study Hub
                </h2>
                <p className="text-slate-400">Master any topic with autonomous AI agents.</p>
            </div>

            {!session ? (
                <div className="glass-card">
                    <form onSubmit={handleStart} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <label className="text-sm font-semibold text-slate-400 ml-1">Student ID</label>
                                <input
                                    type="text"
                                    placeholder="e.g. Alex"
                                    className="input-field"
                                    value={studentId}
                                    onChange={(e) => setStudentId(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-semibold text-slate-400 ml-1">Target Topic</label>
                                <input
                                    type="text"
                                    placeholder="e.g. Quantum Physics"
                                    className="input-field"
                                    value={topic}
                                    onChange={(e) => setTopic(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div className="flex justify-between items-center text-sm font-semibold text-slate-400 ml-1">
                                <span>Initial Confidence Level</span>
                                <span className="text-indigo-400">{confidence}%</span>
                            </div>
                            <input
                                type="range"
                                min="0"
                                max="100"
                                value={confidence}
                                onChange={(e) => setConfidence(parseInt(e.target.value))}
                                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                            />
                        </div>

                        <button type="submit" className="btn-primary w-full" disabled={loading}>
                            {loading ? (
                                <span className="flex items-center justify-center gap-2">
                                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Synchronizing Agents...
                                </span>
                            ) : "Initialize Study Session"}
                        </button>
                    </form>
                </div>
            ) : (
                <div className="space-y-6">
                    <div className="flex flex-wrap gap-3">
                        <div className="bg-indigo-500/10 text-indigo-400 text-xs font-bold px-3 py-1 rounded-full border border-indigo-500/20 flex items-center gap-2">
                            <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-pulse" />
                            LEVEL: {session.level.toUpperCase()}
                        </div>
                        <div className="bg-purple-500/10 text-purple-400 text-xs font-bold px-3 py-1 rounded-full border border-purple-500/20">
                            STRATEGY: {session.strategy}
                        </div>
                    </div>

                    <div className="glass-card prose prose-invert max-w-none">
                        <h3 className="text-2xl font-bold text-white border-b border-slate-700 pb-4 mb-6">Lesson Content</h3>
                        <div className="text-slate-300 leading-relaxed text-lg italic mb-8">
                            <ReactMarkdown>{session.lesson}</ReactMarkdown>
                        </div>

                        <hr className="border-slate-700 my-8" />

                        {!feedback ? (
                            <div className="space-y-6">
                                <div className="space-y-2">
                                    <span className="text-xs font-black tracking-widest text-indigo-500 uppercase">Assessment Task</span>
                                    <h4 className="text-xl font-semibold text-white">{session.question}</h4>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    {session.options.map((opt, i) => (
                                        <button
                                            key={i}
                                            onClick={() => setUserAnswer(opt)}
                                            className={`text-left p-4 rounded-xl border transition-all ${userAnswer === opt
                                                ? "bg-indigo-600/20 border-indigo-500 text-white shadow-lg shadow-indigo-500/10 ring-1 ring-indigo-500"
                                                : "bg-slate-900/40 border-slate-700 text-slate-400 hover:border-slate-600 hover:bg-slate-800/40"
                                                }`}
                                        >
                                            <span className="inline-block w-6 h-6 rounded-full bg-slate-800 text-xs font-bold leading-6 text-center mr-3">
                                                {String.fromCharCode(65 + i)}
                                            </span>
                                            {opt}
                                        </button>
                                    ))}
                                </div>

                                <div className="pt-4 space-y-4">
                                    <div className="flex justify-between items-center text-sm font-semibold text-slate-400">
                                        <span>How confident are you in this answer?</span>
                                        <span className="text-indigo-400 font-bold">{confidence}%</span>
                                    </div>
                                    <input
                                        type="range"
                                        min="0"
                                        max="100"
                                        value={confidence}
                                        onChange={(e) => setConfidence(parseInt(e.target.value))}
                                        className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                                    />
                                    <button
                                        onClick={handleSubmitAnswer}
                                        className="btn-primary w-full disabled:opacity-50"
                                        disabled={loading || !userAnswer}
                                    >
                                        {loading ? "Validating Logic..." : "Submit Answer to Evaluator"}
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className={`p-8 rounded-2xl border-2 transition-all duration-500 ${feedback.correct
                                ? "bg-emerald-500/5 border-emerald-500/20 text-emerald-200"
                                : "bg-rose-500/5 border-rose-500/20 text-rose-200"
                                }`}>
                                <div className="flex items-center gap-4 mb-4">
                                    <div className={`p-3 rounded-full ${feedback.correct ? "bg-emerald-500/20" : "bg-rose-500/20"}`}>
                                        {feedback.correct ? "✓" : "×"}
                                    </div>
                                    <h3 className="text-2xl font-bold">{feedback.correct ? "Brilliant!" : "Not Quite Right"}</h3>
                                </div>
                                <p className="text-lg opacity-80 mb-8">{feedback.explanation}</p>
                                <div className="flex flex-col sm:flex-row gap-4">
                                    {feedback.has_next ? (
                                        <button onClick={handleNext} className="flex-1 bg-white/10 hover:bg-white/20 text-white py-4 rounded-xl font-bold transition-all border border-white/10">
                                            Continue to Next Question
                                        </button>
                                    ) : (
                                        <>
                                            <button onClick={handleContinueTopic} className="flex-1 bg-indigo-600 hover:bg-indigo-500 text-white py-4 rounded-xl font-bold transition-all border border-indigo-500">
                                                Continue Learning This Topic
                                            </button>
                                            <button onClick={handleEndSession} className="flex-1 bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-300 py-4 rounded-xl font-bold transition-all">
                                                Finish Session & View Score
                                            </button>
                                        </>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {history.length > 0 && !session && (
                <div className="space-y-4">
                    <h3 className="text-xl font-bold text-slate-300 flex items-center gap-2">
                        <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        Cognitive History
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {history.map((h, i) => (
                            <div key={i} className="glass-card p-4 space-y-2 border-l-4 border-l-indigo-500">
                                <div className="text-xs font-bold text-slate-500 uppercase">{h.strategy}</div>
                                <div className="text-lg font-bold text-white truncate">{h.topic}</div>
                                <div className="flex justify-between items-end">
                                    <span className={`text-3xl font-black ${h.score >= 80 ? 'text-emerald-400' : h.score >= 50 ? 'text-yellow-400' : 'text-rose-400'}`}>
                                        {Math.round(h.score)}% Score
                                    </span>
                                    <span className="text-xs text-slate-500 pb-1">Confidence: {Math.round(h.confidence)}%</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default StudentView;
