import {
  Alert,
  Button,
  Container,
  Link,
  TextField,
  Typography,
} from "@mui/material";

import { APP_NAME } from "../../config";
import theme from "../../theme";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import useAuthStore from "../../store/authStore";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const { login, loading, authError, isAuthenticated, setError } =
    useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/");
    }
  }, [isAuthenticated]);

  useEffect(() => {
    setError(null);
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    console.log("Logging in with", { username, password });

    await login({ username, password });

    console.log("Login attempt finished");
  };

  return (
    <>
      <Container
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Typography variant="subtitle1" sx={{ margin: 3 }}>
          {APP_NAME}
        </Typography>
        <Container
          component="form"
          onSubmit={handleLogin}
          sx={{
            display: "flex",
            flexDirection: "column",
            width: "70vw",
            maxWidth: "500px",
            gap: 2,
            justifyContent: "center",
            alignItems: "center",
            borderRadius: 5,
            boxShadow: 3,
            padding: 2,
          }}
        >
          <Typography variant="subtitle2">Login</Typography>
          <TextField
            label="Username"
            variant="outlined"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            sx={{ width: "100%" }}
            required
          />
          <TextField
            label="Password"
            variant="outlined"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{ width: "100%" }}
            required
          />
          <Container sx={{ margin: 0, width: "110%" }}>
            <Link
              variant="body1"
              sx={{ textDecoration: "none", cursor: "pointer" }}
              href="/signup/"
            >
              Sign Up
            </Link>
          </Container>
          <Button
            type="submit"
            variant="contained"
            disabled={loading}
            sx={{
              width: "50%",
              "&:hover": {
                backgroundColor: theme.palette.secondary.dark,
              },
            }}
          >
            Login
          </Button>

          {authError && (
            <Alert severity="error" variant="standard">
              {authError}
            </Alert>
          )}
        </Container>
      </Container>
    </>
  );
}
