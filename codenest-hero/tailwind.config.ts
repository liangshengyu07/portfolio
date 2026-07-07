import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)", "Inter", "sans-serif"],
        inter: ["var(--font-inter)", "Inter", "sans-serif"],
        "plus-jakarta": ["var(--font-plus-jakarta)", "Plus Jakarta Sans", "sans-serif"],
        "instrument-serif": ["var(--font-instrument-serif)", "Instrument Serif", "serif"],
      },
      colors: {
        codenest: {
          bg: "#070b0a",
          accent: "#5ed29c",
        },
      },
    },
  },
  plugins: [],
};

export default config;
