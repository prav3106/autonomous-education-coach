import { useState, useEffect } from "react";
import { getMotivation } from "../api";

const Footer = () => {
    const [quote, setQuote] = useState("Loading inspiration...");
    const [fade, setFade] = useState(true);

    useEffect(() => {
        fetchQuote();
        const interval = setInterval(fetchQuote, 10000); // New quote every 10s
        return () => clearInterval(interval);
    }, []);

    const fetchQuote = async () => {
        setFade(false);
        try {
            const res = await getMotivation();
            if (res.quote) {
                setTimeout(() => {
                    setQuote(res.quote);
                    setFade(true);
                }, 500);
            }
        } catch (err) {
            setQuote("Keep expanding your horizons.");
            setFade(true);
        }
    };

    return (
        <footer className="border-t border-slate-800 py-16 bg-slate-950/50 mt-auto">
            <div className="max-w-7xl mx-auto px-4 text-center space-y-4">
                <div className={`transition-all duration-1000 transform ${fade ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}`}>
                    <p className="text-xl font-serif italic text-slate-400 max-w-2xl mx-auto leading-relaxed">
                        "{quote}"
                    </p>
                </div>
                <div className="pt-8 flex justify-center gap-6 grayscale opacity-30 hover:grayscale-0 hover:opacity-100 transition-all">
                    <span className="text-[10px] font-black tracking-[0.3em] text-slate-500 uppercase">Neural Intelligence Framework</span>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
