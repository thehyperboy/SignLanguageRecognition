import React from "react";
import { motion } from "framer-motion";
import { 
  ArrowLeft, 
  ShieldCheck, 
  Volume2, 
  Eye, 
  Lock, 
  Sparkles, 
  ArrowRight,
  Heart,
  CheckCircle2,
  Users
} from "lucide-react";

export const AccessibilityPage = ({ onBackToHome, onOpenTracker }) => {
  return (
    <div className="min-h-screen bg-[#070708] text-white py-12 px-6 sm:px-12 bg-dots-dark">
      <div className="max-w-7xl mx-auto">
        
        {/* Breadcrumb Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-12 pb-6 border-b border-zinc-800">
          <div className="flex items-center gap-4">
            <button
              onClick={onBackToHome}
              className="px-4 py-2 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-xs font-bold text-zinc-300 hover:text-white flex items-center gap-2 transition-all shadow-md active:scale-95"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Overview</span>
            </button>

            <div>
              <div className="flex items-center gap-2 text-purple-400 text-xs font-bold tracking-wider uppercase mb-1">
                <ShieldCheck className="w-4 h-4" />
                <span>Inclusive Technology</span>
              </div>
              <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                Universal Communication & Accessibility
              </h1>
            </div>
          </div>

          <button
            onClick={onOpenTracker}
            className="px-6 py-2.5 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 text-white text-xs font-black tracking-wide uppercase hover:opacity-95 transition-all shadow-xl active:scale-95 flex items-center gap-2"
          >
            <span>Launch Live Studio</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Mission Statement Hero Card */}
        <div className="p-8 sm:p-12 rounded-3xl bg-gradient-to-br from-purple-950/40 via-zinc-900 to-[#0F0F12] border border-purple-800/30 shadow-2xl mb-12 relative overflow-hidden">
          <div className="max-w-3xl relative z-10">
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40 mb-4 inline-block">
              Breaking Barriers
            </span>
            <h2 className="text-2xl sm:text-3xl font-black text-white tracking-tight leading-snug mb-4">
              Enabling natural, fluid dialogue between Deaf signers and non-signing hearing communities.
            </h2>
            <p className="text-sm text-zinc-300 leading-relaxed">
              Traditional sign language recognition often required $2,000+ sensory cyber-gloves or cloud servers that compromised visual privacy. SignFlow utilizes state-of-the-art spatial landmark extraction and temporal neural nets to run entirely locally in real-time on standard webcam hardware.
            </p>
          </div>
        </div>

        {/* 4 Core Accessibility Pillars */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          
          {/* Pillar 1: Vocal Audio Engine */}
          <div className="p-8 rounded-3xl bg-[#0F0F12] border border-zinc-800 shadow-xl flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/30 text-purple-400 flex items-center justify-center mb-6">
                <Volume2 className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-black text-white mb-2">Bi-Directional Speech Synthesis</h3>
              <p className="text-xs text-zinc-400 leading-relaxed mb-6">
                Integrated with pyttsx3 offline text-to-speech engine. As gestures like "HELLO", "THANK YOU", or "HELP" are recognized with high confidence, the system vocalizes the sign through the computer speakers with sub-100ms latency.
              </p>
            </div>
            <div className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 text-[11px] text-zinc-300 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Hands-free voice output for seamless in-person conversations.</span>
            </div>
          </div>

          {/* Pillar 2: Zero Hardware Cost */}
          <div className="p-8 rounded-3xl bg-[#0F0F12] border border-zinc-800 shadow-xl flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center mb-6">
                <Eye className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-black text-white mb-2">Pure Optical Computer Vision</h3>
              <p className="text-xs text-zinc-400 leading-relaxed mb-6">
                Uses 258 MediaPipe Holistic landmarks (face, pose, hands) captured by ordinary 640×480 webcams. Zero need for specialized infrared sensors, colored markers, or awkward wearable equipment.
              </p>
            </div>
            <div className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 text-[11px] text-zinc-300 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Democratizes accessibility technology on any laptop or desktop.</span>
            </div>
          </div>

          {/* Pillar 3: Privacy by Design */}
          <div className="p-8 rounded-3xl bg-[#0F0F12] border border-zinc-800 shadow-xl flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center mb-6">
                <Lock className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-black text-white mb-2">Private & Local Computation</h3>
              <p className="text-xs text-zinc-400 leading-relaxed mb-6">
                All video processing, MediaPipe landmark calculations, and LSTM neural classifications happen on your local device. Your video feed is never stored, tracked, or sent to external cloud servers.
              </p>
            </div>
            <div className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 text-[11px] text-zinc-300 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Full compliance with privacy standards and personal data protection.</span>
            </div>
          </div>

          {/* Pillar 4: Multi-Sensory Feedback */}
          <div className="p-8 rounded-3xl bg-[#0F0F12] border border-zinc-800 shadow-xl flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-400 flex items-center justify-center mb-6">
                <Sparkles className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-black text-white mb-2">Confidence & Temporal Stability</h3>
              <p className="text-xs text-zinc-400 leading-relaxed mb-6">
                Visual progress tracking gives signers continuous visual feedback of their 30-frame sequence buffer. The prediction stabilizes and latches onto recognized gestures for 1.5 seconds to prevent visual flicker.
              </p>
            </div>
            <div className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 text-[11px] text-zinc-300 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Intuitive visual confidence meter and green validation halos.</span>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
