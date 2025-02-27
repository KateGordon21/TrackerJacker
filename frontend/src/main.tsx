import { createRoot } from "react-dom/client";
import App from "./App.tsx";

createRoot(document.getElementById("root")!).render(<App />);
document.title = import.meta.env.VITE_APP_NAME;
