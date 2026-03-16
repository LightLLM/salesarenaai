"use client";

import { useState } from 'react';
import { useLiveAudio } from '@/hooks/useLiveAudio';
import { Mic, MicOff, Activity, CheckCircle, ShieldAlert, BadgeDollarSign, FileWarning } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const PERSONAS = [
  { id: 'skeptic', name: 'The Skeptic CTO', icon: Activity, desc: 'Interrupts frequently, demands proof.' },
  { id: 'budget_guardian', name: 'Budget Guardian CFO', icon: BadgeDollarSign, desc: 'Cares only about ROI and cost.' },
  { id: 'procurement', name: 'Aggressive Procurement', icon: FileWarning, desc: 'Impatient, aggressive on pricing.' }
];

export default function Home() {
  const [selectedPersona, setSelectedPersona] = useState('skeptic');
  const [isSessionActive, setIsSessionActive] = useState(false);
  
  const { isConnected, error, scorecard, setScorecard, backendFeedback, mediaStream } = useLiveAudio(selectedPersona, isSessionActive);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 flex flex-col items-center py-12 px-4 selection:bg-indigo-500/30">
      
      {/* Header */}
      <div className="max-w-4xl w-full flex justify-between items-center mb-16">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
            SalesArena AI
          </h1>
          <p className="text-slate-400 mt-2 font-medium">Train like a closer.</p>
        </div>
        
        {/* Connection Status Indicator */}
        <div className="flex items-center gap-2 bg-slate-900/50 backdrop-blur-md px-4 py-2 rounded-full border border-slate-800">
           <div className={`w-2.5 h-2.5 rounded-full ${isSessionActive ? (isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400 animate-pulse') : 'bg-slate-600'}`} />
           <span className="text-sm font-medium text-slate-300">
             {!isSessionActive ? 'Ready' : (isConnected ? 'Live Agent Active' : 'Connecting...')}
           </span>
        </div>
      </div>

      <div className="w-full max-w-4xl grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Controls & Setup */}
        <div className="col-span-1 space-y-6">
          {!scorecard && (
             <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 backdrop-blur-sm">
                <h2 className="text-lg font-semibold mb-4 text-slate-200">Select Buyer Persona</h2>
                <div className="space-y-3">
                  {PERSONAS.map(p => {
                    const Icon = p.icon;
                    const isActive = selectedPersona === p.id;
                    return (
                      <button
                        key={p.id}
                        onClick={() => !isSessionActive && setSelectedPersona(p.id)}
                        disabled={isSessionActive}
                        className={`w-full text-left p-4 rounded-xl transition-all duration-300 border flex items-start gap-4 ${
                          isActive 
                            ? 'bg-indigo-500/10 border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.1)]' 
                            : 'bg-slate-950 border-slate-800 hover:border-slate-700 opacity-60'
                        }`}
                      >
                        <div className={`p-2 rounded-lg ${isActive ? 'bg-indigo-500/20 text-indigo-400' : 'bg-slate-800 text-slate-400'}`}>
                           <Icon size={20} />
                        </div>
                        <div>
                          <p className={`font-medium ${isActive ? 'text-indigo-100' : 'text-slate-300'}`}>{p.name}</p>
                          <p className="text-xs text-slate-500 mt-1 leading-relaxed">{p.desc}</p>
                        </div>
                      </button>
                    )
                  })}
                </div>
             </div>
          )}
        </div>

        {/* Right Column: Arena & Results */}
        <div className="col-span-1 lg:col-span-2 flex flex-col items-center justify-center min-h-[400px]">
          
          <AnimatePresence mode="wait">
             {/* Final Scorecard */}
             {scorecard ? (
                <motion.div 
                   key="scorecard"
                   initial={{ opacity: 0, y: 20, scale: 0.95 }}
                   animate={{ opacity: 1, y: 0, scale: 1 }}
                   className="w-full bg-slate-900 border border-slate-700/50 rounded-3xl p-8 shadow-2xl relative overflow-hidden"
                >
                   <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-indigo-500 via-cyan-400 to-indigo-500" />
                   <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                      <CheckCircle className="text-emerald-400" /> Session Complete
                   </h2>
                   
                   <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                      {['confidence', 'objection_handling', 'clarity', 'value_framing', 'closing'].map(metric => (
                        <div key={metric} className="bg-slate-950 p-4 rounded-2xl border border-slate-800 flex flex-col items-center justify-center">
                           <p className="text-4xl font-black text-white">{scorecard[metric] ?? 0}<span className="text-lg text-slate-500 font-medium">/10</span></p>
                           <p className="text-[10px] font-medium text-slate-400 uppercase tracking-widest mt-2">{metric.replace('_', ' ')}</p>
                        </div>
                      ))}
                   </div>

                   <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-2xl p-6">
                      <h3 className="text-indigo-300 font-semibold mb-2 text-sm uppercase tracking-wider">Coach Feedback</h3>
                      <p className="text-slate-300 leading-relaxed text-lg">{scorecard.feedback || "Good job! Focus on answering specific ROI questions more directly next time."}</p>
                   </div>
                   
                   <button 
                      onClick={() => { setScorecard(null); setIsSessionActive(false); }}
                      className="mt-8 w-full py-4 rounded-xl bg-slate-800 hover:bg-slate-700 font-medium transition-colors"
                   >
                     Start New Session
                   </button>
                </motion.div>
             ) : (
                /* Active Arena View */
                <motion.div 
                  key="arena"
                  initial={{ opacity: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="w-full flex flex-col items-center justify-center space-y-12"
                >
                  
                  {/* Avatar / Visualizer */}
                  <div className="relative group">
                     {/* Pulse animations when active */}
                     {isSessionActive && isConnected && (
                       <>
                         <div className="absolute inset-0 bg-indigo-500/20 rounded-full blur-3xl animate-pulse" />
                         <div className="absolute -inset-4 bg-cyan-500/10 rounded-full blur-2xl animate-[pulse_3s_ease-in-out_infinite]" />
                       </>
                     )}
                     
                     <div className={`relative z-10 w-48 h-48 rounded-full flex items-center justify-center border-4 transition-all duration-700 overflow-hidden ${
                         isSessionActive ? 'bg-slate-900 border-indigo-500/50 shadow-[0_0_40px_rgba(99,102,241,0.2)]' : 'bg-slate-900 border-slate-800'
                     }`}>
                        {isSessionActive ? (
                            <img src={`https://api.dicebear.com/7.x/bottts/svg?seed=${selectedPersona}&backgroundColor=transparent`} alt="AI Avatar" className="w-full h-full object-cover p-4" />
                        ) : (
                            <Mic className="w-16 h-16 text-slate-600" />
                        )}
                     </div>

                     {/* User Video Pip */}
                     {isSessionActive && mediaStream && (
                         <div className="absolute -bottom-4 -right-4 w-24 h-24 rounded-full overflow-hidden border-4 border-slate-900 bg-slate-950 z-20 shadow-2xl">
                           <video 
                             autoPlay 
                             playsInline 
                             muted 
                             className="w-full h-full object-cover"
                             style={{ transform: "scaleX(-1)" }}
                             ref={videoEl => {
                                 if (videoEl && videoEl.srcObject !== mediaStream) {
                                     videoEl.srcObject = mediaStream;
                                 }
                             }}
                           />
                         </div>
                     )}
                  </div>

                  {/* Feedback Overlay */}
                  <AnimatePresence>
                     {backendFeedback && (
                        <motion.div 
                          key="feedback"
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="absolute bottom-32 bg-amber-500/20 text-amber-200 px-6 py-3 rounded-full flex items-center gap-3 backdrop-blur-md border border-amber-500/30"
                        >
                           <ShieldAlert size={18} />
                           {backendFeedback}
                        </motion.div>
                     )}
                  </AnimatePresence>
                  
                  {error && (
                    <div className="text-red-400 bg-red-400/10 px-4 py-2 rounded-lg border border-red-400/20">
                      {error}
                    </div>
                  )}

                  {/* Call Action Button */}
                  <button
                     onClick={() => setIsSessionActive(!isSessionActive)}
                     className={`group relative overflow-hidden rounded-full font-bold text-lg px-12 py-5 transition-all duration-300 border-2 shadow-2xl ${
                        isSessionActive 
                          ? 'bg-red-500/10 text-red-500 border-red-500 hover:bg-red-500/20' 
                          : 'bg-indigo-600 text-white border-indigo-500 hover:bg-indigo-500 hover:scale-105 hover:shadow-indigo-500/25'
                     }`}
                  >
                     <div className="flex items-center gap-3">
                        {isSessionActive ? <MicOff size={24} /> : <Mic size={24} />}
                        <span>{isSessionActive ? 'End Session' : 'Start Pitching'}</span>
                     </div>
                  </button>

                </motion.div>
             )}
          </AnimatePresence>
        </div>
      </div>
      
    </main>
  );
}
