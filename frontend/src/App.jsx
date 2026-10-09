import React, { useState, useEffect, useRef, useCallback } from "react";
import { Navbar } from "./components/Navbar";
import { HeroSection } from "./components/HeroSection";
import { BentoSection } from "./components/BentoSection";
import { TrackerPage } from "./components/TrackerPage";
import { ArchitecturePage } from "./components/ArchitecturePage";
import { GestureLibraryPage } from "./components/GestureLibraryPage";
import { AccessibilityPage } from "./components/AccessibilityPage";
import { Footer } from "./components/Footer";

export function App() {
  const [activeTab, setActiveTab] = useState("home");
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

  const API_BASE = "http://localhost:8000";
  const WS_URL = "ws://localhost:8000/ws/stream";

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

  // 2. Camera Controls
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

  // 3. Frame Sender Function
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

  // 4. WebSocket Manager
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
        // Immediately request next frame via requestAnimationFrame with ZERO artificial delay
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

  // 5. Reset Recognition Buffer
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
    setActiveTab("tracker");
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (!isCameraActive) {
      startCamera();
    }
  };

  const handleNavigate = (tabName) => {
    setActiveTab(tabName);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

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

      {/* 1. Header Navigation Bar with 3D Motion Graphics */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={handleNavigate} 
        isCameraActive={isCameraActive} 
        onToggleCamera={toggleCamera}
        connectionStatus={connectionStatus}
      />

      {/* 2. Full Page Routing (Clean Dedicated Views - NO MODAL POPUPS) */}
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
            />

            {/* Home Bento Architecture Showcase Section */}
            <BentoSection 
              onOpenTracker={handleOpenTracker}
              onNavigate={handleNavigate}
            />
          </>
        )}
      </main>

      {/* 3. Footer */}
      <Footer />

    </div>
  );
}

export default App;
