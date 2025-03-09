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
import { useEffect, useState } from "react";
import useAuthStore from "../../store/authStore";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const { register, loading, authError, isAuthenticated, user } =
    useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/");
    }
  }, [isAuthenticated]);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    // Call the register action from the store
    register({ username, password, password2: confirmPassword });
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
          onSubmit={handleRegister}
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
          <Typography variant="subtitle2">Sign Up</Typography>
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
          <TextField
            label="Confirm Password"
            variant="outlined"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            sx={{ width: "100%" }}
            required
          />
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
            Sign Up
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
