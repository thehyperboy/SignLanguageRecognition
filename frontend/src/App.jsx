import React, { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Navbar } from "./components/Navbar";
import { HeroSection } from "./components/HeroSection";
import { BentoSection } from "./components/BentoSection";
import { TrackerPage } from "./components/TrackerPage";
import { ArchitecturePage } from "./components/ArchitecturePage";
import { GestureLibraryPage } from "./components/GestureLibraryPage";
import { AccessibilityPage } from "./components/AccessibilityPage";
import { AuthPage } from "./components/AuthPage";
import { CookieBanner } from "./components/CookieBanner";
import { CookiePolicyModal } from "./components/CookiePolicyModal";
import { Footer } from "./components/Footer";

export function App() {
  const [activeTab, setActiveTab] = useState("home");
  const [authMode, setAuthMode] = useState("login"); // "login" | "signup"
  const pendingTabRef = useRef(null); // tab user tried to access before signing in

  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem("signflow_user");
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  // Cookie Consent State: 'accepted' | 'rejected' | object | null
  const [cookieConsent, setCookieConsent] = useState(() => {
    try {
      const stored = localStorage.getItem("signflow_cookie_consent");
      if (!stored) return null;
      if (stored === "accepted" || stored === "rejected") return stored;
      return JSON.parse(stored);
    } catch {
      return null;
    }
  });

  const [isCookieModalOpen, setIsCookieModalOpen] = useState(false);

  const [isCameraActive, setIsCameraActive] = useState(false);
  const [mediaStream, setMediaStream] = useState(null);
  const [practiceSign, setPracticeSign] = useState(null);
  const [serverData, setServerData] = useState({
    prediction: "Waiting...",
    confidence: 0,
    display_prediction: "Waiting...",
    display_confidence: 0,
    is_latched: false,
    ready: false,
    frames: 0,
    hand_detected: false,
    last_spoken: "",
    annotated_frame: null
  });
  const [connectionStatus, setConnectionStatus] = useState("connecting");
  const [serverHealth, setServerHealth] = useState(null);

  const workerVideoRef = useRef(null);
  const canvasRef = useRef(null);
  const wsRef = useRef(null);
  const streamRef = useRef(null);
  const isStreamingRef = useRef(false);
  const inFlightRef = useRef(false);

  const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const WS_URL = (import.meta.env.VITE_WS_URL || "ws://localhost:8000") + "/ws/stream";

  // 1. Fetch Backend Health on Mount
  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((res) => res.json())
      .then((data) => {
        setServerHealth(data);
        setConnectionStatus("connected");
      })
      .catch((err) => {
        console.warn("Backend not reached yet:", err);
        setConnectionStatus("offline");
      });
  }, []);

  // 2. Cookie Consent Handlers
  const handleAcceptCookies = () => {
    setCookieConsent("accepted");
    try {
      localStorage.setItem("signflow_cookie_consent", "accepted");
    } catch (e) {
      console.warn("Storage error:", e);
    }
  };

  const handleRejectCookies = () => {
    setCookieConsent("rejected");
    try {
      localStorage.setItem("signflow_cookie_consent", "rejected");
    } catch (e) {
      console.warn("Storage error:", e);
    }
  };

  const handleSaveCustomConsent = (preferences) => {
    setCookieConsent(preferences);
    try {
      localStorage.setItem("signflow_cookie_consent", JSON.stringify(preferences));
    } catch (e) {
      console.warn("Storage error:", e);
    }
  };

  const handleOpenCookieModal = () => {
    setIsCookieModalOpen(true);
  };

  const handleCloseCookieModal = () => {
    setIsCookieModalOpen(false);
  };

  // 3. Camera Controls
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: "user" },
        audio: false,
      });
      streamRef.current = stream;
      setMediaStream(stream);

      if (workerVideoRef.current) {
        workerVideoRef.current.srcObject = stream;
        workerVideoRef.current.play().catch((e) => console.log("Worker video play:", e));
      }

      setIsCameraActive(true);
      connectWebSocket();
    } catch (err) {
      console.error("Camera access failed:", err);
      alert("Camera access denied or device unavailable. Please allow camera permissions in your browser.");
      setIsCameraActive(false);
    }
  };

  const stopCamera = () => {
    isStreamingRef.current = false;
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (workerVideoRef.current) {
      workerVideoRef.current.srcObject = null;
    }
    setMediaStream(null);
    setIsCameraActive(false);

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setServerData((prev) => ({
      ...prev,
      annotated_frame: null,
      prediction: "Waiting...",
      display_prediction: "Waiting...",
      confidence: 0,
      frames: 0,
      hand_detected: false
    }));
  };

  const toggleCamera = () => {
    if (isCameraActive) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  // Re-bind stream to worker video whenever mediaStream changes
  useEffect(() => {
    if (workerVideoRef.current && mediaStream) {
      workerVideoRef.current.srcObject = mediaStream;
      workerVideoRef.current.play().catch(console.error);
    }
  }, [mediaStream]);

  // 4. Frame Sender Function
  const sendFrame = useCallback(() => {
    if (!isStreamingRef.current || inFlightRef.current) return;
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;

    const video = workerVideoRef.current;
    if (!video || video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA) {
      setTimeout(sendFrame, 25);
      return;
    }

    if (!canvasRef.current) {
      canvasRef.current = document.createElement("canvas");
      canvasRef.current.width = 640;
      canvasRef.current.height = 480;
    }

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    ctx.drawImage(video, 0, 0, 640, 480);

    const b64Data = canvas.toDataURL("image/jpeg", 0.50);
    inFlightRef.current = true;
    wsRef.current.send(b64Data);
  }, []);

  // 5. WebSocket Manager
  const connectWebSocket = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      isStreamingRef.current = true;
      sendFrame();
      return;
    }

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("[WS] Connected to inference server.");
      setConnectionStatus("connected");
      isStreamingRef.current = true;
      inFlightRef.current = false;
      sendFrame();
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "inference") {
          setServerData(data);
        }
      } catch (err) {
        console.error("Failed to parse inference payload:", err);
      }
      inFlightRef.current = false;
      if (isStreamingRef.current) {
        requestAnimationFrame(sendFrame);
      }
    };

    ws.onerror = (err) => {
      console.warn("[WS] WebSocket error:", err);
      inFlightRef.current = false;
    };

    ws.onclose = () => {
      console.log("[WS] WebSocket disconnected.");
      isStreamingRef.current = false;
      inFlightRef.current = false;
    };
  };

  // Watchdog timer to prevent frame lockups if a WebSocket frame drops
  useEffect(() => {
    const watchdog = setInterval(() => {
      if (isStreamingRef.current && inFlightRef.current) {
        inFlightRef.current = false;
        sendFrame();
      }
    }, 150);
    return () => clearInterval(watchdog);
  }, [sendFrame]);

  // 6. Reset Recognition Buffer
  const handleResetBuffer = async () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send("RESET");
    } else {
      try {
        await fetch(`${API_BASE}/api/reset`, { method: "POST" });
      } catch (e) {
        console.error("Reset failed:", e);
      }
    }
    setServerData((prev) => ({
      ...prev,
      prediction: "Waiting...",
      display_prediction: "Waiting...",
      confidence: 0,
      display_confidence: 0,
      frames: 0
    }));
  };

  const handleOpenTracker = () => {
    if (!user) {
      pendingTabRef.current = "tracker";
      setAuthMode("login");
      setActiveTab("auth");
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    setActiveTab("tracker");
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (!isCameraActive) {
      startCamera();
    }
  };

  // ─── Auth guard: tabs that require a signed-in user ───────────────────────
  const PROTECTED_TABS = ["tracker", "matrix", "architecture", "accessibility"];

  const handleNavigate = (tabName) => {
    if (!user && PROTECTED_TABS.includes(tabName)) {
      // Remember where they wanted to go, then redirect to auth
      pendingTabRef.current = tabName;
      setAuthMode("login");
      setActiveTab("auth");
    } else {
      setActiveTab(tabName);
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleOpenAuth = (mode = "login") => {
    setAuthMode(mode);
    setActiveTab("auth");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleAuthSuccess = (userData, token) => {
    setUser(userData);
    // After login, go to home (or the originally requested tab)
    setActiveTab(pendingTabRef.current || "home");
    pendingTabRef.current = null;
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleLogout = () => {
    localStorage.removeItem("signflow_user");
    localStorage.removeItem("signflow_token");
    setUser(null);
    setActiveTab("home");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // ─── Auth Gate: if not signed in, show only the auth page ──────────────────
  if (!user) {
    return (
      <div className="min-h-screen bg-[#0B0B0C] text-white font-sans selection:bg-cyan-500 selection:text-black">
        <AuthPage
          initialMode={authMode}
          onAuthSuccess={handleAuthSuccess}
          onBackToHome={() => setAuthMode("login")}
          onOpenTracker={handleOpenTracker}
          isGated={true}
        />

        {/* Cookie consent still works before sign-in */}
        <CookieBanner
          isVisible={cookieConsent === null}
          onAccept={handleAcceptCookies}
          onReject={handleRejectCookies}
          onOpenPreferences={handleOpenCookieModal}
        />
        <CookiePolicyModal
          isOpen={isCookieModalOpen}
          onClose={handleCloseCookieModal}
          consent={cookieConsent}
          onSaveConsent={handleSaveCustomConsent}
        />
      </div>
    );
  }

  // ─── Authenticated App ────────────────────────────────────────────────────
  // ─── Auth Gate: if not signed in, show only the auth page ──────────────────
  if (!user) {
    return (
      <div className="min-h-screen bg-[#0B0B0C] text-white font-sans selection:bg-cyan-500 selection:text-black">
        <AuthPage
          initialMode={authMode}
          onAuthSuccess={handleAuthSuccess}
          onBackToHome={() => {
            // On the auth gate, "back to home" stays on the auth page
            // but we show the landing preview instead (no full nav)
            setAuthMode("login");
          }}
          onOpenTracker={handleOpenTracker}
        />

        {/* Cookie consent still works before sign-in */}
        <CookieBanner
          isVisible={cookieConsent === null}
          onAccept={handleAcceptCookies}
          onReject={handleRejectCookies}
          onOpenPreferences={handleOpenCookieModal}
        />
        <CookiePolicyModal
          isOpen={isCookieModalOpen}
          onClose={handleCloseCookieModal}
          consent={cookieConsent}
          onSaveConsent={handleSaveCustomConsent}
        />
      </div>
    );
  }

  // ─── Authenticated App ────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-[#0B0B0C] text-white flex flex-col font-sans selection:bg-cyan-500 selection:text-black">
      
      {/* Off-screen Worker Video: NEVER unmounts, continuously feeds frames to canvas */}
      <video
        ref={workerVideoRef}
        autoPlay
        playsInline
        muted
        style={{
          position: "fixed",
          top: -9999,
          left: -9999,
          width: 640,
          height: 480,
          opacity: 0,
          pointerEvents: "none"
        }}
      />

      {/* 1. Header Navigation Bar with 3D Motion Graphics & Auth */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={handleNavigate} 
        isCameraActive={isCameraActive} 
        onToggleCamera={toggleCamera}
        connectionStatus={connectionStatus}
        user={user}
        onLogout={handleLogout}
        onOpenAuth={handleOpenAuth}
      />

      {/* 2. Full Page Routing — all tabs accessible after sign-in */}
      <main className="flex-grow">
        {activeTab === "tracker" || activeTab === "live" ? (
          <TrackerPage 
            onBackToHome={() => handleNavigate("home")}
            isCameraActive={isCameraActive}
            onToggleCamera={toggleCamera}
            practiceSign={practiceSign}
            setPracticeSign={setPracticeSign}
            serverData={serverData}
            onResetBuffer={handleResetBuffer}
            annotatedFrame={serverData?.annotated_frame}
            mediaStream={mediaStream}
            connectionStatus={connectionStatus}
          />
        ) : activeTab === "architecture" ? (
          <ArchitecturePage 
            onBackToHome={() => handleNavigate("home")}
            onOpenTracker={handleOpenTracker}
          />
        ) : activeTab === "matrix" ? (
          <GestureLibraryPage 
            onBackToHome={() => handleNavigate("home")}
            onOpenTrackerWithSign={(signName) => {
              setPracticeSign(signName);
              handleOpenTracker();
            }}
          />
        ) : activeTab === "accessibility" ? (
          <AccessibilityPage 
            onBackToHome={() => handleNavigate("home")}
            onOpenTracker={handleOpenTracker}
          />
        ) : (
          <>
            {/* Home Hero Section */}
            <HeroSection 
              onOpenTracker={handleOpenTracker}
              onScrollToDemo={() => {
                const el = document.getElementById("demo-section");
                if (el) el.scrollIntoView({ behavior: "smooth" });
              }}
              isCameraActive={isCameraActive} 
              onToggleCamera={toggleCamera}
              onOpenAuth={handleOpenAuth}
            />

            {/* Home Bento Architecture Showcase Section */}
            <BentoSection 
              onOpenTracker={handleOpenTracker}
              onNavigate={handleNavigate}
            />
          </>
        )}
      </main>

      {/* 3. Footer with Interactive Cookie Controls */}
      <Footer 
        onOpenAuth={handleOpenAuth}
        cookieConsent={cookieConsent}
        onAcceptCookies={handleAcceptCookies}
        onRejectCookies={handleRejectCookies}
        onOpenCookieModal={handleOpenCookieModal}
      />

      {/* 4. First-Visit Cookie & Privacy Consent Banner */}
      <CookieBanner
        isVisible={cookieConsent === null}
        onAccept={handleAcceptCookies}
        onReject={handleRejectCookies}
        onOpenPreferences={handleOpenCookieModal}
      />

      {/* 5. Comprehensive Cookie & Privacy Policy Preferences Modal */}
      <CookiePolicyModal
        isOpen={isCookieModalOpen}
        onClose={handleCloseCookieModal}
        consent={cookieConsent}
        onSaveConsent={handleSaveCustomConsent}
      />

    </div>
  );
}

export default App;
