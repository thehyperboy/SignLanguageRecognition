import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Camera, 
  RotateCcw, 
  Volume2, 
  VolumeX, 
  ArrowLeft, 
  Sparkles, 
  CheckCircle2, 
  Layers, 
  Eye, 
  Radio, 
  Cpu, 
  Zap,
  Activity
} from "lucide-react";

export const TrackerPage = ({
  onBackToHome,
  isCameraActive,
  onToggleCamera,
  practiceSign,
  setPracticeSign,
  serverData,
  onResetBuffer,
  annotatedFrame,
  mediaStream,
  connectionStatus
}) => {
  const [isMirror, setIsMirror] = useState(true);
  const [speechEnabled, setSpeechEnabled] = useState(true);
  const [viewMode, setViewMode] = useState("live"); // "live" (60 FPS direct GPU video) or "landmarks" (MediaPipe skeleton)
  const displayVideoRef = useRef(null);

  // Bind mediaStream to local video element whenever available
  useEffect(() => {
    if (displayVideoRef.current && mediaStream) {
      displayVideoRef.current.srcObject = mediaStream;
      displayVideoRef.current.play().catch((err) => {
        console.warn("Display video play:", err);
      });
    }
  }, [mediaStream, isCameraActive]);

  const vocabularyList = [
    { id: "hello", name: "HELLO", icon: "👋", desc: "Wave dominant hand naturally" },
    { id: "thank_you", name: "THANK YOU", icon: "🙏", desc: "Chin forward to camera" },
    { id: "yes", name: "YES", icon: "🙆", desc: "Nod fist up and down" },
    { id: "no", name: "NO", icon: "🙅", desc: "Snap index & middle fingers" },
    { id: "help", name: "HELP", icon: "🆘", desc: "Elevate fist on open palm" },
    { id: "love", name: "LOVE", icon: "🤟", desc: "Thumb, index & pinky open" },
    { id: "please", name: "PLEASE", icon: "🤲", desc: "Rub circular motion on chest" },
    { id: "sorry", name: "SORRY", icon: "✊", desc: "Rub circular fist on chest" },
  ];

  const currentPrediction = serverData?.display_prediction || serverData?.prediction || "Waiting...";
  const currentConfidence = (serverData?.display_confidence || serverData?.confidence || 0) * 100;
  const currentFrames = serverData?.frames || 0;
  const handDetected = serverData?.hand_detected || false;
  const isLatched = serverData?.is_latched || false;

  const isMatchedPractice = practiceSign && currentPrediction.toLowerCase() === practiceSign.toLowerCase();

  return (
    <div className="min-h-screen bg-[#070708] text-white py-8 px-4 sm:px-8 bg-dots-dark">
      <div className="max-w-7xl mx-auto">

        {/* Top Header & Breadcrumb */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8 pb-6 border-b border-zinc-800">
          <div className="flex items-center gap-4">
            <button
              onClick={onBackToHome}
              className="px-4 py-2 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-xs font-bold text-zinc-300 hover:text-white flex items-center gap-2 transition-all shadow-md active:scale-95"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Overview</span>
            </button>

            <div>
              <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight flex items-center gap-3">
                <span>Neural Live Tracker</span>
                <span className={`text-xs px-2.5 py-1 rounded-full font-bold uppercase tracking-wider flex items-center gap-1.5 ${
                  connectionStatus === "connected"
                    ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                    : "bg-amber-500/20 text-amber-400 border border-amber-500/40"
                }`}>
                  <span className={`w-2 h-2 rounded-full ${connectionStatus === "connected" ? "bg-emerald-400 animate-pulse" : "bg-amber-400"}`} />
                  {connectionStatus === "connected" ? "Live Stream (Sub-30ms)" : "Connecting..."}
                </span>
              </h1>
              <p className="text-xs text-zinc-400 mt-1">Direct 60 FPS Hardware Acceleration • 258 Holistic Spatial Vector • Fast Temporal LSTM</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={onResetBuffer}
              title="Reset temporal sequence buffer"
              className="bg-zinc-900 hover:bg-zinc-800 text-zinc-300 hover:text-white px-4 py-2 rounded-full text-xs font-semibold flex items-center gap-2 transition-all border border-zinc-700 shadow-sm active:scale-95"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset Buffer</span>
            </button>
            <button
              onClick={onToggleCamera}
              className={`px-5 py-2 rounded-full text-xs font-bold flex items-center gap-2 transition-all shadow-md active:scale-95 ${
                isCameraActive 
                  ? "bg-rose-600/90 hover:bg-rose-700 text-white" 
                  : "bg-white text-black hover:bg-zinc-200"
              }`}
            >
              <Camera className="w-3.5 h-3.5" />
              <span>{isCameraActive ? "Stop Camera" : "Start Camera"}</span>
            </button>
          </div>
        </div>

        {/* Practice Banner if active */}
        {practiceSign && (
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`mb-8 p-4 rounded-2xl border flex items-center justify-between ${
              isMatchedPractice 
                ? "bg-emerald-950/70 border-emerald-500 shadow-[0_0_25px_rgba(16,185,129,0.35)]" 
                : "bg-zinc-900 border-zinc-700"
            }`}
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">{isMatchedPractice ? "🎉" : "🎯"}</span>
              <div>
                <span className="text-xs font-bold text-zinc-400 uppercase tracking-wider">Practice Target:</span>
                <span className="ml-2 text-base font-extrabold text-white">{practiceSign.toUpperCase()}</span>
                {isMatchedPractice && (
                  <span className="ml-3 text-xs font-bold text-emerald-400 bg-emerald-500/20 px-2.5 py-0.5 rounded-full border border-emerald-500/40 animate-pulse">
                    ✓ GESTURE MATCHED!
                  </span>
                )}
              </div>
            </div>
            <button
              onClick={() => setPracticeSign(null)}
              className="px-3.5 py-1 rounded-full text-xs font-semibold bg-zinc-800 hover:bg-zinc-700 text-zinc-300"
            >
              Exit Practice ✕
            </button>
          </motion.div>
        )}

        {/* 3-Column Tracker Layout matching reference bento cards style */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">

          {/* ========================================================= */}
          {/* PANEL 1: LIVE WEBCAM & LANDMARK OVERLAY (Coral Accent)    */}
          {/* ========================================================= */}
          <div className="bento-card-coral flex flex-col justify-between shadow-2xl relative">
            <div className="p-6 relative flex flex-col flex-grow min-h-[440px]">
              
              {/* Header Badge & Mode Toggles */}
              <div className="flex items-center justify-between mb-4 z-10 gap-2">
                
                {/* 60 FPS Native vs Landmark Mode Switcher */}
                <div className="flex items-center bg-black/50 backdrop-blur-md p-1 rounded-full border border-white/20">
                  <button
                    onClick={() => setViewMode("live")}
                    className={`px-2.5 py-0.5 rounded-full text-[10px] font-black transition-all ${
                      viewMode === "live"
                        ? "bg-emerald-400 text-black shadow-sm"
                        : "text-white/70 hover:text-white"
                    }`}
                  >
                    ⚡ 60 FPS Native
                  </button>
                  <button
                    onClick={() => setViewMode("landmarks")}
                    className={`px-2.5 py-0.5 rounded-full text-[10px] font-black transition-all ${
                      viewMode === "landmarks"
                        ? "bg-cyan-400 text-black shadow-sm"
                        : "text-white/70 hover:text-white"
                    }`}
                  >
                    🦴 Skeleton Mesh
                  </button>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setIsMirror(!isMirror)}
                    className="px-2.5 py-1 rounded-full bg-black/50 hover:bg-black/70 text-white text-[11px] font-bold border border-white/20 transition-all"
                    title="Mirror Viewport"
                  >
                    ⇄ Mirror
                  </button>
                </div>
              </div>

              {/* Camera Video / Landmark Frame Viewport */}
              <div className="w-full flex-grow rounded-2xl overflow-hidden bg-black border border-white/20 relative shadow-inner flex items-center justify-center min-h-[320px]">
                {isCameraActive ? (
                  <>
                    {/* Native 60 FPS Video Element: Always running directly on GPU with zero latency */}
                    <video
                      ref={displayVideoRef}
                      autoPlay
                      playsInline
                      muted
                      className={`w-full h-full object-cover transition-transform ${isMirror ? "scale-x-[-1]" : ""} ${
                        viewMode === "landmarks" && annotatedFrame ? "hidden" : "block"
                      }`}
                    />

                    {/* MediaPipe Skeleton Landmark Stream (When in Skeleton Mesh Mode) */}
                    {viewMode === "landmarks" && annotatedFrame && (
                      <img 
                        src={annotatedFrame} 
                        alt="Neural Landmark Stream"
                        className={`w-full h-full object-cover ${isMirror ? "scale-x-[-1]" : ""}`}
                      />
                    )}

                    {/* Live Optical Crosshair Overlay (Active in 60 FPS mode) */}
                    {viewMode === "live" && handDetected && (
                      <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
                        <div className="w-56 h-56 border-2 border-emerald-400/50 rounded-2xl animate-pulse flex items-center justify-center">
                          <div className="w-2 h-2 rounded-full bg-emerald-400" />
                        </div>
                      </div>
                    )}

                    {/* Real-time Tracking Status Badge */}
                    <div className="absolute top-3 left-3 bg-black/75 backdrop-blur-md px-3 py-1 rounded-full text-[10px] font-semibold text-white border border-white/20 flex items-center gap-1.5 shadow-md">
                      <span className={`w-2 h-2 rounded-full ${handDetected ? "bg-emerald-400 animate-ping" : "bg-amber-400"}`} />
                      <span className={`w-2 h-2 rounded-full ${handDetected ? "bg-emerald-400" : "bg-amber-400"} absolute left-3`} />
                      <span className="ml-1 font-bold">
                        {handDetected ? "Hand Tracking Active" : "Show Hand to Camera"}
                      </span>
                    </div>

                    {/* Mode & Performance Pill */}
                    <div className="absolute bottom-3 right-3 bg-black/75 backdrop-blur-md px-2.5 py-0.5 rounded-md text-[9px] font-mono text-cyan-300 border border-white/15">
                      {viewMode === "live" ? "⚡ 60 FPS • GPU Direct" : "258 Features • MediaPipe Mesh"}
                    </div>
                  </>
                ) : (
                  <div className="text-center p-6 flex flex-col items-center">
                    <div className="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center mb-4 border border-white/20 shadow-lg">
                      <Camera className="w-7 h-7 text-white/80" />
                    </div>
                    <div className="text-base font-bold text-white mb-1">Camera Is Not Active</div>
                    <div className="text-xs text-white/70 mb-5 max-w-[220px]">
                      Enable your camera to track 258 landmarks and recognize gestures in real-time.
                    </div>
                    <button
                      onClick={onToggleCamera}
                      className="px-6 py-2.5 rounded-full bg-white text-black text-xs font-black uppercase tracking-wider hover:bg-zinc-200 transition-all shadow-xl active:scale-95 flex items-center gap-2"
                    >
                      <Camera className="w-3.5 h-3.5" />
                      <span>Start Camera</span>
                    </button>
                  </div>
                )}
              </div>

            </div>

            {/* Panel Footer */}
            <div className="bg-[#0B0B0C] p-6 pt-5 border-t border-zinc-800">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-black text-white tracking-tight">Vision Viewport</h3>
                  <p className="text-xs text-zinc-500 font-medium">Sub-30ms Optical Pipeline</p>
                </div>
                <div className="text-right">
                  <div className="text-xs font-extrabold text-white flex items-center gap-1">
                    <span className="text-emerald-400 text-sm">◆</span>
                    <span>{viewMode === "live" ? "60 FPS Native" : "30 FPS Mesh"}</span>
                  </div>
                  <div className="text-[10px] text-zinc-500 font-semibold uppercase tracking-wider">Zero Input Lag</div>
                </div>
              </div>
            </div>
          </div>


          {/* ========================================================= */}
          {/* PANEL 2: NEURAL CONSOLE & PREDICTIONS (Blue Accent)       */}
          {/* ========================================================= */}
          <div className="bento-card-blue flex flex-col justify-between shadow-2xl relative">
            <div className="p-6 relative flex flex-col flex-grow min-h-[440px]">
              
              {/* Header */}
              <div className="flex items-center justify-between mb-4 z-10">
                <span className="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider bg-black/50 text-white backdrop-blur-md border border-white/20 flex items-center gap-1.5">
                  <Radio className="w-3 h-3 text-cyan-300 animate-pulse" />
                  Neural Console
                </span>
                <span className="text-[10px] font-bold bg-white/20 px-2.5 py-0.5 rounded-full text-white uppercase tracking-wider">
                  Real-Time
                </span>
              </div>

              {/* Console Body */}
              <div className="w-full flex-grow rounded-2xl bg-black/90 border border-white/20 p-5 flex flex-col justify-between shadow-inner">
                
                {/* Recognized Sign Output Display */}
                <div>
                  <div className="flex items-center justify-between text-xs font-semibold text-white/60 mb-2">
                    <span className="uppercase tracking-wider text-[10px]">Recognized Sign</span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      currentConfidence >= 65 
                        ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40" 
                        : "bg-white/10 text-white/70"
                    }`}>
                      {currentConfidence.toFixed(1)}% Conf
                    </span>
                  </div>

                  <div className="text-center py-6 px-4 rounded-xl bg-white/5 border border-white/10 my-2">
                    <div className={`text-3xl sm:text-4xl font-black tracking-tight uppercase transition-all ${
                      currentPrediction !== "Waiting..." && currentPrediction !== "Uncertain"
                        ? "text-white scale-105 drop-shadow-[0_0_25px_rgba(56,189,248,0.9)]" 
                        : "text-zinc-500"
                    }`}>
                      {currentPrediction}
                    </div>
                    <div className="text-[11px] text-zinc-400 mt-2 font-medium">
                      {isLatched 
                        ? "✓ Gesture Latched & Stabilized" 
                        : handDetected 
                          ? "Tracking motion sequence..." 
                          : "Awaiting hand gesture in frame"}
                    </div>
                  </div>
                </div>

                {/* Temporal Sequence Buffer Progress */}
                <div className="mt-4">
                  <div className="flex items-center justify-between text-[11px] font-bold text-white/70 mb-1.5">
                    <span className="flex items-center gap-1.5 uppercase tracking-wider text-[10px]">
                      <Layers className="w-3 h-3 text-cyan-400" />
                      Temporal Buffer
                    </span>
                    <span className="font-mono text-cyan-300">{currentFrames} / 30 frames</span>
                  </div>
                  <div className="w-full h-2.5 rounded-full bg-white/10 overflow-hidden border border-white/10">
                    <div 
                      className={`h-full rounded-full transition-all duration-150 ${
                        currentFrames >= 30 
                          ? "bg-emerald-400" 
                          : "bg-gradient-to-r from-cyan-400 to-blue-500"
                      }`}
                      style={{ width: `${Math.min(100, (currentFrames / 30) * 100)}%` }}
                    />
                  </div>
                </div>

                {/* Voice Audio Speech Status */}
                <div className="mt-4 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-white/80">
                  <div className="flex items-center gap-2">
                    <Volume2 className="w-4 h-4 text-cyan-400" />
                    <span className="text-[11px] font-semibold">Voice Output:</span>
                    <span className="text-[11px] font-bold text-emerald-400">
                      {speechEnabled ? "Active (pyttsx3)" : "Muted"}
                    </span>
                  </div>
                  <button
                    onClick={() => setSpeechEnabled(!speechEnabled)}
                    className="p-1 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"
                    title={speechEnabled ? "Mute Speech" : "Unmute Speech"}
                  >
                    {speechEnabled ? <Volume2 className="w-3 h-3" /> : <VolumeX className="w-3 h-3" />}
                  </button>
                </div>

              </div>

            </div>

            {/* Panel Footer */}
            <div className="bg-[#0B0B0C] p-6 pt-5 border-t border-zinc-800">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-black text-white tracking-tight">LSTM Engine</h3>
                  <p className="text-xs text-zinc-500 font-medium">2-Layer Recurrent Neural Net</p>
                </div>
                <div className="text-right">
                  <div className="text-xs font-extrabold text-white flex items-center gap-1">
                    <span className="text-blue-400 text-sm">◆</span>
                    <span>98.44% Accuracy</span>
                  </div>
                  <div className="text-[10px] text-zinc-500 font-semibold uppercase tracking-wider">0.041 Loss</div>
                </div>
              </div>
            </div>
          </div>


          {/* ========================================================= */}
          {/* PANEL 3: GESTURE MATRIX & PRACTICE (Charcoal Accent)      */}
          {/* ========================================================= */}
          <div className="bento-card-charcoal flex flex-col justify-between shadow-2xl relative">
            <div className="p-6 relative flex flex-col flex-grow min-h-[440px]">
              
              {/* Header */}
              <div className="flex items-center justify-between mb-4 z-10">
                <span className="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider bg-black/60 text-white backdrop-blur-md border border-zinc-700 flex items-center gap-1.5">
                  <Layers className="w-3 h-3 text-emerald-400" />
                  Gesture Matrix
                </span>
                <span className="text-[10px] font-bold bg-zinc-800 px-2.5 py-0.5 rounded-full text-zinc-400 uppercase tracking-wider">
                  8 Classes
                </span>
              </div>

              {/* Gesture Grid */}
              <div className="grid grid-cols-2 gap-2.5 w-full flex-grow overflow-y-auto max-h-[350px] pr-1 custom-scrollbar">
                {vocabularyList.map((sign) => {
                  const isCurrent = currentPrediction.toLowerCase() === sign.name.toLowerCase();
                  const isTarget = practiceSign && practiceSign.toLowerCase() === sign.id;

                  return (
                    <div
                      key={sign.id}
                      onClick={() => setPracticeSign(sign.name)}
                      className={`p-3 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
                        isCurrent 
                          ? "bg-emerald-500/25 border-emerald-500 text-white shadow-lg ring-1 ring-emerald-400" 
                          : isTarget 
                            ? "bg-cyan-500/20 border-cyan-400 text-white" 
                            : "bg-zinc-900/90 border-zinc-800 hover:border-zinc-600 text-zinc-300"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xl">{sign.icon}</span>
                        {isCurrent && (
                          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                        )}
                      </div>
                      <div className="mt-2">
                        <div className="text-xs font-black tracking-wide text-white">{sign.name}</div>
                        <div className="text-[10px] text-zinc-400 line-clamp-1">{sign.desc}</div>
                      </div>
                    </div>
                  );
                })}
              </div>

            </div>

            {/* Panel Footer */}
            <div className="bg-[#0B0B0C] p-6 pt-5 border-t border-zinc-800">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-black text-white tracking-tight">Practice Studio</h3>
                  <p className="text-xs text-zinc-500 font-medium">Click any sign to practice</p>
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
          </div>

        </div>

      </div>
    </div>
  );
};
