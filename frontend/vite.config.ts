/// <reference types="vite/client" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// For debugging
console.log("VITE_BACKEND_URL:", process.env.VITE_BACKEND_URL);

export default defineConfig({
  plugins: [react()],
  server: {
    watch: {
      usePolling: true,
    },
    host: "0.0.0.0",
    proxy: {},
  },
});
