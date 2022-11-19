import * as React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

export default function NLP() {
  const [value, setValue] = React.useState("Controlled");

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  return (
    <Box
      component="form"
      sx={{
        "& .MuiTextField-root": { m: 1, width: "40ch" },
      }}
      noValidate
      autoComplete="off"
    >
      <TextField
        id="fullWidth"
        label="Text prompt"
        placeholder="A rabbit in the pursuit of happiness..."
        size="large"
        multiline
      />
      <div>
      <Button
          variant="outlined"
        >Submit</Button>
      </div>
    </Box>
  );
}
