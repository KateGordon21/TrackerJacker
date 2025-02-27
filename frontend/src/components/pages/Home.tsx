import { Container, Typography } from "@mui/material";
import logo from "../../assets/logo.png";

import { APP_NAME } from "../../config";
import Budget from "../Budget";

export default function Home() {
  return (
    <>
      <Container
        maxWidth={false}
        sx={{
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Logo and App Name Container */}
        <Container
          sx={{
            display: "flex",
            flexDirection: "row",
            position: "fixed", // Change to fixed positioning
            top: 0,
            left: 0,
            mt: 2,
            gap: 2,
          }}
        >
          <img
            src={logo}
            alt="Emdc Homepage"
            style={{
              width: "100px",
              height: "auto",
            }}
          />
          <Typography variant="subtitle1" sx={{ mt: 2 }}>
            {APP_NAME}
          </Typography>
        </Container>

        {/* Content Section */}
        <Budget />
      </Container>
    </>
  );
}
