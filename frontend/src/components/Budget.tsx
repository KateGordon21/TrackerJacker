import { Box } from "@mui/material";
import theme from "../theme";

export default function Budget() {
  return (
    <>
      <Box
        sx={{
          background: theme.palette.secondary.dark,
          height: "500px",
          width: "500px",
          borderRadius: "10px",
          mt: 10,
        }}
      ></Box>
    </>
  );
}
