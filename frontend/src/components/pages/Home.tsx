import { Button, Container, Typography } from "@mui/material";
import logo from "../../assets/logo.png";

import { APP_NAME } from "../../config";
import Budget from "../Budget";
import useAuthStore from "../../store/authStore";

export default function Home() {
  const { user, isAuthenticated, logout, setError } = useAuthStore();

  console.log(user);
  return (
    <>
      <Container>
        hello
        {user?.id || "no"}
        {user?.username || "no"}
        {isAuthenticated && <Container>Authenticated</Container>}
      </Container>
      <Button onClick={logout}>Logout</Button>
      <Button onClick={() => setError(null)}>Clear error</Button>
    </>
  );
}
