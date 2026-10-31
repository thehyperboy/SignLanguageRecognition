import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  X, 
  Cookie, 
  ShieldCheck, 
  Check, 
  Sliders, 
  Lock, 
  EyeOff, 
  Cpu, 
  CheckCircle2, 
  Info,
  Volume2
} from "lucide-react";

export function CookiePolicyModal({ 
  isOpen, 
  onClose, 
  consent, 
  onSaveConsent 
}) {
  const [preferences, setPreferences] = useState({
    necessary: true,
    analytics: consent === "accepted" || (typeof consent === "object" && consent?.analytics !== false),
    accessibility: consent === "accepted" || (typeof consent === "object" && consent?.accessibility !== false),
  });

  const [savedToast, setSavedToast] = useState(false);

  useEffect(() => {
    if (consent === "accepted") {
      setPreferences({ necessary: true, analytics: true, accessibility: true });
    } else if (consent === "rejected") {
      setPreferences({ necessary: true, analytics: false, accessibility: false });
    } else if (typeof consent === "object" && consent !== null) {
      setPreferences({
        necessary: true,
        analytics: !!consent.analytics,
        accessibility: !!consent.accessibility,
      });
    }
  }, [consent]);

  // Handle ESC key to close
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleToggle = (key) => {
    if (key === "necessary") return; // strictly necessary cannot be disabled
    setPreferences((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSave = () => {
    onSaveConsent(preferences);
    setSavedToast(true);
    setTimeout(() => {
      setSavedToast(false);
      onClose();
    }, 600);
  };

  const handleAcceptAll = () => {
    const all = { necessary: true, analytics: true, accessibility: true };
    setPreferences(all);
    onSaveConsent("accepted");
    setSavedToast(true);
    setTimeout(() => {
      setSavedToast(false);
      onClose();
    }, 600);
  };

  const handleRejectAll = () => {
    const rejected = { necessary: true, analytics: false, accessibility: false };
    setPreferences(rejected);
    onSaveConsent("rejected");
    setSavedToast(true);
    setTimeout(() => {
      setSavedToast(false);
      onClose();
    }, 600);
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
        
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/75 backdrop-blur-md transition-opacity"
        />

        {/* Modal Dialog Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 15 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 15 }}
          transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
          className="relative w-full max-w-2xl bg-zinc-950 border border-zinc-800 rounded-[28px] p-6 sm:p-8 shadow-[0_25px_60px_-15px_rgba(0,0,0,0.9),0_0_0_1px_rgba(255,255,255,0.06)_inset] text-white z-10 max-h-[90vh] flex flex-col overflow-hidden"
        >
          
          {/* Header */}
          <div className="flex items-start justify-between pb-5 border-b border-zinc-850">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-zinc-900 border border-zinc-750 flex items-center justify-center shadow-inner">
                <Cookie className="w-5 h-5 text-amber-400" />
              </div>
              <div>
                <h3 className="text-lg font-black text-white tracking-tight flex items-center gap-2">
                  <span>Cookie Privacy Policy & Preferences</span>
                </h3>
                <p className="text-xs text-zinc-400 mt-0.5">
                  SignFlow Privacy Notice • Updated for local neural processing
                </p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="w-8 h-8 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-400 hover:text-white flex items-center justify-center transition-colors"
              aria-label="Close modal"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Modal Body: Scrollable Content */}
          <div className="py-5 space-y-6 overflow-y-auto pr-1 flex-grow">
            
            {/* Overview Banner */}
            <div className="p-4 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 text-xs text-zinc-300 leading-relaxed flex items-start gap-3">
              <ShieldCheck className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-white mb-1">Our Privacy First Commitment</p>
                <p>
                  We prioritize your fundamental digital privacy. SignFlow uses cookies and local browser storage 
                  solely to keep you signed in, remember your accessibility preferences, and calibrate the real-time neural inference engine.
                </p>
              </div>
            </div>

            {/* Video & Camera Stream Policy Guarantee */}
            <div className="p-4 rounded-2xl bg-cyan-950/20 border border-cyan-500/20 text-xs text-zinc-300 leading-relaxed flex items-start gap-3">
              <EyeOff className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-cyan-200 mb-1">100% On-Device Camera Processing</p>
                <p className="text-zinc-400">
                  Your webcam stream is captured in your local browser and sent over a private localhost bridge to the MediaPipe holistic landmarker. 
                  <strong className="text-zinc-200"> No video footage, facial biometrics, or camera recordings are ever stored in cookies or uploaded to third-party cloud servers.</strong>
                </p>
              </div>
            </div>

            {/* Granular Cookie Categories */}
            <div className="space-y-4">
              <h4 className="text-xs font-black uppercase tracking-wider text-zinc-400 flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5" />
                <span>Manage Cookie Categories</span>
              </h4>

              {/* 1. Necessary Cookies */}
              <div className="p-4 rounded-2xl bg-zinc-900/90 border border-zinc-800 flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white">Strictly Necessary Cookies</span>
                    <span className="text-[10px] font-black uppercase tracking-wider bg-zinc-800 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded-full">
                      Always Active
                    </span>
                  </div>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Essential for website security, user authentication sessions (<code className="text-zinc-300 bg-zinc-850 px-1 py-0.5 rounded text-[11px]">signflow_token</code>), and WebSocket inference streaming handshake. These cannot be switched off.
                  </p>
                </div>
                <div className="flex-shrink-0 pt-1">
                  <div className="w-10 h-6 bg-emerald-500 rounded-full flex items-center justify-end px-1 cursor-not-allowed opacity-90">
                    <div className="w-4 h-4 bg-white rounded-full shadow-sm flex items-center justify-center">
                      <Check className="w-2.5 h-2.5 text-emerald-600 stroke-[3]" />
                    </div>
                  </div>
                </div>
              </div>

              {/* 2. Accessibility & Speech Synthesis Cookies */}
              <div className="p-4 rounded-2xl bg-zinc-900/90 border border-zinc-800 flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white">Speech Synthesis & Accessibility Preferences</span>
                    <span className="text-[10px] font-semibold text-zinc-500">Optional</span>
                  </div>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Saves your chosen Text-to-Speech voice rate, volume, audio feedback preferences, and high-contrast view states so you don't have to reconfigure them each session.
                  </p>
                </div>
                <div className="flex-shrink-0 pt-1">
                  <button
                    type="button"
                    onClick={() => handleToggle("accessibility")}
                    className={`w-10 h-6 rounded-full transition-colors flex items-center px-1 cursor-pointer ${
                      preferences.accessibility ? "bg-cyan-500 justify-end" : "bg-zinc-800 justify-start"
                    }`}
                  >
                    <motion.div 
                      layout 
                      transition={{ type: "spring", stiffness: 500, damping: 30 }}
                      className="w-4 h-4 bg-white rounded-full shadow-sm" 
                    />
                  </button>
                </div>
              </div>

              {/* 3. Analytics & Telemetry Cookies */}
              <div className="p-4 rounded-2xl bg-zinc-900/90 border border-zinc-800 flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white">Performance Benchmarking & Telemetry</span>
                    <span className="text-[10px] font-semibold text-zinc-500">Optional</span>
                  </div>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Collects local runtime performance diagnostics (FPS, WebSocket latency, temporal buffer frame drop statistics) to evaluate model responsiveness and prevent video lag.
                  </p>
                </div>
                <div className="flex-shrink-0 pt-1">
                  <button
                    type="button"
                    onClick={() => handleToggle("analytics")}
                    className={`w-10 h-6 rounded-full transition-colors flex items-center px-1 cursor-pointer ${
                      preferences.analytics ? "bg-cyan-500 justify-end" : "bg-zinc-800 justify-start"
                    }`}
                  >
                    <motion.div 
                      layout 
                      transition={{ type: "spring", stiffness: 500, damping: 30 }}
                      className="w-4 h-4 bg-white rounded-full shadow-sm" 
                    />
                  </button>
                </div>
              </div>

            </div>

          </div>

          {/* Footer Actions */}
          <div className="pt-4 border-t border-zinc-850 flex flex-col sm:flex-row items-center justify-between gap-3">
            <button
              type="button"
              onClick={handleRejectAll}
              className="w-full sm:w-auto px-4 py-2.5 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-900/80 hover:bg-zinc-850 text-xs font-bold text-zinc-300 hover:text-white transition-all order-2 sm:order-1"
            >
              Reject Non-Essential
            </button>

            <div className="flex items-center gap-2.5 w-full sm:w-auto order-1 sm:order-2">
              <button
                type="button"
                onClick={handleSave}
                className="flex-1 sm:flex-initial px-4 py-2.5 rounded-xl border border-zinc-700 bg-zinc-850 hover:bg-zinc-800 text-xs font-bold text-white transition-all shadow-sm"
              >
                Save Preferences
              </button>

              <button
                type="button"
                onClick={handleAcceptAll}
                className="flex-1 sm:flex-initial px-5 py-2.5 rounded-xl bg-white hover:bg-zinc-200 text-xs font-black text-black transition-all shadow-[0_4px_15px_rgba(255,255,255,0.2)]"
              >
                Accept All
              </button>
            </div>
          </div>

          {/* Saved Toast Feedback */}
          <AnimatePresence>
            {savedToast && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute bottom-5 left-1/2 -translate-x-1/2 px-4 py-2 rounded-full bg-emerald-500 text-black text-xs font-bold shadow-2xl flex items-center gap-1.5 z-20"
              >
                <CheckCircle2 className="w-4 h-4 text-black" />
                <span>Preferences saved successfully!</span>
              </motion.div>
            )}
          </AnimatePresence>

        </motion.div>

      </div>
    </AnimatePresence>
  );
}

export default CookiePolicyModal;

