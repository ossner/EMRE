import * as React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { useRef } from 'react';


export default function NLP() {
  const [value, setValue] = React.useState("Controlled");
  
  const handleClick = event => {
    var text = value;
    fetch("/semantic", {
      method: 'POST',
      headers: {
        "content_type": "application/json"
      },
      body: JSON.stringify( { "sentence": text } )})
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
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
        label="Email (Controlled)"
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
        }} />
      <div>
      <Button
          variant="outlined"
          onClick={handleClick}
        >Submit</Button>
      </div>
    </Box>
  );
}
