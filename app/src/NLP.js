import * as React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { useRef } from 'react';
import "./NLP.css";

var rec = []
export default function NLP() {

  const [value, setValue] = React.useState("");
  
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
        rec = data;
        setValue(value + ' ');
      });
  };


  return (
    <div>
    <Box
      component="form"
      sx={{
        "& .MuiTextField-root": { m: 1, width: "40ch" },
      }}
      noValidate
      autoComplete="off"
    >
      <TextField
        className='superInput'
        label="Text prompt..."
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
    <div>
      <div>
        <ul>
            {rec.map(d => (        
            <li key={d.title} className="a_big_box">
              <div>
                  <div className="left_image"><img src={d.poster} width="400px" height="auto"></img></div>
                  <div className="right_info"><h2>{d.title} ({d.year})</h2></div>
                  <div className="prompts">{d.plot}</div>
              </div>
            </li>
            ))
            } 

        </ul>
      </div>
    </div>
    </div>
    
  );
}
