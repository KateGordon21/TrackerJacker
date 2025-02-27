import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1878B4",
      light: "#ffffff",
      dark: "000000",
    },
    secondary: {
      main: "#2C9CE2", // white
      light: "#D9D9D8", // grey
      dark: "#155983", // black
    },
    background: {
      default: "#ffffff",
    },
  },
  typography: {
    fontFamily: "Arial, sans-serif",
    subtitle1: {
      color: "#1878B4",
      fontSize: 24,
    },
    body1: {
      color: "#000000",
    },
    body2: {
      fontSize: 16,
      color: "#009A4A",
    },
    h1: {
      fontWeight: "550",
      fontSize: 28,
      color: "#009A4A",
    },
    h2: {
      fontWeight: "550",
      fontSize: 20,
      color: "#009A4A",
    },
  },
});

export default theme;
