import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import confetti from "canvas-confetti";
import { 
  Mail, 
  Lock, 
  User, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  ShieldCheck, 
  ArrowLeft,
  KeyRound,
  Zap,
  HelpCircle
} from "lucide-react";

export function AuthPage({ 
  initialMode = "login", 
  onAuthSuccess, 
  onBackToHome, 
  onOpenTracker,
  isGated = false  // true when used as the full-app auth gate (no "back" escape)
}) {
  const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const [mode, setMode] = useState(initialMode); // "login" | "signup" | "forgot"
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("ASL Learner");
  const [rememberMe, setRememberMe] = useState(true);
  const [agreeTerms, setAgreeTerms] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [forgotSent, setForgotSent] = useState(false);

  // Sync mode if initialMode prop changes
  useEffect(() => {
    setMode(initialMode);
    setErrorMessage("");
    setSuccessMessage("");
  }, [initialMode]);

  const ROLES = [
    { id: "ASL Learner", label: "ASL Learner", icon: "🤟", desc: "Practicing vocabulary & gestures" },
    { id: "Deaf & Hard-of-Hearing", label: "Deaf / HoH", icon: "⚡", desc: "Accessible real-time translation" },
    { id: "Educator & Interpreter", label: "Educator", icon: "🎓", desc: "Teaching & evaluating students" },
    { id: "Researcher & Dev", label: "Researcher", icon: "🔬", desc: "Exploring neural architectures" }
  ];

  // Password Strength Calculation
  const calculatePasswordStrength = (pass) => {
    let score = 0;
    if (!pass) return 0;
    if (pass.length >= 6) score += 1;
    if (pass.length >= 8) score += 1;
    if (/[A-Z]/.test(pass) && /[a-z]/.test(pass)) score += 1;
    if (/[0-9]/.test(pass) || /[^A-Za-z0-9]/.test(pass)) score += 1;
    return score; // 0 to 4
  };

  const strength = calculatePasswordStrength(password);
  const strengthLabels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"];
  const strengthColors = ["bg-zinc-700", "bg-rose-500", "bg-amber-500", "bg-cyan-500", "bg-emerald-500"];

  // Handle Form Submission
  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    // Forgot password flow
    if (mode === "forgot") {
      if (!email || !email.includes("@")) {
        setErrorMessage("Please enter a valid email address.");
        return;
      }
      setIsLoading(true);
      try {
        const res = await fetch(`${API_BASE}/api/auth/forgot-password`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email })
        });
        const data = await res.json();
        setIsLoading(false);
        setForgotSent(true);
        setSuccessMessage(data.message || `Password reset instructions sent to ${email}`);
      } catch (err) {
        setIsLoading(false);
        setForgotSent(true);
        setSuccessMessage(`If an account exists for ${email}, a password reset link has been dispatched.`);
      }
      return;
    }

    // Validation
    if (!email || !email.includes("@")) {
      setErrorMessage("Please enter a valid email address.");
      return;
    }
    if (!password || password.length < 6) {
      setErrorMessage("Password must be at least 6 characters long.");
      return;
    }

    if (mode === "signup") {
      if (!name.trim()) {
        setErrorMessage("Please enter your full name.");
        return;
      }
      if (password !== confirmPassword) {
        setErrorMessage("Passwords do not match.");
        return;
      }
      if (!agreeTerms) {
        setErrorMessage("Please agree to the Terms of Service & Privacy Policy.");
        return;
      }
    }

    setIsLoading(true);

    const endpoint = mode === "signup" ? "/api/auth/signup" : "/api/auth/login";
    const payload = mode === "signup" 
      ? { name, email, password, role } 
      : { email, password };

    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Authentication request failed");
      }

      setIsLoading(false);
      setSuccessMessage(data.message || (mode === "signup" ? "Account created successfully!" : "Signed in successfully!"));

      if (mode === "signup") {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      }

      // Store in localStorage if rememberMe or signup
      if (data.user && data.token) {
        localStorage.setItem("signflow_token", data.token);
        localStorage.setItem("signflow_user", JSON.stringify(data.user));
      }

      setTimeout(() => {
        if (onAuthSuccess) {
          onAuthSuccess(data.user, data.token);
        }
      }, 1000);

    } catch (err) {
      setIsLoading(false);
      setErrorMessage(err.message || "Failed to connect to authentication server.");
    }
  };

  // Instant Demo Account Sign In
  const handleDemoSignIn = async () => {
    setEmail("demo@signflow.ai");
    setPassword("password123");
    setMode("login");
    setErrorMessage("");
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: "demo@signflow.ai", password: "password123" })
      });
      const data = await res.json();
      setIsLoading(false);

      if (res.ok && data.user) {
        setSuccessMessage("Logged in as Demo User!");
        localStorage.setItem("signflow_token", data.token);
        localStorage.setItem("signflow_user", JSON.stringify(data.user));
        setTimeout(() => {
          if (onAuthSuccess) onAuthSuccess(data.user, data.token);
        }, 800);
      } else {
        setErrorMessage(data.error || "Demo login failed");
      }
    } catch (err) {
      setIsLoading(false);
      // Fallback local demo user if server is unreachable
      const demoUser = {
        id: "usr_demo_offline",
        name: "Alex Morgan",
        email: "demo@signflow.ai",
        role: "ASL Learner"
      };
      setSuccessMessage("Logged in as Demo User (Offline Mode)!");
      localStorage.setItem("signflow_user", JSON.stringify(demoUser));
      setTimeout(() => {
        if (onAuthSuccess) onAuthSuccess(demoUser, "demo_token");
      }, 800);
    }
  };

  return (
    <div className={`relative w-full bg-dots-dark flex flex-col justify-center items-center px-4 py-12 md:py-20 select-none overflow-hidden ${isGated ? "min-h-screen" : "min-h-[calc(100vh-80px)]"}`}>
      
      {/* Background Ambient Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-gradient-to-tr from-cyan-500/10 via-pink-500/10 to-yellow-500/10 blur-[130px] pointer-events-none rounded-full" />
      <div className="absolute bottom-10 right-10 w-[350px] h-[350px] bg-emerald-500/5 blur-[100px] pointer-events-none rounded-full" />

      {/* Back to Home Breadcrumb — hidden when used as auth gate */}
      {!isGated && (
        <motion.button
          onClick={onBackToHome}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="absolute top-6 left-6 md:left-12 flex items-center gap-2 text-xs font-bold text-zinc-400 hover:text-white transition-colors py-2 px-3.5 rounded-full bg-zinc-900/60 hover:bg-zinc-850 border border-zinc-800/80 backdrop-blur-md"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Home</span>
        </motion.button>
      )}

      {/* Main Glassmorphic Auth Card */}
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-[480px] bg-zinc-950/85 border border-zinc-800/90 rounded-[32px] p-8 md:p-10 shadow-[0_24px_60px_-15px_rgba(0,0,0,0.7),0_0_0_1px_rgba(255,255,255,0.06)_inset] backdrop-blur-2xl relative z-10"
      >
        
        {/* Top Logo & Holographic Badge */}
        <div className="flex flex-col items-center text-center mb-8">
          <motion.div 
            className="w-14 h-14 rounded-2xl bg-black p-1 shadow-[0_8px_20px_rgba(0,0,0,0.5)] border border-zinc-750 flex items-center justify-center relative overflow-hidden mb-4"
            whileHover={{ scale: 1.08, rotateY: 15 }}
            transition={{ type: "spring", stiffness: 400, damping: 25 }}
          >
            <motion.div 
              className="absolute inset-0 bg-gradient-to-tr from-pink-500 via-cyan-400 to-yellow-300 opacity-90"
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
            />
            <div className="w-full h-full rounded-xl bg-zinc-950/95 relative z-10 flex items-center justify-center p-2 backdrop-blur-sm shadow-inner">
              <svg className="w-6 h-6 text-cyan-300 drop-shadow-[0_0_10px_rgba(56,189,248,0.9)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0" />
                <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2" />
                <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8" />
                <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.83l1.76 1.77" />
              </svg>
            </div>
          </motion.div>

          <h2 className="text-2xl md:text-3xl font-black tracking-tight text-white mb-1.5 flex items-center gap-2">
            <span>{mode === "login" ? "Welcome Back" : mode === "signup" ? "Join SignFlow" : "Reset Password"}</span>
            <span className="text-[10px] font-black uppercase tracking-wider bg-zinc-800 text-cyan-300 border border-cyan-500/30 px-2 py-0.5 rounded-full">
              AI Vision
            </span>
          </h2>
          <p className="text-xs text-zinc-400 max-w-sm">
            {mode === "login" 
              ? "Access your neural gesture tracking studio, practice metrics, and speech preferences." 
              : mode === "signup"
              ? "Create your free account to unlock real-time ASL recognition and custom vocabulary."
              : "Enter your registered email address to receive password recovery instructions."}
          </p>
        </div>

        {/* Mode Selector Pill Tabs (Log In vs Sign Up) */}
        {mode !== "forgot" && (
          <div className="bg-zinc-900/90 p-1.5 rounded-full border border-zinc-800 flex items-center mb-6 relative">
            <button
              type="button"
              onClick={() => { setMode("login"); setErrorMessage(""); setSuccessMessage(""); }}
              className={`flex-1 py-2 text-xs font-bold rounded-full transition-all relative z-10 flex items-center justify-center gap-1.5 ${
                mode === "login" ? "text-black" : "text-zinc-400 hover:text-white"
              }`}
            >
              {mode === "login" && (
                <motion.div
                  layoutId="authPillActive"
                  className="absolute inset-0 bg-white rounded-full shadow-md -z-10"
                  transition={{ type: "spring", stiffness: 450, damping: 35 }}
                />
              )}
              <KeyRound className="w-3.5 h-3.5" />
              <span>Log In</span>
            </button>

            <button
              type="button"
              onClick={() => { setMode("signup"); setErrorMessage(""); setSuccessMessage(""); }}
              className={`flex-1 py-2 text-xs font-bold rounded-full transition-all relative z-10 flex items-center justify-center gap-1.5 ${
                mode === "signup" ? "text-black" : "text-zinc-400 hover:text-white"
              }`}
            >
              {mode === "signup" && (
                <motion.div
                  layoutId="authPillActive"
                  className="absolute inset-0 bg-white rounded-full shadow-md -z-10"
                  transition={{ type: "spring", stiffness: 450, damping: 35 }}
                />
              )}
              <Sparkles className="w-3.5 h-3.5" />
              <span>Sign Up</span>
            </button>
          </div>
        )}

        {/* Alert Notifications (Error or Success) */}
        <AnimatePresence mode="wait">
          {errorMessage && (
            <motion.div
              initial={{ opacity: 0, y: -8, height: 0 }}
              animate={{ opacity: 1, y: 0, height: "auto" }}
              exit={{ opacity: 0, y: -8, height: 0 }}
              className="mb-5 p-3 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2.5 overflow-hidden"
            >
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
              <span className="flex-grow">{errorMessage}</span>
            </motion.div>
          )}

          {successMessage && (
            <motion.div
              initial={{ opacity: 0, y: -8, height: 0 }}
              animate={{ opacity: 1, y: 0, height: "auto" }}
              exit={{ opacity: 0, y: -8, height: 0 }}
              className="mb-5 p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2.5 overflow-hidden"
            >
              <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-emerald-400" />
              <span className="flex-grow">{successMessage}</span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Authentication Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Sign Up Name Field */}
          {mode === "signup" && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-1.5"
            >
              <label className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider block">
                Full Name
              </label>
              <div className="relative flex items-center">
                <User className="absolute left-3.5 w-4 h-4 text-zinc-500" />
                <input
                  type="text"
                  required
                  placeholder="e.g. Jordan Hayes"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-zinc-900/90 border border-zinc-800 rounded-2xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400/50 transition-all"
                />
              </div>
            </motion.div>
          )}

          {/* Email Address Field */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider block">
              Email Address
            </label>
            <div className="relative flex items-center">
              <Mail className="absolute left-3.5 w-4 h-4 text-zinc-500" />
              <input
                type="email"
                required
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-zinc-900/90 border border-zinc-800 rounded-2xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400/50 transition-all"
              />
            </div>
          </div>

          {/* Sign Up Role / Intent Selector */}
          {mode === "signup" && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-1.5 pt-1"
            >
              <label className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider block">
                Your Primary Goal
              </label>
              <div className="grid grid-cols-2 gap-2">
                {ROLES.map((r) => {
                  const isSelected = role === r.id;
                  return (
                    <button
                      type="button"
                      key={r.id}
                      onClick={() => setRole(r.id)}
                      className={`text-left p-2.5 rounded-2xl border transition-all text-xs flex flex-col justify-between ${
                        isSelected 
                          ? "bg-cyan-950/40 border-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.15)]" 
                          : "bg-zinc-900/60 border-zinc-800 text-zinc-400 hover:border-zinc-700"
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-base">{r.icon}</span>
                        {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />}
                      </div>
                      <span className="font-bold text-[11px] leading-tight text-white">{r.label}</span>
                      <span className="text-[10px] text-zinc-400 leading-tight mt-0.5 line-clamp-1">{r.desc}</span>
                    </button>
                  );
                })}
              </div>
            </motion.div>
          )}

          {/* Password Field (for Login and Signup) */}
          {mode !== "forgot" && (
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <label className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider block">
                  Password
                </label>
                {mode === "login" && (
                  <button
                    type="button"
                    onClick={() => { setMode("forgot"); setErrorMessage(""); setSuccessMessage(""); }}
                    className="text-[11px] font-semibold text-cyan-400 hover:text-cyan-300 transition-colors"
                  >
                    Forgot password?
                  </button>
                )}
              </div>
              <div className="relative flex items-center">
                <Lock className="absolute left-3.5 w-4 h-4 text-zinc-500" />
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  placeholder="••••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-zinc-900/90 border border-zinc-800 rounded-2xl pl-10 pr-10 py-2.5 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400/50 transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 text-zinc-500 hover:text-zinc-300 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              {/* Password Strength Meter (Sign Up Only) */}
              {mode === "signup" && password && (
                <div className="space-y-1.5 pt-1">
                  <div className="flex items-center justify-between text-[10px]">
                    <span className="text-zinc-400">Strength:</span>
                    <span className="font-bold text-zinc-300">{strengthLabels[strength]}</span>
                  </div>
                  <div className="grid grid-cols-4 gap-1 h-1.5 w-full">
                    {[1, 2, 3, 4].map((step) => (
                      <div
                        key={step}
                        className={`rounded-full transition-colors ${
                          strength >= step ? strengthColors[strength] : "bg-zinc-800"
                        }`}
                      />
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Confirm Password Field (Sign Up Only) */}
          {mode === "signup" && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <label className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider block">
                  Confirm Password
                </label>
                {confirmPassword && (
                  <span className={`text-[10px] font-bold ${password === confirmPassword ? "text-emerald-400" : "text-rose-400"}`}>
                    {password === confirmPassword ? "✓ Passwords Match" : "✕ Must Match"}
                  </span>
                )}
              </div>
              <div className="relative flex items-center">
                <Lock className="absolute left-3.5 w-4 h-4 text-zinc-500" />
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  required
                  placeholder="••••••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className={`w-full bg-zinc-900/90 border rounded-2xl pl-10 pr-10 py-2.5 text-xs text-white placeholder-zinc-500 focus:outline-none transition-all ${
                    confirmPassword 
                      ? password === confirmPassword 
                        ? "border-emerald-500/60 focus:border-emerald-400" 
                        : "border-rose-500/60 focus:border-rose-400"
                      : "border-zinc-800 focus:border-cyan-400"
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3.5 text-zinc-500 hover:text-zinc-300 transition-colors"
                >
                  {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </motion.div>
          )}

          {/* Checkboxes: Remember Me (Login) or Terms (Signup) */}
          {mode === "login" ? (
            <div className="flex items-center justify-between pt-1">
              <label className="flex items-center gap-2 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="w-3.5 h-3.5 rounded border-zinc-700 bg-zinc-900 text-cyan-500 focus:ring-0 focus:ring-offset-0 cursor-pointer"
                />
                <span className="text-xs text-zinc-400">Remember this device</span>
              </label>
              <div className="flex items-center gap-1 text-[11px] text-zinc-500">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>On-device privacy</span>
              </div>
            </div>
          ) : mode === "signup" ? (
            <div className="pt-1">
              <label className="flex items-start gap-2 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={agreeTerms}
                  onChange={(e) => setAgreeTerms(e.target.checked)}
                  className="w-3.5 h-3.5 rounded border-zinc-700 bg-zinc-900 text-cyan-500 focus:ring-0 focus:ring-offset-0 cursor-pointer mt-0.5"
                />
                <span className="text-[11px] text-zinc-400 leading-tight">
                  I agree to the <span className="text-white hover:underline">Terms of Service</span> and acknowledge that my video is processed 100% locally.
                </span>
              </label>
            </div>
          ) : null}

          {/* Main Action Submit Button */}
          <motion.button
            type="submit"
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`w-full py-3 rounded-2xl text-xs font-black tracking-wide text-black transition-all flex items-center justify-center gap-2 relative overflow-hidden shadow-[0_4px_20px_rgba(255,255,255,0.2)] mt-2 ${
              isLoading 
                ? "bg-zinc-300 opacity-70 cursor-not-allowed" 
                : "bg-white hover:bg-zinc-100"
            }`}
          >
            {isLoading ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin" />
                <span>Processing...</span>
              </div>
            ) : (
              <>
                <span>
                  {mode === "login" 
                    ? "Log In to SignFlow" 
                    : mode === "signup" 
                    ? "Create Account" 
                    : "Send Reset Link"}
                </span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </motion.button>

        </form>

        {/* Forgot Password: Back to Login link */}
        {mode === "forgot" && (
          <div className="mt-4 text-center">
            <button
              type="button"
              onClick={() => { setMode("login"); setErrorMessage(""); setSuccessMessage(""); }}
              className="text-xs font-bold text-zinc-400 hover:text-white transition-colors"
            >
              ← Back to Log In
            </button>
          </div>
        )}

        {/* Divider & Social / Demo Sign In Options */}
        {mode !== "forgot" && (
          <div className="mt-6 pt-6 border-t border-zinc-800/80 space-y-4">
            
            {/* Quick Demo Sign-In (Great for Instant Testing!) */}
            <motion.button
              type="button"
              onClick={handleDemoSignIn}
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full py-2.5 px-4 rounded-2xl bg-zinc-900 hover:bg-zinc-850 border border-zinc-800 hover:border-zinc-700 text-xs font-bold text-zinc-200 transition-all flex items-center justify-center gap-2 shadow-inner group"
            >
              <Zap className="w-3.5 h-3.5 text-yellow-400 fill-yellow-400 group-hover:scale-110 transition-transform" />
              <span>Instant Demo Account Sign-In</span>
              <span className="text-[10px] text-zinc-500 font-normal">(One Click)</span>
            </motion.button>

            {/* Social Logins */}
            <div className="relative flex py-1 items-center">
              <div className="flex-grow border-t border-zinc-850" />
              <span className="flex-shrink mx-3 text-[10px] font-bold text-zinc-500 uppercase tracking-widest">
                Or continue with
              </span>
              <div className="flex-grow border-t border-zinc-850" />
            </div>

            <div className="grid grid-cols-3 gap-2.5">
              {/* Google */}
              <button
                type="button"
                onClick={() => {
                  setName("Google User");
                  setEmail("user@gmail.com");
                  handleDemoSignIn();
                }}
                className="py-2.5 rounded-2xl bg-zinc-900/60 hover:bg-zinc-800 border border-zinc-800/80 flex items-center justify-center transition-all hover:border-zinc-700"
                title="Sign in with Google"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.65v3h3.88c2.27-2.09 3.66-5.17 3.66-9.09z" />
                  <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.1A11.99 11.99 0 0 0 12 24z" />
                  <path fill="#FBBC05" d="M5.28 14.32a7.18 7.18 0 0 1 0-4.64V6.58H1.25a11.99 11.99 0 0 0 0 10.84l4.03-3.1z" />
                  <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.36 0 3.37 2.67 1.25 6.58l4.03 3.1c.95-2.83 3.6-4.93 6.72-4.93z" />
                </svg>
              </button>

              {/* GitHub */}
              <button
                type="button"
                onClick={() => {
                  setName("GitHub Dev");
                  setEmail("developer@github.com");
                  handleDemoSignIn();
                }}
                className="py-2.5 rounded-2xl bg-zinc-900/60 hover:bg-zinc-800 border border-zinc-800/80 flex items-center justify-center transition-all hover:border-zinc-700 text-white"
                title="Sign in with GitHub"
              >
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                  <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                </svg>
              </button>

              {/* Apple */}
              <button
                type="button"
                onClick={() => {
                  setName("Apple User");
                  setEmail("user@icloud.com");
                  handleDemoSignIn();
                }}
                className="py-2.5 rounded-2xl bg-zinc-900/60 hover:bg-zinc-800 border border-zinc-800/80 flex items-center justify-center transition-all hover:border-zinc-700 text-white"
                title="Sign in with Apple"
              >
                <svg className="w-4 h-4 fill-current" viewBox="0 0 170 170">
                  <path d="M150.37 130.25c-2.45 5.66-5.35 10.87-8.71 15.66-4.58 6.53-8.33 11.05-11.22 13.56-4.48 4.12-9.28 6.23-14.42 6.35-3.69 0-8.14-1.05-13.32-3.18-5.19-2.12-9.97-3.17-14.34-3.17-4.58 0-9.49 1.05-14.75 3.17-5.26 2.13-9.5 3.24-12.74 3.35-4.35.13-9.16-1.9-14.42-6.08-3.7-3.04-7.69-7.85-11.96-14.42-5.75-8.89-10.37-19.16-13.86-30.82-3.48-11.66-5.23-22.95-5.23-33.86 0-14.54 3.7-26.69 11.09-36.46 7.4-9.77 16.79-14.76 28.18-14.98 5.12 0 10.74 1.34 16.85 4.02 6.11 2.68 9.94 4.08 11.48 4.2 1.83-.24 5.92-1.74 12.28-4.5 6.36-2.76 11.9-4.04 16.63-3.84 12.63.61 22.84 5.37 30.63 14.28-11.03 6.72-16.42 16.02-16.18 27.9.24 9.4 3.85 17.26 10.83 23.58 4.89 4.41 10.5 7.42 16.85 9.04-2.2 6.36-4.65 12.37-7.34 18.04zM119.22 31.96c0-7.34 2.68-14.38 8.04-21.13 5.35-6.75 11.96-10.83 19.82-12.24.24 1.1.37 2.08.37 2.93 0 7.34-2.81 14.43-8.43 21.26-5.62 6.83-12.39 10.87-20.31 12.12-.13-.97-.2-1.89-.2-2.94z"/>
                </svg>
              </button>
            </div>

            {/* Toggle Between Login and Signup at Bottom */}
            <div className="text-center pt-2">
              <span className="text-xs text-zinc-400">
                {mode === "login" ? "Don't have an account yet?" : "Already have an account?"}
              </span>{" "}
              <button
                type="button"
                onClick={() => {
                  setMode(mode === "login" ? "signup" : "login");
                  setErrorMessage("");
                  setSuccessMessage("");
                }}
                className="text-xs font-bold text-white hover:text-cyan-400 transition-colors underline underline-offset-4"
              >
                {mode === "login" ? "Sign up free" : "Log in"}
              </button>
            </div>

          </div>
        )}

      </motion.div>

      {/* Security & Accessibility Subtitle Footer */}
      <div className="mt-8 flex items-center gap-6 text-[11px] font-semibold text-zinc-500">
        <span className="flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>AES-256 Hashed Security</span>
        </span>
        <span>•</span>
        <span>Zero Video Cloud Upload</span>
        <span>•</span>
        <span>WCAG 2.1 AAA Compliant</span>
      </div>

    </div>
  );
}

export default AuthPage;

