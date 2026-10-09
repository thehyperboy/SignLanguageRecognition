import React, { useState } from "react";
import { motion } from "framer-motion";
import { 
  ArrowLeft, 
  Layers, 
  ArrowRight, 
  Sparkles, 
  CheckCircle2, 
  Filter, 
  Play, 
  Search 
} from "lucide-react";

export const GestureLibraryPage = ({ onBackToHome, onOpenTrackerWithSign }) => {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  const gestures = [
    {
      id: "hello",
      name: "HELLO",
      icon: "👋",
      category: "greeting",
      tag: "Greeting",
      difficulty: "Easy",
      hands: "Dominant Hand",
      desc: "Raise dominant hand to shoulder height with open palm and wave from side to side smoothly.",
      tips: "Keep wrist relaxed and face the camera directly.",
      features: "Right hand keypoints (wrist to pinky)"
    },
    {
      id: "thank_you",
      name: "THANK YOU",
      icon: "🙏",
      category: "courtesy",
      tag: "Courtesy",
      difficulty: "Easy",
      hands: "Dominant Hand",
      desc: "Touch fingertips of open hand to chin or lower lip, then smoothly extend hand forward toward camera.",
      tips: "Keep fingers flat and finish with palm facing upward.",
      features: "Fingertips to chin distance tracking"
    },
    {
      id: "yes",
      name: "YES",
      icon: "🙆",
      category: "affirmation",
      tag: "Affirmation",
      difficulty: "Easy",
      hands: "Dominant Hand",
      desc: "Form a relaxed fist at chest height and nod your wrist up and down repeatedly like a nodding head.",
      tips: "Focus motion in the wrist rather than the full arm.",
      features: "Wrist angular pitch acceleration"
    },
    {
      id: "no",
      name: "NO",
      icon: "🙅",
      category: "affirmation",
      tag: "Negation",
      difficulty: "Medium",
      hands: "Dominant Hand",
      desc: "Extend index and middle fingers together, then snap them down firmly onto the thumb.",
      tips: "Resembles a mouth closing quickly.",
      features: "Index & middle DIP distance to thumb tip"
    },
    {
      id: "help",
      name: "HELP",
      icon: "🆘",
      category: "needs",
      tag: "Assistance",
      difficulty: "Medium",
      hands: "Two Hands",
      desc: "Place a closed fist with thumb pointing up on top of flat open palm, then elevate both hands together.",
      tips: "Non-dominant hand acts as a supporting platform.",
      features: "Dual-hand proximity and vertical elevation"
    },
    {
      id: "love",
      name: "LOVE",
      icon: "🤟",
      category: "emotion",
      tag: "Emotion",
      difficulty: "Easy",
      hands: "Dominant Hand",
      desc: "Extend thumb, index, and pinky fingers outward while folding middle and ring fingers down into palm.",
      tips: "Universal ASL 'I Love You' combining letters I, L, and Y.",
      features: "Thumb, index & pinky vector alignment"
    },
    {
      id: "please",
      name: "PLEASE",
      icon: "🤲",
      category: "courtesy",
      tag: "Courtesy",
      difficulty: "Easy",
      hands: "Dominant Hand",
      desc: "Place flat open palm over center of chest and rub in a smooth clockwise circular motion.",
      tips: "Maintain contact with chest area while rotating.",
      features: "Planar circular centroid trajectory"
    },
    {
      id: "sorry",
      name: "SORRY",
      icon: "✊",
      category: "courtesy",
      tag: "Courtesy",
      difficulty: "Easy",
      hands: "Dominant Hand",
      desc: "Form a closed fist against the center of your chest and rub in a gentle circular motion.",
      tips: "Keep thumb wrapped across fingers facing inward.",
      features: "Fist circular trajectory on torso plane"
    }
  ];

  const filtered = gestures.filter((g) => {
    const matchesCategory = selectedCategory === "all" || g.category === selectedCategory;
    const matchesSearch = g.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          g.desc.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-[#070708] text-white py-12 px-6 sm:px-12 bg-dots-dark">
      <div className="max-w-7xl mx-auto">
        
        {/* Header Breadcrumb */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-10 pb-6 border-b border-zinc-800">
          <div className="flex items-center gap-4">
            <button
              onClick={onBackToHome}
              className="px-4 py-2 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-xs font-bold text-zinc-300 hover:text-white flex items-center gap-2 transition-all shadow-md active:scale-95"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Overview</span>
            </button>

            <div>
              <div className="flex items-center gap-2 text-emerald-400 text-xs font-bold tracking-wider uppercase mb-1">
                <Layers className="w-4 h-4" />
                <span>Sign Language Matrix</span>
              </div>
              <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                Gesture Library & Practice Studio
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-3.5 top-3" />
              <input
                type="text"
                placeholder="Search gestures..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-zinc-900 border border-zinc-800 rounded-full pl-9 pr-4 py-2 text-xs text-white placeholder-zinc-500 outline-none focus:border-zinc-600 transition-colors w-44 sm:w-56"
              />
            </div>
          </div>
        </div>

        {/* Category Filter Pills */}
        <div className="flex flex-wrap items-center gap-2 mb-10">
          {[
            { id: "all", label: "All Gestures (8)" },
            { id: "greeting", label: "Greetings" },
            { id: "courtesy", label: "Courtesy & Politeness" },
            { id: "affirmation", label: "Yes / No" },
            { id: "needs", label: "Needs & Assistance" },
            { id: "emotion", label: "Emotions" },
          ].map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-4 py-2 rounded-full text-xs font-bold transition-all ${
                selectedCategory === cat.id
                  ? "bg-white text-black shadow-lg"
                  : "bg-zinc-900 text-zinc-400 hover:text-white border border-zinc-800"
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Gestures Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {filtered.map((sign) => (
            <div
              key={sign.id}
              className="p-6 rounded-3xl bg-[#0F0F12] border border-zinc-800 shadow-xl flex flex-col justify-between hover:border-zinc-700 transition-all group"
            >
              <div>
                <div className="flex items-start justify-between mb-4">
                  <div className="w-14 h-14 rounded-2xl bg-zinc-900 border border-zinc-800 flex items-center justify-center text-3xl shadow-md group-hover:scale-105 transition-transform">
                    {sign.icon}
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-zinc-800 text-zinc-300">
                      {sign.tag}
                    </span>
                    <span className="text-[10px] text-zinc-500 font-semibold">{sign.difficulty}</span>
                  </div>
                </div>

                <h3 className="text-xl font-black text-white tracking-tight mb-2 group-hover:text-emerald-400 transition-colors">
                  {sign.name}
                </h3>
                <p className="text-xs text-zinc-400 leading-relaxed mb-4">
                  {sign.desc}
                </p>

                <div className="p-3 rounded-xl bg-zinc-900/80 border border-zinc-800/80 text-[11px] text-zinc-300 mb-6">
                  <div className="font-semibold text-white mb-0.5">💡 Kinematic Tip:</div>
                  <div className="text-zinc-400">{sign.tips}</div>
                </div>
              </div>

              <button
                onClick={() => onOpenTrackerWithSign(sign.name)}
                className="w-full py-2.5 rounded-full bg-zinc-900 group-hover:bg-white text-zinc-300 group-hover:text-black text-xs font-bold flex items-center justify-center gap-2 transition-all border border-zinc-800 group-hover:border-white shadow-md active:scale-95"
              >
                <span>Practice in Tracker</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
};
