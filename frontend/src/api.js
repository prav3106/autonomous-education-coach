const API_BASE = "http://localhost:8000";

export const getMotivation = async () => {
    const res = await fetch(`${API_BASE}/motivation`);
    return res.json();
};

export const startLesson = async (studentId, topic, confidence = 50) => {
    const res = await fetch(`${API_BASE}/start-session`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: studentId, topic, confidence })
    });
    return res.json();
};

export const submitAnswer = async (sessionId, userAnswer, confidence) => {
    const res = await fetch(`${API_BASE}/answer-question`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: sessionId,
            user_answer: userAnswer,
            confidence
        })
    });
    return res.json();
};

export const endSession = async (sessionId) => {
    const res = await fetch(`${API_BASE}/end-session`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: sessionId
        })
    });
    return res.json();
};

export const getStudentHistory = async (studentId) => {
    const res = await fetch(`${API_BASE}/student/${studentId}`);
    return res.json();
};

export const getAdminDashboard = async () => {
    const res = await fetch(`${API_BASE}/admin/dashboard`);
    return res.json();
};

export const getAgentLogs = async (since = 0) => {
    try {
        const res = await fetch(`${API_BASE}/agent-logs?since=${since}`);
        return res.json();
    } catch (e) {
        console.error("Failed to fetch agent logs", e);
        return { success: false, data: [] };
    }
};
