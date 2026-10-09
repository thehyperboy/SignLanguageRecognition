import React from "react";
import { motion } from "framer-motion";
import { 
  Camera, 
  ArrowRight, 
  Sparkles, 
  Layers, 
  Cpu, 
  Volume2, 
  Eye, 
  CheckCircle2 
} from "lucide-react";

/**
 * 3D Illustrated Character 1: Vision Landmark Character (Coral Card)
 * Matching reference image: Black hoodie, pink wireframe glasses, cursor arrows, smiling face.
 */
const VisionCharacter = () => (
  <div className="relative w-48 h-56 flex flex-col items-center justify-end select-none group-hover:scale-105 transition-transform duration-500">
    {/* Floating cursor selection frame around head */}
    <div className="absolute top-2 w-36 h-28 border-2 border-dashed border-white/60 rounded-2xl flex items-center justify-center pointer-events-none">
      {/* Corner bounding points */}
      <div className="absolute -top-1.5 -left-1.5 w-3 h-3 bg-white rounded-sm shadow-md" />
      <div className="absolute -top-1.5 -right-1.5 w-3 h-3 bg-white rounded-sm shadow-md" />
      <div className="absolute -bottom-1.5 -left-1.5 w-3 h-3 bg-white rounded-sm shadow-md" />
      <div className="absolute -bottom-1.5 -right-1.5 w-3 h-3 bg-white rounded-sm shadow-md" />
      
      {/* Pink cursor arrows */}
      <span className="absolute -left-3 top-6 text-pink-300 text-sm">◀</span>
      <span className="absolute -right-3 bottom-6 text-pink-300 text-sm">▶</span>
    </div>

    {/* Character Head */}
    <div className="w-24 h-22 rounded-[28px] bg-gradient-to-b from-white via-zinc-100 to-zinc-200 shadow-2xl relative flex flex-col items-center justify-center z-10 border border-white">
      {/* Cute Face & Wireframe Glasses */}
      <div className="relative flex items-center justify-center">
        {/* Pink Eyeglass Frames */}
        <div className="flex gap-2.5 z-20">
          <div className="w-7 h-7 rounded-full border-3 border-rose-500 bg-white/40 flex items-center justify-center shadow-sm">
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-950" />
          </div>
          <div className="w-7 h-7 rounded-full border-3 border-rose-500 bg-white/40 flex items-center justify-center shadow-sm">
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-950" />
          </div>
        </div>
        {/* Glasses Bridge */}
        <div className="absolute w-4 h-1 bg-rose-500 -top-0 z-10" />
      </div>
      {/* Smile */}
      <div className="w-3.5 h-1.5 border-b-2 border-zinc-950 rounded-full mt-2" />
    </div>

    {/* Black Hoodie Body with "interfaces" typography */}
    <div className="w-36 h-24 bg-gradient-to-b from-[#18181B] to-[#09090B] rounded-t-[36px] relative -mt-5 flex flex-col items-center justify-center shadow-2xl border-t border-zinc-700/50 overflow-hidden">
      {/* Hoodie strings */}
      <div className="flex gap-4 -mt-3">
        <div className="w-0.5 h-4 bg-zinc-500 rounded-full" />
        <div className="w-0.5 h-4 bg-zinc-500 rounded-full" />
      </div>
      {/* Stylized Logo text */}
      <div className="mt-2 text-[11px] font-black tracking-widest text-white/90 italic font-mono uppercase">
        interfaces
      </div>
    </div>
  </div>
);

/**
 * 3D Illustrated Character 2: Neural Speech Character (Blue Card)
 * Matching reference image: Blue hoodie, 3D red/cyan glasses, green speech bubble, cute smile.
 */
const NeuralCharacter = () => (
  <div className="relative w-48 h-56 flex flex-col items-center justify-end select-none group-hover:scale-105 transition-transform duration-500">
    {/* Green Speech Bubble Floating Above Head */}
    <div className="absolute top-0 px-4 py-1.5 rounded-full bg-[#22C55E] text-zinc-950 text-xs font-black shadow-lg flex items-center gap-1.5 z-20 border border-green-300 animate-bounce" style={{ animationDuration: "3s" }}>
      <Sparkles className="w-3 h-3 text-zinc-950" />
      <span>"HELLO"</span>
    </div>

    {/* Character Head */}
    <div className="w-24 h-22 rounded-[28px] bg-gradient-to-b from-cyan-300 via-sky-400 to-blue-500 shadow-2xl relative flex flex-col items-center justify-center z-10 border border-cyan-200">
      {/* 3D Stereoscopic Red/Cyan Glasses */}
      <div className="relative flex items-center justify-center my-1 z-20">
        <div className="flex gap-2">
          {/* Cyan Left Lens */}
          <div className="w-6 h-6 rounded-md bg-cyan-400 border-2 border-zinc-950 flex items-center justify-center shadow-inner">
            <div className="w-2 h-2 rounded-full bg-zinc-950" />
          </div>
          {/* Red Right Lens */}
          <div className="w-6 h-6 rounded-md bg-rose-500 border-2 border-zinc-950 flex items-center justify-center shadow-inner">
            <div className="w-2 h-2 rounded-full bg-zinc-950" />
          </div>
        </div>
        <div className="absolute w-3 h-1 bg-zinc-950 top-2" />
      </div>

      {/* Cute Smile */}
      <div className="w-3.5 h-1.5 border-b-2 border-zinc-950 rounded-full mt-1" />
    </div>

    {/* Electric Blue Hoodie with Wave logo */}
    <div className="w-36 h-24 bg-gradient-to-b from-[#2563EB] to-[#1D4ED8] rounded-t-[36px] relative -mt-5 flex flex-col items-center justify-center shadow-2xl border-t border-blue-400/50">
      <div className="flex gap-4 -mt-3">
        <div className="w-0.5 h-4 bg-blue-300 rounded-full" />
        <div className="w-0.5 h-4 bg-blue-300 rounded-full" />
      </div>
      <div className="mt-2 text-[11px] font-black tracking-widest text-white/95 italic font-mono uppercase">
        lstm 3d
      </div>
    </div>
  </div>
);

/**
 * 3D Illustrated Character 3: Podcast Audio Character (Charcoal Card)
 * Matching reference image: Acoustic foam background, metallic toaster head, boom mic, red hoodie.
 */
const VoiceCharacter = () => (
  <div className="relative w-48 h-56 flex flex-col items-center justify-end select-none group-hover:scale-105 transition-transform duration-500">
    {/* Boom Microphone on Right Side */}
    <div className="absolute top-6 right-2 flex flex-col items-center z-30">
      <div className="w-5 h-8 bg-zinc-900 border border-zinc-600 rounded-md shadow-lg flex flex-col items-center justify-center p-0.5">
        <div className="w-3.5 h-1 bg-zinc-500 rounded-full mb-0.5" />
        <div className="w-3.5 h-1 bg-zinc-500 rounded-full mb-0.5" />
        <div className="w-3.5 h-1 bg-zinc-500 rounded-full" />
      </div>
      {/* Mic Arm */}
      <div className="w-1 h-12 bg-zinc-700 -rotate-12 origin-top" />
    </div>

    {/* Metallic Box Head with Handle */}
    <div className="w-24 h-22 rounded-2xl bg-gradient-to-b from-zinc-300 via-zinc-400 to-zinc-500 shadow-2xl relative flex flex-col items-center justify-center z-10 border-2 border-zinc-200">
      {/* Leather Orange Handle */}
      <div className="absolute -top-3 w-16 h-4 border-t-3 border-l-3 border-r-3 border-amber-600 rounded-t-xl" />
      {/* Eyes & Smile */}
      <div className="flex gap-3 mb-1">
        <div className="w-2.5 h-2.5 rounded-full bg-zinc-950" />
        <div className="w-2.5 h-2.5 rounded-full bg-zinc-950" />
      </div>
      <div className="w-4 h-1.5 border-b-2 border-zinc-950 rounded-full" />
    </div>

    {/* Red Hoodie Body */}
    <div className="w-36 h-24 bg-gradient-to-b from-[#DC2626] to-[#991B1B] rounded-t-[36px] relative -mt-5 flex flex-col items-center justify-center shadow-2xl border-t border-rose-400/40">
      <div className="flex gap-4 -mt-3">
        <div className="w-0.5 h-4 bg-rose-300 rounded-full" />
        <div className="w-0.5 h-4 bg-rose-300 rounded-full" />
      </div>
      <div className="mt-2 text-[11px] font-black tracking-widest text-white/95 italic font-mono uppercase">
        voice mic
      </div>
    </div>
  </div>
);

export const BentoSection = ({ onOpenTracker, onNavigate }) => {
  return (
    <section id="demo-section" className="w-full bg-dots-dark py-20 px-6 sm:px-10 border-b border-zinc-900 text-white">
      <div className="max-w-7xl mx-auto">
        
        {/* Section Header (Exact Match to Reference Layout: Title + Pill Dropdown Action) */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-12 pb-6 border-b border-zinc-800/80">
          <div className="flex items-center gap-3">
            <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
              <span>SignFlow Core Systems</span>
              <span className="text-zinc-500 font-normal text-lg sm:text-xl">• Architecture Showcase</span>
            </h2>
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          </div>

          {/* Action CTA: Launch Live Tracker */}
          <div className="flex items-center gap-3">
            <div className="bg-white text-black px-4 py-1.5 rounded-full text-xs font-bold tracking-wide flex items-center gap-2 shadow-lg">
              <span>8 Active Classes</span>
              <span className="text-[10px]">▼</span>
            </div>
            <button
              onClick={onOpenTracker}
              className="px-5 py-2 rounded-full bg-gradient-to-r from-emerald-500 to-cyan-500 text-black text-xs font-black tracking-wider uppercase flex items-center gap-2 hover:opacity-90 transition-all shadow-lg shadow-emerald-500/20 active:scale-95"
            >
              <span>Launch Live Tracker</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* 3-COLUMN BENTO GRID (EXACT REFERENCE 3 CARDS LAYOUT) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">

          {/* ========================================================= */}
          {/* CARD 1: CORAL RED VERTICAL CARD ("WGMI Jam" • 3 ETH)      */}
          {/* THEME: Neural Vision & 258 Holistic Landmarks             */}
          {/* ========================================================= */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="bento-card-coral flex flex-col justify-between shadow-2xl relative group cursor-pointer"
            onClick={() => onNavigate ? onNavigate("architecture") : onOpenTracker()}
          >
            {/* Top Inner Section (Coral Red Container with 3D Character) */}
            <div className="p-6 relative flex flex-col flex-grow min-h-[380px] items-center justify-between overflow-hidden">
              
              {/* Card Header Tag */}
              <div className="w-full flex items-center justify-between mb-2 z-10">
                <span className="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider bg-black/40 text-white backdrop-blur-md border border-white/20 flex items-center gap-1.5">
                  <Eye className="w-3 h-3 text-white" />
                  <span>MediaPipe Holistic</span>
                </span>
                <span className="text-[10px] font-bold bg-white/20 px-2.5 py-0.5 rounded-full text-white uppercase tracking-wider">
                  258 Vector
                </span>
              </div>

              {/* 3D Character Illustration */}
              <div className="my-auto py-2">
                <VisionCharacter />
              </div>

              {/* Card Action Hint */}
              <div className="w-full flex items-center justify-between pt-2 text-white/90 text-xs font-bold border-t border-white/20">
                <span>Real-Time Optical Tracking</span>
                <span className="group-hover:translate-x-1 transition-transform flex items-center gap-1 text-[11px]">
                  Launch Vision →
                </span>
              </div>

            </div>

            {/* Bottom Dark Footer (Exact reference typography) */}
            <div className="bg-[#0B0B0C] p-6 pt-5 border-t border-zinc-800">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-black text-white tracking-tight">WGMI Jam</h3>
                  <p className="text-xs text-zinc-500 font-medium">Holistic Landmark Pipeline</p>
                </div>
                <div className="text-right">
                  <div className="text-xs font-extrabold text-white flex items-center gap-1">
                    <span className="text-rose-400 text-sm">◆</span>
                    <span>30 FPS • 258 Features</span>
                  </div>
                  <div className="text-[10px] text-zinc-500 font-semibold uppercase tracking-wider">Sub-15ms Extraction</div>
                </div>
              </div>
            </div>
          </motion.div>


          {/* ========================================================= */}
          {/* CARD 2: ELECTRIC BLUE VERTICAL CARD ("WGMI 3D" • 2.5 ETH) */}
          {/* THEME: 30-Frame Temporal LSTM Neural Classifier           */}
          {/* ========================================================= */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bento-card-blue flex flex-col justify-between shadow-2xl relative group cursor-pointer"
            onClick={() => onNavigate ? onNavigate("architecture") : onOpenTracker()}
          >
            {/* Top Inner Section (Electric Blue Container with 3D Character) */}
            <div className="p-6 relative flex flex-col flex-grow min-h-[380px] items-center justify-between overflow-hidden">
              
              {/* Card Header Tag */}
              <div className="w-full flex items-center justify-between mb-2 z-10">
                <span className="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider bg-black/40 text-white backdrop-blur-md border border-white/20 flex items-center gap-1.5">
                  <Cpu className="w-3 h-3 text-cyan-300" />
                  <span>Keras LSTM</span>
                </span>
                <span className="text-[10px] font-bold bg-white/20 px-2.5 py-0.5 rounded-full text-white uppercase tracking-wider">
                  30 Frames
                </span>
              </div>

              {/* 3D Character Illustration */}
              <div className="my-auto py-2">
                <NeuralCharacter />
              </div>

              {/* Card Action Hint */}
              <div className="w-full flex items-center justify-between pt-2 text-white/90 text-xs font-bold border-t border-white/20">
                <span>Temporal Motion Classification</span>
                <span className="group-hover:translate-x-1 transition-transform flex items-center gap-1 text-[11px]">
                  Open Architecture →
                </span>
              </div>

            </div>

            {/* Bottom Dark Footer (Exact reference typography) */}
            <div className="bg-[#0B0B0C] p-6 pt-5 border-t border-zinc-800">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-black text-white tracking-tight">WGMI 3D</h3>
                  <p className="text-xs text-zinc-500 font-medium">LSTM Temporal Classifier</p>
                </div>
                <div className="text-right">
                  <div className="text-xs font-extrabold text-white flex items-center gap-1">
                    <span className="text-blue-400 text-sm">◆</span>
                    <span>98.44% Accuracy</span>
                  </div>
                  <div className="text-[10px] text-zinc-500 font-semibold uppercase tracking-wider">0.041 Test Loss</div>
                </div>
              </div>
            </div>
          </motion.div>


          {/* ========================================================= */}
          {/* CARD 3: DARK CHARCOAL VERTICAL CARD ("WGMI Podcast")      */}
          {/* THEME: Voice Synthesis & Accessibility Gesture Studio     */}
          {/* ========================================================= */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bento-card-charcoal flex flex-col justify-between shadow-2xl relative group cursor-pointer"
            onClick={() => onNavigate ? onNavigate("matrix") : onOpenTracker()}
          >
            {/* Top Inner Section (Charcoal Container with Foam Background & Mic Character) */}
            <div className="p-6 relative flex flex-col flex-grow min-h-[380px] items-center justify-between overflow-hidden">
              
              {/* Card Header Tag */}
              <div className="w-full flex items-center justify-between mb-2 z-10">
                <span className="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider bg-black/60 text-white backdrop-blur-md border border-zinc-700 flex items-center gap-1.5">
                  <Volume2 className="w-3 h-3 text-emerald-400" />
                  <span>Speech Synthesis</span>
                </span>
                <span className="text-[10px] font-bold bg-zinc-800 px-2.5 py-0.5 rounded-full text-zinc-400 uppercase tracking-wider">
                  8 Classes
                </span>
              </div>

              {/* 3D Character Illustration */}
              <div className="my-auto py-2">
                <VoiceCharacter />
              </div>

              {/* Card Action Hint */}
              <div className="w-full flex items-center justify-between pt-2 text-white/90 text-xs font-bold border-t border-zinc-700">
                <span>pyttsx3 Voice Vocalization</span>
                <span className="group-hover:translate-x-1 transition-transform flex items-center gap-1 text-[11px]">
                  Explore Studio →
                </span>
              </div>

            </div>

            {/* Bottom Dark Footer (Exact reference typography) */}
            <div className="bg-[#0B0B0C] p-6 pt-5 border-t border-zinc-800">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-black text-white tracking-tight">WGMI Podcast</h3>
                  <p className="text-xs text-zinc-500 font-medium">Practice & Kinematics Studio</p>
                </div>
                <div className="text-right">
                  <div className="text-xs font-extrabold text-white flex items-center gap-1">
                    <span className="text-emerald-400 text-sm">◆</span>
                    <span>8 Core Signs</span>
                  </div>
                  <div className="text-[10px] text-zinc-500 font-semibold uppercase tracking-wider">Interactive Matrix</div>
                </div>
              </div>
            </div>
          </motion.div>

        </div>

      </div>
    </section>
  );
};
