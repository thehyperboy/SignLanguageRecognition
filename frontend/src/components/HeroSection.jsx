import React from "react";
import { motion } from "framer-motion";
import { 
  FloatingSquircle, 
  NeuralSkeletalHand, 
  HandLandmarksSquircle, 
  FingerspellingCubes, 
  SpeechWaveSquircle, 
  LoveGestureSquircle 
} from "./FloatingSquircle";
import { ArrowDown, Sparkles } from "lucide-react";

export const HeroSection = ({ onScrollToDemo, onOpenTracker, isCameraActive, onToggleCamera }) => {
  return (
    <section className="relative w-full bg-dots-light py-20 md:py-28 overflow-hidden border-b border-zinc-200">
      
      {/* Floating 3D Squircles Orbiting Title (Sign Language Recognition Themed) */}

      {/* Top Left: 3D Hand Landmark Pose (Golden Amber Squircle) */}
      <div className="absolute left-[12%] top-[10%] hidden lg:block z-10" title="MediaPipe Optical Landmark Tracking">
        <FloatingSquircle className="w-16 h-16" delay={0.2} floatDuration={5} yOffset={10}>
          <HandLandmarksSquircle />
        </FloatingSquircle>
      </div>

      {/* Mid Left: Iridescent Holographic Skeletal Hand Mesh (21 Keypoints) */}
      <div className="absolute left-[5%] top-[34%] hidden md:block z-10" title="21-Keypoint Hand Skeletal Mesh & 258 Holistic Features">
        <FloatingSquircle className="w-24 h-24" delay={0.4} floatDuration={6} yOffset={14}>
          <NeuralSkeletalHand />
        </FloatingSquircle>
      </div>

      {/* Bottom Left: 3D Sign Letter Cubes (S - I - G - N) */}
      <div className="absolute left-[14%] bottom-[8%] hidden lg:block z-10" title="Sign Alphabet & Fingerspelling Cubes">
        <FloatingSquircle className="w-20 h-20" delay={0.6} floatDuration={4.5} yOffset={12}>
          <FingerspellingCubes />
        </FloatingSquircle>
      </div>

      {/* Top Right: Speech Wave & Vocal Synthesis Squircle */}
      <div className="absolute right-[12%] top-[12%] hidden md:block z-10" title="Text-to-Speech Vocal Audio Synthesis">
        <FloatingSquircle className="w-20 h-20" delay={0.3} floatDuration={5.5} yOffset={12}>
          <SpeechWaveSquircle />
        </FloatingSquircle>
      </div>

      {/* Mid Right: 3D ASL 'I Love You' Gesture Character (Neon Lime Squircle) */}
      <div className="absolute right-[6%] top-[40%] hidden md:block z-10" title="ASL 'I Love You' Gesture">
        <FloatingSquircle className="w-28 h-28" delay={0.5} floatDuration={6.5} yOffset={16}>
          <LoveGestureSquircle />
        </FloatingSquircle>
      </div>

      {/* Hero Center Content */}
      <div className="max-w-4xl mx-auto px-6 text-center relative z-20">
        
        {/* Eyebrow badge */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-zinc-200/80 border border-zinc-300 text-zinc-800 text-[11px] font-bold tracking-wide uppercase mb-6 shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 text-zinc-900" />
          <span>Bi-Directional Neural Accessibility</span>
        </motion.div>

        {/* Main Title: Sign Language Recognition */}
        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-4xl sm:text-6xl md:text-7xl font-black text-zinc-950 tracking-tight leading-[1.08] mb-6"
        >
          Sign Language <br className="hidden sm:inline" />
          Recognition
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="max-w-xl mx-auto text-sm sm:text-base text-zinc-600 font-medium leading-relaxed mb-8"
        >
          Real-time AI gesture translation powered by 258 MediaPipe holistic landmarks & 30-frame temporal LSTM neural prediction for bi-directional accessibility.
        </motion.p>

        {/* Action Button (Exact Reference Match: Pill Black Button) */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <button
            onClick={onOpenTracker || onScrollToDemo}
            className="px-8 py-3.5 rounded-full bg-black text-white text-xs font-bold tracking-wider uppercase hover:bg-zinc-800 transition-all shadow-xl shadow-zinc-900/10 active:scale-95 flex items-center gap-2"
          >
            <span>Try Live Recognition</span>
            <span className="text-sm">→</span>
          </button>
        </motion.div>

      </div>

    </section>
  );
};
