import React from "react";
import { ArrowRight, Cookie, ShieldCheck } from "lucide-react";

const TwitterIcon = () => (
  <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
  </svg>
);

const InstagramIcon = () => (
  <svg className="w-3.5 h-3.5 fill-none stroke-current stroke-2" viewBox="0 0 24 24">
    <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
    <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
    <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
  </svg>
);

const DiscordIcon = () => (
  <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
    <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
  </svg>
);

const GithubIcon = () => (
  <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
    <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
  </svg>
);

export const MascotCookie = ({ onOpenCookieModal = null }) => (
  <div 
    onClick={onOpenCookieModal}
    title="Click to view Cookie & Privacy Settings"
    className="relative w-20 h-20 select-none cursor-pointer group"
  >
    {/* 3D Chocolate Chip Cookie with Bite & Face */}
    <div className="w-20 h-20 rounded-full bg-gradient-to-b from-[#C48C56] via-[#B27943] to-[#8C5728] relative shadow-2xl flex items-center justify-center border-2 border-[#D9A36E]/40 overflow-hidden group-hover:scale-105 transition-transform">
      {/* Cookie Bite out of top-left */}
      <div className="absolute -top-3 -left-3 w-8 h-8 rounded-full bg-[#070708]" />
      
      {/* Chocolate Chips */}
      <div className="absolute top-3 right-5 w-2.5 h-2.5 rounded-full bg-[#4A2810]" />
      <div className="absolute bottom-4 left-4 w-3 h-2.5 rounded-full bg-[#4A2810]" />
      <div className="absolute bottom-5 right-4 w-2 h-2 rounded-full bg-[#4A2810]" />
      
      {/* Happy Face */}
      <div className="flex flex-col items-center mt-1 z-10">
        <div className="flex gap-3 mb-1">
          <div className="w-2 h-2 bg-zinc-950 rounded-full" />
          <div className="w-2 h-2 bg-zinc-950 rounded-full" />
        </div>
        <div className="w-3.5 h-2 border-b-2 border-zinc-950 rounded-full" />
      </div>
    </div>
  </div>
);

export const Footer = ({ 
  onOpenAuth = null,
  cookieConsent = null,
  onAcceptCookies = null,
  onRejectCookies = null,
  onOpenCookieModal = null
}) => {
  return (
    <footer className="w-full bg-[#070708] border-t border-zinc-900 py-10 sm:py-16 px-4 sm:px-8 md:px-12 text-zinc-400 select-none">
      <div className="max-w-7xl mx-auto flex flex-col items-center gap-8 md:flex-row md:items-start md:justify-between md:gap-10">
        
        {/* Left: Copyright & Legal */}
        <div className="flex flex-col items-center md:items-start gap-3 w-full md:w-auto">
          <div className="flex items-center gap-2 text-xs font-bold text-white tracking-widest uppercase">
            <span className="w-2 h-2 rounded-full bg-white" />
            <span>©2026 WGMI • SignFlow</span>
          </div>
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-x-3 gap-y-2 text-[11px] font-semibold text-zinc-500">
            {onOpenAuth && (
              <>
                <button 
                  onClick={() => onOpenAuth("login")}
                  className="hover:text-zinc-200 transition-colors"
                >
                  LOG IN
                </button>
                <span>•</span>
                <button 
                  onClick={() => onOpenAuth("signup")}
                  className="hover:text-zinc-200 transition-colors"
                >
                  SIGN UP
                </button>
                <span>•</span>
              </>
            )}
            <button 
              onClick={onOpenCookieModal} 
              className="hover:text-zinc-200 transition-colors"
            >
              PRIVACY POLICY
            </button>
            <span>•</span>
            <button 
              onClick={onOpenCookieModal} 
              className="hover:text-zinc-200 transition-colors"
            >
              T&C's
            </button>
            <span>•</span>
            <a 
              href="https://github.com" 
              target="_blank" 
              rel="noreferrer" 
              className="hover:text-zinc-300 transition-colors"
            >
              NEURAL REPO
            </a>
          </div>
        </div>

        {/* Center: Mailing List Pill */}
        <div className="flex flex-col items-center gap-2 w-full md:w-auto">
          <span className="text-[10px] font-black tracking-widest text-zinc-500 uppercase">
            MAILING LIST
          </span>
          <form 
            onSubmit={(e) => { e.preventDefault(); alert("Subscribed to SignFlow updates!"); }}
            className="flex items-center bg-zinc-900/90 border border-zinc-700/80 rounded-full pl-5 pr-2 py-1.5 focus-within:border-white transition-all shadow-inner w-full max-w-xs"
          >
            <input 
              type="email" 
              placeholder="Email Address" 
              className="bg-transparent text-xs text-white placeholder-zinc-500 outline-none flex-1 min-w-0"
            />
            <button 
              type="submit" 
              className="w-7 h-7 rounded-full bg-zinc-800 hover:bg-white text-zinc-400 hover:text-black flex items-center justify-center transition-all shrink-0"
            >
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>

        {/* Mascot Center-Right */}
        <div className="hidden lg:flex items-center">
          <MascotCookie onOpenCookieModal={onOpenCookieModal} />
        </div>

        {/* Right: Cookies Policy Consent Controls & Social Icons */}
        <div className="flex flex-col items-center md:items-end gap-3 w-full md:w-auto">
          
          {/* Functional Cookie Consent Controls */}
          <div className="flex items-center gap-2 flex-wrap justify-center">
            <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-500 mr-1 flex items-center gap-1">
              <Cookie className="w-3 h-3 text-amber-400" />
              <span>COOKIES POLICY</span>
            </span>

            {cookieConsent === "accepted" ? (
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-500/40 text-[11px] font-bold text-emerald-300 shadow-sm">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <span>Cookies Accepted</span>
                <button 
                  onClick={onOpenCookieModal}
                  className="ml-1 text-zinc-400 hover:text-white underline text-[10px] cursor-pointer"
                  title="Modify Cookie Settings"
                >
                  Manage
                </button>
              </div>
            ) : cookieConsent === "rejected" ? (
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-700 text-[11px] font-bold text-zinc-300 shadow-sm">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                <span>Essential Only</span>
                <button 
                  onClick={onOpenCookieModal}
                  className="ml-1 text-zinc-400 hover:text-white underline text-[10px] cursor-pointer"
                  title="Modify Cookie Settings"
                >
                  Manage
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-1.5">
                <button 
                  onClick={onAcceptCookies}
                  className="px-3.5 py-1 rounded-full text-[11px] font-bold bg-white text-black hover:bg-zinc-200 transition-colors shadow-sm cursor-pointer"
                >
                  Accept
                </button>
                <button 
                  onClick={onRejectCookies}
                  className="px-3.5 py-1 rounded-full text-[11px] font-bold bg-zinc-900 border border-zinc-700 text-zinc-300 hover:text-white transition-colors cursor-pointer"
                >
                  Reject
                </button>
                <button 
                  onClick={onOpenCookieModal}
                  className="px-3 py-1 rounded-full text-[11px] font-bold bg-zinc-900 border border-zinc-700 text-zinc-300 hover:text-white transition-colors cursor-pointer"
                >
                  Find out more
                </button>
              </div>
            )}
          </div>

          {/* Social Icons */}
          <div className="flex items-center gap-3 pt-1">
            <a href="https://twitter.com" target="_blank" rel="noreferrer" className="w-7 h-7 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-400 hover:text-white hover:border-zinc-600 transition-all">
              <TwitterIcon />
            </a>
            <a href="https://instagram.com" target="_blank" rel="noreferrer" className="w-7 h-7 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-400 hover:text-white hover:border-zinc-600 transition-all">
              <InstagramIcon />
            </a>
            <a href="https://discord.com" target="_blank" rel="noreferrer" className="w-7 h-7 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-400 hover:text-white hover:border-zinc-600 transition-all">
              <DiscordIcon />
            </a>
            <a href="https://github.com" target="_blank" rel="noreferrer" className="w-7 h-7 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-400 hover:text-white hover:border-zinc-600 transition-all">
              <GithubIcon />
            </a>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;
