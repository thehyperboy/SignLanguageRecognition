import React from "react";
import { motion } from "framer-motion";
import { Camera, Radio, Sparkles } from "lucide-react";

export const Navbar = ({ 
  activeTab, 
  setActiveTab, 
  isCameraActive, 
  onToggleCamera,
  connectionStatus = "connected"
}) => {
  const navItems = [
    { id: "home", label: "Home" },
    { id: "tracker", label: "Live Tracker" },
    { id: "matrix", label: "Gesture Library" },
    { id: "architecture", label: "Neural Architecture" },
    { id: "accessibility", label: "Accessibility" }
  ];

  return (
    <header className="w-full bg-[#F8F9FA]/85 backdrop-blur-xl border-b border-zinc-200/80 sticky top-0 z-50 transition-all shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)]">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        
        {/* Brand Logo with 3D Perspective Tilt and Holographic Motion Graphic */}
        <motion.div 
          onClick={() => setActiveTab("home")}
          className="flex items-center gap-3.5 cursor-pointer group select-none"
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.97 }}
          style={{ perspective: 1000 }}
        >
          {/* 3D Holographic Cube Badge */}
          <motion.div 
            className="w-11 h-11 rounded-2xl bg-black p-1 shadow-[0_8px_16px_rgba(0,0,0,0.25)] border border-zinc-700/60 flex items-center justify-center relative overflow-hidden"
            whileHover={{ 
              rotateY: 18, 
              rotateX: -10,
              boxShadow: "0 12px 24px rgba(0,0,0,0.35)"
            }}
            transition={{ type: "spring", stiffness: 350, damping: 20 }}
          >
            {/* Iridescent Spinning Shimmer Ring */}
            <motion.div 
              className="absolute inset-0 bg-gradient-to-tr from-pink-500 via-cyan-400 to-yellow-300 opacity-90"
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
            />

            {/* Glossy Black Core with 3D Hand Vector */}
            <div className="w-full h-full rounded-xl bg-zinc-950/90 relative z-10 flex items-center justify-center p-1.5 backdrop-blur-sm shadow-inner">
              <svg className="w-5 h-5 text-cyan-300 drop-shadow-[0_0_8px_rgba(56,189,248,0.8)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0" />
                <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2" />
                <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8" />
                <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.83l1.76 1.77" />
              </svg>
            </div>
          </motion.div>

          {/* Typography */}
          <div>
            <div className="text-base font-black tracking-tight text-zinc-950 flex items-center gap-1.5">
              <span>SignFlow</span>
              <span className="text-[10px] font-black uppercase tracking-wider bg-black text-white px-1.5 py-0.5 rounded-full shadow-sm">AI</span>
            </div>
            <div className="text-[11px] font-medium text-zinc-500 flex items-center gap-1">
              <span>Neural Sign Vision</span>
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
            </div>
          </div>
        </motion.div>

        {/* Center Nav Links with Smooth Framer-Motion 3D Spring Pill Slider */}
        <nav className="hidden md:flex items-center gap-1 bg-zinc-200/60 backdrop-blur-md p-1.5 rounded-full border border-zinc-300/80 shadow-[inset_0_2px_4px_rgba(0,0,0,0.06)] relative">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <motion.button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                whileHover={{ y: -1 }}
                whileTap={{ scale: 0.96 }}
                className={`relative px-4 py-1.5 text-xs font-bold rounded-full transition-colors z-10 select-none ${
                  isActive 
                    ? "text-black" 
                    : "text-zinc-600 hover:text-black"
                }`}
              >
                {/* 3D Motion Graphic Floating Active Pill */}
                {isActive && (
                  <motion.div
                    layoutId="navbarActiveIndicator"
                    transition={{ 
                      type: "spring", 
                      stiffness: 420, 
                      damping: 32 
                    }}
                    className="absolute inset-0 bg-white rounded-full shadow-[0_3px_10px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.06)] -z-10 border border-zinc-200/60"
                  />
                )}
                <span>{item.label}</span>
              </motion.button>
            );
          })}
        </nav>

        {/* Right 3D Motion Graphic CTA Button ("Launch Live Tracker") */}
        <div className="flex items-center gap-3">
          <motion.button
            onClick={() => {
              if (activeTab !== "tracker") {
                setActiveTab("tracker");
                if (!isCameraActive) onToggleCamera();
              } else {
                onToggleCamera();
              }
            }}
            whileHover={{ 
              scale: 1.05, 
              y: -2,
              boxShadow: isCameraActive 
                ? "0 10px 25px -4px rgba(225,29,72,0.4)" 
                : "0 10px 25px -4px rgba(0,0,0,0.35)"
            }}
            whileTap={{ scale: 0.95, y: 0 }}
            className={`relative group overflow-hidden flex items-center gap-2.5 px-6 py-2.5 rounded-full text-xs font-black tracking-wide transition-all shadow-md ${
              isCameraActive 
                ? "bg-zinc-950 text-white border border-rose-500/60" 
                : "bg-black text-white hover:bg-zinc-900 shadow-zinc-900/20"
            }`}
          >
            {/* Shimmer Light Sweep on Hover */}
            <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

            {/* Glowing Live Beacon Indicator */}
            <span className="relative flex h-2 w-2">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                isCameraActive ? "bg-rose-400" : "bg-emerald-400"
              }`} />
              <span className={`relative inline-flex rounded-full h-2 w-2 ${
                isCameraActive ? "bg-rose-500" : "bg-emerald-500"
              }`} />
            </span>

            <Camera className="w-3.5 h-3.5" />
            <span>{isCameraActive ? "Camera Active" : "Launch Tracker"}</span>
          </motion.button>
        </div>

      </div>
    </header>
  );
};
