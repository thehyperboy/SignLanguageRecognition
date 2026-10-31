import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Camera, Sparkles, LogIn, UserPlus, LogOut, ChevronDown, CheckCircle2, Menu, X, Home, BookOpen, Brain, Accessibility } from "lucide-react";

export const Navbar = ({ 
  activeTab, 
  setActiveTab, 
  isCameraActive, 
  onToggleCamera,
  connectionStatus = "connected",
  user = null,
  onLogout = null,
  onOpenAuth = null
}) => {
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const userMenuRef = useRef(null);

  const navItems = [
    { id: "home", label: "Home", icon: Home },
    { id: "tracker", label: "Live Tracker", icon: Camera },
    { id: "matrix", label: "Gesture Library", icon: BookOpen },
    { id: "architecture", label: "Neural Architecture", icon: Brain },
    { id: "accessibility", label: "Accessibility", icon: Accessibility }
  ];

  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (userMenuRef.current && !userMenuRef.current.contains(e.target)) {
        setIsUserMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024) setIsMobileMenuOpen(false);
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const handleNavClick = (id) => {
    setActiveTab(id);
    setIsMobileMenuOpen(false);
  };

  return (
    <header className="w-full bg-[#F8F9FA]/90 backdrop-blur-xl border-b border-zinc-200/80 sticky top-0 z-50 transition-all shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 sm:h-20 flex items-center justify-between gap-3">
        
        {/* Brand Logo */}
        <motion.div 
          onClick={() => setActiveTab("home")}
          className="flex items-center gap-2.5 cursor-pointer group select-none shrink-0"
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.97 }}
          style={{ perspective: 1000 }}
        >
          <motion.div 
            className="w-9 h-9 sm:w-11 sm:h-11 rounded-2xl bg-black p-1 shadow-[0_8px_16px_rgba(0,0,0,0.25)] border border-zinc-700/60 flex items-center justify-center relative overflow-hidden"
            whileHover={{ rotateY: 18, rotateX: -10, boxShadow: "0 12px 24px rgba(0,0,0,0.35)" }}
            transition={{ type: "spring", stiffness: 350, damping: 20 }}
          >
            <motion.div 
              className="absolute inset-0 bg-gradient-to-tr from-pink-500 via-cyan-400 to-yellow-300 opacity-90"
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
            />
            <div className="w-full h-full rounded-xl bg-zinc-950/90 relative z-10 flex items-center justify-center p-1.5 backdrop-blur-sm shadow-inner">
              <svg className="w-4 h-4 sm:w-5 sm:h-5 text-cyan-300 drop-shadow-[0_0_8px_rgba(56,189,248,0.8)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0" />
                <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2" />
                <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8" />
                <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.83l1.76 1.77" />
              </svg>
            </div>
          </motion.div>

          <div>
            <div className="text-sm font-black tracking-tight text-zinc-950 flex items-center gap-1.5">
              <span>SignFlow</span>
              <span className="text-[9px] sm:text-[10px] font-black uppercase tracking-wider bg-black text-white px-1.5 py-0.5 rounded-full shadow-sm">AI</span>
            </div>
            <div className="hidden sm:flex text-[11px] font-medium text-zinc-500 items-center gap-1">
              <span>Neural Sign Vision</span>
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-pulse" />
            </div>
          </div>
        </motion.div>

        {/* Center Nav Links — Desktop only (lg+) */}
        <nav className="hidden lg:flex items-center gap-1 bg-zinc-200/60 backdrop-blur-md p-1.5 rounded-full border border-zinc-300/80 shadow-[inset_0_2px_4px_rgba(0,0,0,0.06)] relative">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <motion.button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                whileHover={{ y: -1 }}
                whileTap={{ scale: 0.96 }}
                className={`relative px-3 xl:px-4 py-1.5 text-xs font-bold rounded-full transition-colors z-10 select-none ${
                  isActive ? "text-black" : "text-zinc-600 hover:text-black"
                }`}
              >
                {isActive && (
                  <motion.div
                    layoutId="navbarActiveIndicator"
                    transition={{ type: "spring", stiffness: 420, damping: 32 }}
                    className="absolute inset-0 bg-white rounded-full shadow-[0_3px_10px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.06)] -z-10 border border-zinc-200/60"
                  />
                )}
                <span className="whitespace-nowrap">{item.label}</span>
              </motion.button>
            );
          })}
        </nav>

        {/* Right Action Bar */}
        <div className="flex items-center gap-1.5 sm:gap-2">
          
          {/* User Auth — hidden on mobile (shown in hamburger menu) */}
          <div className="hidden sm:flex items-center gap-1.5">
            {user ? (
              <div className="relative" ref={userMenuRef}>
                <motion.button
                  onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  className="flex items-center gap-2 py-1.5 pl-2 pr-3 rounded-full bg-zinc-200/80 hover:bg-zinc-300/80 border border-zinc-300 text-zinc-900 transition-all shadow-sm"
                >
                  <div className="w-7 h-7 rounded-full bg-black text-white flex items-center justify-center text-xs font-black shadow-inner">
                    {user.name ? user.name.charAt(0).toUpperCase() : "U"}
                  </div>
                  <div className="hidden md:flex flex-col text-left">
                    <span className="text-xs font-bold leading-tight">{user.name || "My Account"}</span>
                    <span className="text-[10px] text-zinc-500 leading-none">{user.role || "Member"}</span>
                  </div>
                  <ChevronDown className={`w-3.5 h-3.5 text-zinc-600 transition-transform ${isUserMenuOpen ? "rotate-180" : ""}`} />
                </motion.button>

                <AnimatePresence>
                  {isUserMenuOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 10, scale: 0.95 }}
                      transition={{ duration: 0.15 }}
                      className="absolute right-0 mt-2 w-60 bg-zinc-950 border border-zinc-800 rounded-2xl p-2 shadow-2xl z-50 text-white"
                    >
                      <div className="px-3 py-2.5 border-b border-zinc-800">
                        <div className="text-xs font-bold text-white flex items-center gap-1.5">
                          <span>{user.name}</span>
                          <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
                        </div>
                        <div className="text-[11px] text-zinc-400 truncate mt-0.5">{user.email}</div>
                        <div className="inline-block mt-1.5 px-2 py-0.5 rounded-full bg-cyan-950/60 border border-cyan-500/40 text-cyan-300 text-[10px] font-bold">
                          {user.role || "ASL Learner"}
                        </div>
                      </div>
                      <div className="py-1">
                        <button onClick={() => { setActiveTab("tracker"); setIsUserMenuOpen(false); }} className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-zinc-300 hover:text-white hover:bg-zinc-900 transition-colors">
                          <Camera className="w-4 h-4 text-cyan-400" /><span>Practice Studio</span>
                        </button>
                        <button onClick={() => { setActiveTab("matrix"); setIsUserMenuOpen(false); }} className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-zinc-300 hover:text-white hover:bg-zinc-900 transition-colors">
                          <Sparkles className="w-4 h-4 text-yellow-400" /><span>Gesture Directory</span>
                        </button>
                      </div>
                      <div className="pt-1 border-t border-zinc-800">
                        <button onClick={() => { setIsUserMenuOpen(false); if (onLogout) onLogout(); }} className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-bold text-rose-400 hover:bg-rose-500/10 transition-colors">
                          <LogOut className="w-4 h-4" /><span>Log Out</span>
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ) : (
              <div className="flex items-center gap-1.5">
                <motion.button
                  onClick={() => { if (onOpenAuth) onOpenAuth("login"); setActiveTab("auth"); }}
                  whileHover={{ scale: 1.04 }}
                  whileTap={{ scale: 0.96 }}
                  className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold text-zinc-800 hover:text-black rounded-full hover:bg-zinc-200/80 transition-all select-none"
                >
                  <LogIn className="w-3.5 h-3.5" />
                  <span>Log In</span>
                </motion.button>
                <motion.button
                  onClick={() => { if (onOpenAuth) onOpenAuth("signup"); setActiveTab("auth"); }}
                  whileHover={{ scale: 1.04 }}
                  whileTap={{ scale: 0.96 }}
                  className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold bg-zinc-900 hover:bg-black text-white rounded-full transition-all shadow-sm select-none"
                >
                  <UserPlus className="w-3.5 h-3.5" />
                  <span>Sign Up</span>
                </motion.button>
              </div>
            )}
          </div>

          {/* Camera Launch Button — icon only on mobile */}
          <motion.button
            onClick={() => {
              if (activeTab !== "tracker") {
                setActiveTab("tracker");
                if (!isCameraActive) onToggleCamera();
              } else {
                onToggleCamera();
              }
              setIsMobileMenuOpen(false);
            }}
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95, y: 0 }}
            className={`relative group overflow-hidden flex items-center gap-2 px-3 sm:px-5 py-2 sm:py-2.5 rounded-full text-xs font-black tracking-wide transition-all shadow-md select-none shrink-0 ${
              isCameraActive 
                ? "bg-zinc-950 text-white border border-rose-500/60" 
                : "bg-black text-white hover:bg-zinc-900 shadow-zinc-900/20"
            }`}
          >
            <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />
            <span className="relative flex h-2 w-2 shrink-0">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isCameraActive ? "bg-rose-400" : "bg-emerald-400"}`} />
              <span className={`relative inline-flex rounded-full h-2 w-2 ${isCameraActive ? "bg-rose-500" : "bg-emerald-500"}`} />
            </span>
            <Camera className="w-3.5 h-3.5 shrink-0" />
            <span className="hidden sm:inline whitespace-nowrap">{isCameraActive ? "Camera Active" : "Launch Tracker"}</span>
          </motion.button>

          {/* Hamburger — mobile/tablet only */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="lg:hidden flex items-center justify-center w-9 h-9 rounded-full bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-zinc-800 transition-all shrink-0"
            aria-label="Toggle navigation menu"
          >
            {isMobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Mobile Slide-Down Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.22, ease: "easeInOut" }}
            className="lg:hidden overflow-hidden border-t border-zinc-200/80 bg-[#F8F9FA]/97 backdrop-blur-xl"
          >
            <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col gap-1">
              
              {/* Nav Items */}
              {navItems.map((item) => {
                const isActive = activeTab === item.id;
                const IconComp = item.icon;
                return (
                  <button
                    key={item.id}
                    onClick={() => handleNavClick(item.id)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold transition-all text-left ${
                      isActive
                        ? "bg-zinc-900 text-white shadow-sm"
                        : "text-zinc-700 hover:bg-zinc-100 hover:text-black"
                    }`}
                  >
                    <IconComp className={`w-4 h-4 shrink-0 ${isActive ? "text-cyan-300" : "text-zinc-500"}`} />
                    <span>{item.label}</span>
                    {isActive && <span className="ml-auto w-1.5 h-1.5 rounded-full bg-cyan-400" />}
                  </button>
                );
              })}

              {/* Auth Section */}
              <div className="mt-2 pt-3 border-t border-zinc-200 flex flex-col gap-2">
                {user ? (
                  <div className="flex items-center justify-between px-4 py-2.5 rounded-2xl bg-zinc-100 border border-zinc-200">
                    <div className="flex items-center gap-3 min-w-0">
                      <div className="w-8 h-8 rounded-full bg-black text-white flex items-center justify-center text-xs font-black shrink-0">
                        {user.name ? user.name.charAt(0).toUpperCase() : "U"}
                      </div>
                      <div className="min-w-0">
                        <div className="text-xs font-bold text-zinc-900 truncate">{user.name || "My Account"}</div>
                        <div className="text-[11px] text-zinc-500 truncate">{user.email}</div>
                      </div>
                    </div>
                    <button
                      onClick={() => { if (onLogout) onLogout(); setIsMobileMenuOpen(false); }}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-200 transition-colors shrink-0 ml-2"
                    >
                      <LogOut className="w-3.5 h-3.5" />
                      <span>Log Out</span>
                    </button>
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => { if (onOpenAuth) onOpenAuth("login"); setActiveTab("auth"); setIsMobileMenuOpen(false); }}
                      className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl text-sm font-bold text-zinc-800 bg-zinc-100 hover:bg-zinc-200 border border-zinc-200 transition-all"
                    >
                      <LogIn className="w-4 h-4" />
                      <span>Log In</span>
                    </button>
                    <button
                      onClick={() => { if (onOpenAuth) onOpenAuth("signup"); setActiveTab("auth"); setIsMobileMenuOpen(false); }}
                      className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl text-sm font-bold text-white bg-zinc-900 hover:bg-black transition-all shadow-sm"
                    >
                      <UserPlus className="w-4 h-4" />
                      <span>Sign Up</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};

export default Navbar;
