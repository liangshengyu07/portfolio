"use client";

import React, { useEffect, useRef, useState } from "react";
import { ArrowRight, Menu, X } from "lucide-react";
import Hls from "hls.js";

/* ───────────────────────────────────────────
   CodeNest Hero Section
   Next.js 14 (App Router) + React 18 + Tailwind CSS
   ─────────────────────────────────────────── */

const HLS_STREAM_URL =
  "https://stream.mux.com/tLkHO1qZoaaQOUeVWo8hEBeGQfySP02EPS02BmnNFyXys.m3u8";

const NAV_LINKS = [
  { label: "PROJECTS", href: "#projects" },
  { label: "BLOG", href: "#blog" },
  { label: "ABOUT", href: "#about" },
  { label: "RESUME", href: "#resume" },
];

/* ─────────── Background Video ─────────── */
function BackgroundVideo() {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    if (Hls.isSupported()) {
      const hls = new Hls({
        enableWorker: false, // required for sandboxed environments
        debug: false,
      });
      hls.loadSource(HLS_STREAM_URL);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.play().catch(() => {
          // autoplay blocked — silent fallback
        });
      });
      return () => {
        hls.destroy();
      };
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      // Native HLS support (Safari)
      video.src = HLS_STREAM_URL;
      video.addEventListener("loadedmetadata", () => {
        video.play().catch(() => {});
      });
    }
  }, []);

  return (
    <video
      ref={videoRef}
      muted
      loop
      playsInline
      autoPlay
      className="absolute inset-0 w-full h-full object-cover"
      style={{ opacity: 0.6 }}
    />
  );
}

/* ─────────── Navbar ─────────── */
function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      <header className="absolute top-0 left-0 w-full z-50 px-6 md:px-12 py-6">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <a href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
              <span className="text-[#070b0a] font-bold text-sm font-inter">C</span>
            </div>
            <span className="text-white font-inter font-semibold text-lg tracking-tight">
              CodeNest
            </span>
          </a>

          {/* Desktop Menu */}
          <nav className="hidden md:flex items-center gap-8">
            {NAV_LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-white font-inter text-base font-medium transition-colors duration-200 hover:text-[#5ed29c]"
              >
                {link.label}
              </a>
            ))}
          </nav>

          {/* Mobile Hamburger */}
          <button
            className="md:hidden text-white p-2"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={24} />
          </button>
        </div>
      </header>

      {/* Mobile Overlay */}
      <div
        className={`fixed inset-0 z-[100] bg-[#070b0a] transition-transform duration-300 ease-in-out md:hidden ${
          mobileOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex flex-col h-full px-8 py-6">
          <div className="flex justify-between items-center mb-12">
            <a href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
                <span className="text-[#070b0a] font-bold text-sm font-inter">C</span>
              </div>
              <span className="text-white font-inter font-semibold text-lg tracking-tight">
                CodeNest
              </span>
            </a>
            <button
              className="text-white p-2"
              onClick={() => setMobileOpen(false)}
              aria-label="Close menu"
            >
              <X size={24} />
            </button>
          </div>
          <nav className="flex flex-col gap-6">
            {NAV_LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className="text-white font-inter text-2xl font-medium transition-colors duration-200 hover:text-[#5ed29c]"
              >
                {link.label}
              </a>
            ))}
          </nav>
        </div>
      </div>
    </>
  );
}

/* ─────────── Liquid Glass Card ─────────── */
function LiquidGlassCard() {
  return (
    <div className="liquid-glass-card translate-y-[-50px] z-20">
      <span className="font-inter text-[14px] text-white/70 mb-2">
        [ 2025 ]
      </span>
      <h3 className="font-inter text-[18px] font-semibold text-white leading-tight mb-2">
        Taught by{" "}
        <span className="font-instrument-serif italic">Industry</span>{" "}
        Professionals
      </h3>
      <p className="font-inter text-[11px] text-white/50 leading-relaxed">
        Learn from engineers who have built systems at scale for the world&apos;s top tech companies.
      </p>
    </div>
  );
}

/* ─────────── Hero Section ─────────── */
export default function HeroPage() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-[#070b0a]">
      {/* Background Video Layer */}
      <div className="absolute inset-0 z-0">
        <BackgroundVideo />
      </div>

      {/* Left-to-right dark gradient overlay */}
      <div
        className="absolute inset-0 z-10 pointer-events-none"
        style={{
          background:
            "linear-gradient(to right, #070b0a 0%, rgba(7, 11, 10, 0.8) 30%, transparent 100%)",
        }}
      />

      {/* Bottom-up gradient for readability */}
      <div
        className="absolute inset-0 z-10 pointer-events-none"
        style={{
          background:
            "linear-gradient(to top, rgba(7, 11, 10, 0.95) 0%, rgba(7, 11, 10, 0.4) 40%, transparent 70%)",
        }}
      />

      {/* Vertical Grid Lines (desktop only) */}
      <div className="hidden lg:block absolute inset-0 z-10 pointer-events-none">
        <div
          className="absolute top-0 bottom-0 w-px bg-white/10"
          style={{ left: "25%" }}
        />
        <div
          className="absolute top-0 bottom-0 w-px bg-white/10"
          style={{ left: "50%" }}
        />
        <div
          className="absolute top-0 bottom-0 w-px bg-white/10"
          style={{ left: "75%" }}
        />
      </div>

      {/* Central Glow Ellipse */}
      <div className="absolute top-[10%] left-1/2 -translate-x-1/2 z-10 pointer-events-none">
        <svg
          width="800"
          height="300"
          viewBox="0 0 800 300"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="max-w-[90vw]"
        >
          <defs>
            <filter id="glowBlur" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="25" result="blur" />
            </filter>
          </defs>
          <ellipse
            cx="400"
            cy="150"
            rx="350"
            ry="80"
            fill="url(#glowGradient)"
            filter="url(#glowBlur)"
            opacity="0.6"
          />
          <defs>
            <linearGradient id="glowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.3" />
              <stop offset="50%" stopColor="#10b981" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.3" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      {/* Navigation */}
      <Navbar />

      {/* Hero Content */}
      <section className="relative z-20 flex flex-col items-center justify-center min-h-screen px-6 md:px-12 pt-24 pb-12">
        <div className="max-w-4xl w-full flex flex-col items-center text-center">
          {/* Floating Liquid Glass Card */}
          <LiquidGlassCard />

          {/* Eyebrow */}
          <span className="font-plus-jakarta font-bold text-[11px] uppercase tracking-widest text-[#5ed29c] mt-4 mb-6">
            Career-Ready Curriculum
          </span>

          {/* Main Headline */}
          <h1 className="font-inter font-extrabold uppercase tracking-tight text-white leading-[1.05] mb-6">
            <span className="block text-[40px] md:text-[56px] lg:text-[72px]">
              Launch Your Coding
            </span>
            <span className="block text-[40px] md:text-[56px] lg:text-[72px]">
              Career<span className="text-[#5ed29c]">.</span>
            </span>
          </h1>

          {/* Description */}
          <p className="font-inter text-[14px] text-white/70 leading-relaxed max-w-[512px] mb-8">
            Master in-demand coding skills with hands-on projects, real-world mentorship, and a
            curriculum designed by engineers from Google, Meta, and Amazon. Your path to a six-figure
            developer career starts here.
          </p>

          {/* Primary CTA */}
          <a
            href="#enroll"
            className="group inline-flex items-center gap-3 rounded-full bg-[#5ed29c] px-8 py-4 text-[#070b0a] font-inter font-bold uppercase text-sm tracking-wide transition-all duration-200 hover:bg-[#4bc88a] hover:scale-105 active:scale-95"
          >
            Get Started
            <ArrowRight
              size={18}
              className="transition-transform duration-200 group-hover:translate-x-1"
            />
          </a>
        </div>
      </section>
    </main>
  );
}
