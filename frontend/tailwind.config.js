/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Poppins", "sans-serif"],
        body: ["Nunito", "sans-serif"]
      },
      colors: {
        soil: "#8a5a44",
        leaf: "#2f7d32",
        sun: "#f4b400",
        sky: "#1e88e5"
      }
    }
  },
  plugins: []
};
