import React from "react";
import { motion } from "framer-motion";

/**
 * 1. Neural Skeletal Hand (Mid-Left, w-24 h-24)
 * Iridescent rainbow border with dark obsidian core showing 
 * 21-keypoint MediaPipe hand skeletal mesh and interconnected glowing nodes.
 */
export const NeuralSkeletalHand = () => (
  <div className="w-full h-full relative rounded-2xl overflow-hidden flex items-center justify-center bg-black shadow-xl">
    {/* Rainbow Iridescent Shimmer Border */}
    <div 
      className="w-[72px] h-[72px] rounded-full relative flex items-center justify-center p-[2px] bg-gradient-to-tr from-pink-500 via-cyan-400 to-yellow-400 animate-spin" 
      style={{ animationDuration: "14s" }}
    >
      <div className="w-full h-full rounded-full bg-zinc-950 flex items-center justify-center relative overflow-hidden">
        {/* Subtle dot matrix grid */}
        <div className="absolute inset-0 opacity-40 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:5px_5px]" />
        
        {/* 21-Landmark Hand Skeletal Wireframe */}
        <svg className="w-11 h-11 relative z-10 text-cyan-400 drop-shadow-[0_0_8px_rgba(56,189,248,0.8)]" viewBox="0 0 100 100" fill="none">
          {/* Skeleton bones (connections) */}
          <path d="M50 85 L35 65 L25 50 L18 40" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M50 85 L42 55 L38 35 L35 20" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M50 85 L50 50 L50 30 L50 15" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M50 85 L58 55 L62 35 L65 22" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M50 85 L65 65 L75 52 L82 42" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M35 65 L42 55 L50 50 L58 55 L65 65" stroke="#ec4899" strokeWidth="2" strokeLinecap="round" strokeDasharray="2 2" />

          {/* Fingertips (glowing yellow nodes) */}
          <circle cx="18" cy="40" r="3.5" fill="#facc15" />
          <circle cx="35" cy="20" r="3.5" fill="#facc15" />
          <circle cx="50" cy="15" r="3.5" fill="#facc15" />
          <circle cx="65" cy="22" r="3.5" fill="#facc15" />
          <circle cx="82" cy="42" r="3.5" fill="#facc15" />

          {/* Intermediary knuckle joints (pink/cyan) */}
          <circle cx="25" cy="50" r="2.5" fill="#38bdf8" />
          <circle cx="38" cy="35" r="2.5" fill="#38bdf8" />
          <circle cx="50" cy="30" r="2.5" fill="#38bdf8" />
          <circle cx="62" cy="35" r="2.5" fill="#38bdf8" />
          <circle cx="75" cy="52" r="2.5" fill="#38bdf8" />

          {/* Wrist root node (golden pulse) */}
          <circle cx="50" cy="85" r="4.5" fill="#f43f5e" />
        </svg>
      </div>
    </div>
  </div>
);

/**
 * 2. Hand Landmarks Squircle (Top-Left, w-16 h-16)
 * Golden/amber glossy 3D squircle with an illuminated hand tracking pose.
 */
export const HandLandmarksSquircle = () => (
  <div className="w-full h-full relative rounded-2xl flex items-center justify-center bg-gradient-to-b from-zinc-800 via-zinc-900 to-black p-2.5 border border-amber-500/30 shadow-lg group">
    {/* Ambient golden glow */}
    <div className="absolute inset-0 rounded-2xl bg-amber-500/10 blur-sm pointer-events-none" />
    <div className="relative flex flex-col items-center justify-center w-full h-full">
      {/* 3D Golden Hand Landmark Glyph */}
      <svg className="w-8 h-8 text-amber-400 drop-shadow-[0_2px_10px_rgba(245,158,11,0.6)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0" />
        <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2" />
        <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8" />
        <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.83l1.76 1.77" />
        {/* Optical Tracking crosshair node on palm */}
        <circle cx="13" cy="14" r="1.5" fill="#fde047" stroke="#b45309" strokeWidth="0.8" />
      </svg>
    </div>
  </div>
);

/**
 * 3. Sign Alphabet Cubes (Bottom-Left, w-20 h-20)
 * 3D tactile cubes representing the letters S - I - G - N with tactile elevation.
 */
export const FingerspellingCubes = () => (
  <div className="w-full h-full relative rounded-2xl flex items-center justify-center bg-gradient-to-b from-zinc-100 to-zinc-300 p-2 shadow-xl border border-white">
    <div className="grid grid-cols-2 gap-1.5 p-1.5 bg-zinc-200/90 rounded-xl shadow-inner">
      <div className="w-6 h-6 bg-white rounded-md shadow-md flex items-center justify-center text-[10px] font-black text-amber-500 hover:scale-105 transition-transform">
        S
      </div>
      <div className="w-6 h-6 bg-white rounded-md shadow-md flex items-center justify-center text-[10px] font-black text-cyan-600 hover:scale-105 transition-transform">
        I
      </div>
      <div className="w-6 h-6 bg-white rounded-md shadow-md flex items-center justify-center text-[10px] font-black text-purple-600 hover:scale-105 transition-transform">
        G
      </div>
      <div className="w-6 h-6 bg-white rounded-md shadow-md flex items-center justify-center text-[10px] font-black text-emerald-600 hover:scale-105 transition-transform">
        N
      </div>
    </div>
  </div>
);

/**
 * 4. Speech Voice Wave Squircle (Top-Right, w-20 h-20)
 * Vibrant purple squircle with 3D speech bubble and vocal audio waveform (TTS).
 */
export const SpeechWaveSquircle = () => (
  <div className="w-full h-full relative rounded-2xl flex items-center justify-center bg-gradient-to-tr from-purple-600 via-indigo-600 to-purple-400 p-2 shadow-xl border border-purple-300/40">
    <div className="relative flex flex-col items-center">
      {/* 3D Speech Bubble with Face */}
      <div className="w-11 h-11 bg-white/95 rounded-2xl relative flex flex-col items-center justify-center shadow-md p-1">
        {/* Antenna / Broadcast Beacon */}
        <div className="absolute -top-3 w-1 h-3 bg-pink-400 rounded-full">
          <div className="w-2 h-2 bg-pink-500 rounded-full -top-1 -left-0.5 absolute animate-ping" style={{ animationDuration: "3s" }} />
          <div className="w-2 h-2 bg-pink-500 rounded-full -top-1 -left-0.5 absolute" />
        </div>
        
        {/* Sound Wave Bars inside bubble */}
        <div className="flex items-center gap-1 mb-1">
          <span className="w-1 h-3 bg-indigo-600 rounded-full animate-pulse" />
          <span className="w-1 h-4.5 bg-purple-600 rounded-full" />
          <span className="w-1 h-2.5 bg-pink-500 rounded-full animate-pulse" />
          <span className="w-1 h-4 bg-indigo-600 rounded-full" />
        </div>

        {/* Happy Smile */}
        <div className="w-3.5 h-1 border-b-2 border-zinc-900 rounded-full" />
      </div>
    </div>
  </div>
);

/**
 * 5. Love Gesture Squircle (Mid-Right, w-28 h-28)
 * Neon lime squircle featuring the 3D ASL "I Love You" (🤟) sign with cute face.
 */
export const LoveGestureSquircle = () => (
  <div className="w-full h-full relative rounded-2xl flex items-center justify-center bg-gradient-to-tr from-[#A3E635] via-[#BEF264] to-[#D9F99D] p-2 shadow-2xl border border-lime-200">
    <div className="relative flex flex-col items-center justify-center">
      {/* 3D Emerald Container */}
      <div className="w-14 h-14 bg-emerald-950/90 rounded-2xl flex flex-col items-center justify-center shadow-inner relative overflow-hidden p-1.5 border border-emerald-800">
        {/* 3D ASL "I Love You" (🤟) Hand Sign Vector */}
        <svg className="w-8 h-8 text-lime-300 drop-shadow-[0_2px_8px_rgba(190,242,100,0.7)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          {/* Thumb extended */}
          <path d="M4 11a2 2 0 0 1 2-2h1" />
          {/* Index extended */}
          <path d="M7 9V3a2 2 0 0 1 4 0v6" />
          {/* Middle & Ring folded */}
          <path d="M11 9a2 2 0 0 1 2 2v1" />
          <path d="M13 11a2 2 0 0 1 2 2v1" />
          {/* Pinky extended */}
          <path d="M17 12V6a2 2 0 0 1 4 0v7a6 6 0 0 1-6 6H9a5 5 0 0 1-5-5v-1" />
        </svg>

        {/* Playful Friendly Eyes matching reference aesthetic */}
        <div className="flex gap-2 mt-0.5">
          <div className="w-1.5 h-1.5 bg-white rounded-full shadow-sm" />
          <div className="w-1.5 h-1.5 bg-white rounded-full shadow-sm" />
        </div>
      </div>
    </div>
  </div>
);

/**
 * Floating squircle animation wrapper with Framer Motion physics
 */
export const FloatingSquircle = ({ children, className = "", delay = 0, floatDuration = 5, yOffset = 12 }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ 
        opacity: 1, 
        scale: 1,
        y: [0, -yOffset, 0] 
      }}
      transition={{
        opacity: { duration: 0.6, delay },
        scale: { duration: 0.6, delay },
        y: {
          duration: floatDuration,
          repeat: Infinity,
          ease: "easeInOut",
          delay: delay * 0.5
        }
      }}
      className={`squircle-3d select-none cursor-pointer ${className}`}
    >
      {children}
    </motion.div>
  );
};
