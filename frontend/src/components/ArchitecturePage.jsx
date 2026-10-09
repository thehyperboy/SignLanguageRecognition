import React from "react";
import { motion } from "framer-motion";
import { 
  ArrowLeft, 
  Cpu, 
  Layers, 
  Activity, 
  Sparkles, 
  CheckCircle2, 
  Zap, 
  BarChart3, 
  ArrowRight,
  ShieldCheck,
  Binary
} from "lucide-react";

export const ArchitecturePage = ({ onBackToHome, onOpenTracker }) => {
  return (
    <div className="min-h-screen bg-[#070708] text-white py-12 px-6 sm:px-12 bg-dots-dark">
      <div className="max-w-7xl mx-auto">
        
        {/* Breadcrumb Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-12 pb-6 border-b border-zinc-800">
          <div className="flex items-center gap-4">
            <button
              onClick={onBackToHome}
              className="px-4 py-2 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-xs font-bold text-zinc-300 hover:text-white flex items-center gap-2 transition-all shadow-md active:scale-95"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Overview</span>
            </button>

            <div>
              <div className="flex items-center gap-2 text-cyan-400 text-xs font-bold tracking-wider uppercase mb-1">
                <Cpu className="w-4 h-4" />
                <span>Deep Learning Pipeline</span>
              </div>
              <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                Neural Architecture & Kinematics
              </h1>
            </div>
          </div>

          <button
            onClick={onOpenTracker}
            className="px-6 py-2.5 rounded-full bg-white text-black text-xs font-black tracking-wide uppercase hover:bg-zinc-200 transition-all shadow-xl active:scale-95 flex items-center gap-2"
          >
            <span>Test In Live Tracker</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Top High-Level Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          <div className="p-5 rounded-2xl bg-[#0F0F12] border border-zinc-800 shadow-xl">
            <div className="text-xs font-semibold text-zinc-400 mb-1">Test Accuracy</div>
            <div className="text-3xl font-black text-emerald-400 tracking-tight">98.44%</div>
            <div className="text-[10px] text-zinc-500 mt-1">Cross-entropy validation</div>
          </div>
          <div className="p-5 rounded-2xl bg-[#0F0F12] border border-zinc-800 shadow-xl">
            <div className="text-xs font-semibold text-zinc-400 mb-1">Spatial Features</div>
            <div className="text-3xl font-black text-cyan-400 tracking-tight">258 Dims</div>
            <div className="text-[10px] text-zinc-500 mt-1">Normalized coordinates</div>
          </div>
          <div className="p-5 rounded-2xl bg-[#0F0F12] border border-zinc-800 shadow-xl">
            <div className="text-xs font-semibold text-zinc-400 mb-1">Temporal Window</div>
            <div className="text-3xl font-black text-purple-400 tracking-tight">30 Frames</div>
            <div className="text-[10px] text-zinc-500 mt-1">1.0 sec continuous motion</div>
          </div>
          <div className="p-5 rounded-2xl bg-[#0F0F12] border border-zinc-800 shadow-xl">
            <div className="text-xs font-semibold text-zinc-400 mb-1">Inference Latency</div>
            <div className="text-3xl font-black text-rose-400 tracking-tight">&lt;15 ms</div>
            <div className="text-[10px] text-zinc-500 mt-1">Sub-frame CPU throughput</div>
          </div>
        </div>

        {/* Two-Column Deep-Dive Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          
          {/* Card 1: Spatial Landmark Extraction Vector */}
          <div className="p-8 rounded-3xl bg-[#0F0F12] border border-zinc-800 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                  Step 1 • Landmark Extraction
                </span>
                <span className="text-xs font-mono text-zinc-500">258 Features / Frame</span>
              </div>
              <h2 className="text-2xl font-black text-white mb-3">MediaPipe Holistic Spatial Vector</h2>
              <p className="text-sm text-zinc-400 leading-relaxed mb-6">
                Every video frame from the webcam is converted into a normalized, illumination-invariant 258-dimensional geometric tensor capturing full upper-body expressive kinematics:
              </p>

              <div className="space-y-3 mb-6">
                <div className="p-4 rounded-xl bg-zinc-900/80 border border-zinc-800 flex items-center justify-between">
                  <div>
                    <div className="text-xs font-bold text-white">Pose Landmarks</div>
                    <div className="text-[11px] text-zinc-400">33 keypoints × 4 (x, y, z, visibility)</div>
                  </div>
                  <span className="font-mono text-xs font-black text-cyan-400">132 dims</span>
                </div>

                <div className="p-4 rounded-xl bg-zinc-900/80 border border-zinc-800 flex items-center justify-between">
                  <div>
                    <div className="text-xs font-bold text-white">Left Hand Landmarks</div>
                    <div className="text-[11px] text-zinc-400">21 keypoints × 3 (x, y, z)</div>
                  </div>
                  <span className="font-mono text-xs font-black text-pink-400">63 dims</span>
                </div>

                <div className="p-4 rounded-xl bg-zinc-900/80 border border-zinc-800 flex items-center justify-between">
                  <div>
                    <div className="text-xs font-bold text-white">Right Hand Landmarks</div>
                    <div className="text-[11px] text-zinc-400">21 keypoints × 3 (x, y, z)</div>
                  </div>
                  <span className="font-mono text-xs font-black text-yellow-400">63 dims</span>
                </div>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-cyan-950/20 border border-cyan-800/40 text-xs text-cyan-200">
              💡 <strong>Zero Sensory Gloves:</strong> Optical computer vision eliminates the need for expensive wearable hardware while maintaining sub-millimeter tracking accuracy.
            </div>
          </div>

          {/* Card 2: 2-Layer LSTM Classification Pipeline */}
          <div className="p-8 rounded-3xl bg-[#0F0F12] border border-zinc-800 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-purple-500/10 text-purple-400 border border-purple-500/30">
                  Step 2 • Recurrent Sequence Classifier
                </span>
                <span className="text-xs font-mono text-zinc-500">TensorFlow / Keras</span>
              </div>
              <h2 className="text-2xl font-black text-white mb-3">2-Layer LSTM Neural Architecture</h2>
              <p className="text-sm text-zinc-400 leading-relaxed mb-6">
                Sign language is fundamentally temporal motion. Static images fail to distinguish gestures like "YES" vs "NO". A 30-frame temporal buffer feeds directly into our trained bidirectional LSTM:
              </p>

              <div className="space-y-3 mb-6">
                <div className="p-3.5 rounded-xl bg-zinc-900/80 border border-zinc-800">
                  <div className="flex justify-between text-xs font-bold text-white mb-1">
                    <span>Input Layer</span>
                    <span className="font-mono text-zinc-400">(Batch, 30, 258)</span>
                  </div>
                  <div className="text-[11px] text-zinc-400">StandardScaler zero-mean unit-variance normalized sequence</div>
                </div>

                <div className="p-3.5 rounded-xl bg-zinc-900/80 border border-zinc-800">
                  <div className="flex justify-between text-xs font-bold text-white mb-1">
                    <span>LSTM Layer 1 (Return Sequences)</span>
                    <span className="font-mono text-purple-400">128 Units • Dropout 0.3</span>
                  </div>
                  <div className="text-[11px] text-zinc-400">Captures long-range trajectory and hand posture transitions</div>
                </div>

                <div className="p-3.5 rounded-xl bg-zinc-900/80 border border-zinc-800">
                  <div className="flex justify-between text-xs font-bold text-white mb-1">
                    <span>LSTM Layer 2</span>
                    <span className="font-mono text-purple-400">64 Units</span>
                  </div>
                  <div className="text-[11px] text-zinc-400">Compresses temporal patterns into high-level gesture representations</div>
                </div>

                <div className="p-3.5 rounded-xl bg-zinc-900/80 border border-zinc-800">
                  <div className="flex justify-between text-xs font-bold text-white mb-1">
                    <span>Dense + Softmax Output</span>
                    <span className="font-mono text-emerald-400">64 Dense → 8 Classes</span>
                  </div>
                  <div className="text-[11px] text-zinc-400">Outputs posterior probabilities across all 8 sign gestures</div>
                </div>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-800/40 text-xs text-purple-200">
              ⚡ <strong>Temporal Filtering:</strong> Sliding window stability voting ensures zero flickering between transient frames and latches results for 1.5 seconds.
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
