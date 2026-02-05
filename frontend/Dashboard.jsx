import React, { useState, useEffect } from 'react';

const Dashboard = () => {
    const [sessions, setSessions] = useState([]);
    const [selectedSession, setSelectedSession] = useState(null);
    const API_KEY = "hackathon-secret-key";

    useEffect(() => {
        fetchSessions();
        const interval = setInterval(fetchSessions, 5000); // Poll every 5s
        return () => clearInterval(interval);
    }, []);

    const fetchSessions = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/v1/sessions", {
                headers: { "X-API-Key": API_KEY }
            });
            const data = await res.json();
            setSessions(data);
        } catch (err) {
            console.error("Failed to fetch sessions", err);
        }
    };

    return (
        <div className="flex h-screen bg-gray-900 text-white font-sans">
            {/* Sidebar: Session List */}
            <div className="w-1/4 border-r border-gray-700 p-4 overflow-y-auto">
                <h1 className="text-xl font-bold mb-6 text-indigo-400">Honey-Pot Monitor</h1>
                <div className="space-y-3">
                    {sessions.map(s => (
                        <div
                            key={s.sessionId}
                            onClick={() => setSelectedSession(s)}
                            className={`p-3 rounded-lg cursor-pointer transition ${selectedSession?.sessionId === s.sessionId ? 'bg-indigo-600' : 'bg-gray-800 hover:bg-gray-700'}`}
                        >
                            <div className="flex justify-between items-center">
                                <span className="font-mono text-xs">{s.sessionId}</span>
                                {s.isScam && <span className="bg-red-500 text-[10px] px-2 py-1 rounded">SCAM</span>}
                            </div>
                            <div className="text-xs text-gray-400 mt-1">{s.messages.length} messages</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Main View: Chat & Intel */}
            <div className="flex-1 flex flex-col">
                {selectedSession ? (
                    <>
                        <div className="flex-1 p-6 overflow-y-auto space-y-4">
                            {selectedSession.messages.map((m, i) => (
                                <div key={i} className={`flex ${m.sender === 'Anjali' ? 'justify-start' : 'justify-end'}`}>
                                    <div className={`max-w-[70%] p-3 rounded-xl ${m.sender === 'Anjali' ? 'bg-gray-800 text-indigo-200' : 'bg-indigo-700 text-white'}`}>
                                        <div className="text-[10px] opacity-50 mb-1">{m.sender}</div>
                                        <div className="text-sm">{m.text}</div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Intel Panel */}
                        <div className="h-1/3 bg-gray-800 border-t border-gray-700 p-4 overflow-y-auto">
                            <h2 className="text-sm font-semibold text-indigo-400 mb-3">Extracted Intelligence</h2>
                            <div className="grid grid-cols-2 gap-4 text-xs">
                                <div>
                                    <h3 className="text-gray-500 mb-1 uppercase">UPI IDs</h3>
                                    {selectedSession.intelligence.upiIds.map(id => <div key={id} className="text-green-400 font-mono">{id}</div>)}
                                </div>
                                <div>
                                    <h3 className="text-gray-500 mb-1 uppercase">Bank Accounts</h3>
                                    {selectedSession.intelligence.bankAccounts.map(acc => <div key={acc} className="text-yellow-400 font-mono">{acc}</div>)}
                                </div>
                                <div>
                                    <h3 className="text-gray-500 mb-1 uppercase">Links</h3>
                                    {selectedSession.intelligence.phishingLinks.map(link => <div key={link} className="text-blue-400 underline truncate">{link}</div>)}
                                </div>
                                <div>
                                    <h3 className="text-gray-500 mb-1 uppercase">Status</h3>
                                    <div className={`font-bold ${selectedSession.callback_sent ? 'text-green-500' : 'text-orange-500'}`}>
                                        {selectedSession.callback_sent ? 'CALLBACK SENT' : 'PENDING'}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </>
                ) : (
                    <div className="flex-1 flex items-center justify-center text-gray-500 italic">
                        Select a session to view details
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
