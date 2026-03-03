const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export const getMotivation = async () => {
    const res = await fetch(`${API_BASE}/motivation`);
    return res.json();
};

export const startLesson = async (studentId, topic, confidence = 50) => {
    const res = await fetch(`${API_BASE}/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: studentId, topic, confidence })
    });
    return res.json();
};

export const submitAnswer = async (studentId, topic, strategy, userAnswer, question, correctOption, confidence) => {
    const res = await fetch(`${API_BASE}/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student_id: studentId,
            topic,
            strategy,
            user_answer: userAnswer,
            question,
            correct_option: correctOption,
            confidence
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
