import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Cookie, ShieldCheck, X, SlidersHorizontal } from "lucide-react";

export function CookieBanner({ 
  isVisible, 
  onAccept, 
  onReject, 
  onOpenPreferences 
}) {
  if (!isVisible) return null;

  return (
    <AnimatePresence>
      <motion.aside
        initial={{ y: 80, opacity: 0, scale: 0.96 }}
        animate={{ y: 0, opacity: 1, scale: 1 }}
        exit={{ y: 80, opacity: 0, scale: 0.96 }}
        transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
        className="fixed bottom-5 right-5 left-5 md:left-auto md:max-w-md z-50 bg-zinc-950/95 border border-zinc-800 rounded-3xl p-5 sm:p-6 shadow-[0_20px_50px_rgba(0,0,0,0.8),0_0_0_1px_rgba(255,255,255,0.06)_inset] backdrop-blur-2xl text-white select-none"
        role="region"
        aria-label="Cookie and Privacy Consent Banner"
      >
        {/* Top Info Header */}
        <div className="flex items-start gap-3.5 mb-3">
          <div className="w-10 h-10 rounded-2xl bg-zinc-900 border border-zinc-750 flex-shrink-0 flex items-center justify-center relative overflow-hidden shadow-inner">
            <Cookie className="w-5 h-5 text-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.5)]" />
          </div>

          <div className="flex-grow pr-4">
            <div className="flex items-center gap-1.5 text-xs font-black tracking-tight text-white uppercase">
              <span>Privacy & Cookie Preferences</span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            </div>
            <p className="text-[11px] text-zinc-400 leading-relaxed mt-1">
              SignFlow uses essential cookies for neural sessions and user login. 
              <strong className="text-zinc-200"> Your camera video frames are processed 100% on-device</strong> and never recorded or sent to any cloud server.
            </p>
          </div>

          <button
            onClick={onReject}
            className="text-zinc-500 hover:text-zinc-300 transition-colors p-1 -mr-2 -mt-1"
            title="Dismiss & Reject Non-Essential"
            aria-label="Close and reject non-essential cookies"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 pt-2 border-t border-zinc-850">
          
          {/* Learn More & Customize link */}
          <button
            type="button"
            onClick={onOpenPreferences}
            className="flex items-center justify-center gap-1.5 px-3 py-2 text-[11px] font-bold text-zinc-400 hover:text-white rounded-xl hover:bg-zinc-900 transition-colors order-3 sm:order-1"
          >
            <SlidersHorizontal className="w-3 h-3 text-cyan-400" />
            <span>Preferences</span>
          </button>

          <div className="flex items-center gap-2 flex-grow justify-end order-1 sm:order-2">
            {/* Reject Non-Essential */}
            <motion.button
              type="button"
              onClick={onReject}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex-1 sm:flex-initial px-4 py-2 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-900 hover:bg-zinc-850 text-xs font-bold text-zinc-300 hover:text-white transition-all"
            >
              Reject Non-Essential
            </motion.button>

            {/* Accept All */}
            <motion.button
              type="button"
              onClick={onAccept}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex-1 sm:flex-initial px-4 py-2 rounded-xl bg-white hover:bg-zinc-100 text-xs font-black text-black transition-all shadow-[0_2px_10px_rgba(255,255,255,0.2)]"
            >
              Accept All
            </motion.button>
          </div>

        </div>

      </motion.aside>
    </AnimatePresence>
  );
}

export default CookieBanner;

