import React, { useState, useEffect } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";

var rec = {};

export default function Tinder() {
  const [recommendation, setRecommendation] = useState(0);
  useEffect(() => {
    fetch("/init")
      .then((res) => res.json())
      .then((data) => {
        setRecommendation(recommendation + 1);
        rec = data;
        rec.posters = data.posters[0];
      });
  }, []);

  return (
    <div>
      <div>
        <img src={rec.posters} width="auto" height="600px"></img>
        <p></p>
        {rec.title} ({rec.year})<p></p>
      </div>
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="center"
        spacing={2}
      >
        <Button
          variant="outlined"
          onClick={() => {
            fetch("/dislike")
              .then((res) => res.json())
              .then((data) => {
                setRecommendation(recommendation + 1);
                rec = data;
                rec.posters = data.posters[0];
                console.log(data)
              });
          }}
        >
          Dislike
        </Button>
        <Button
          variant="outlined"
          onClick={() => {
            fetch("/like")
              .then((res) => res.json())
              .then((data) => {
                setRecommendation(recommendation + 1);
                rec = data;
                rec.posters = data.posters[0];
                console.log(data)
              });
          }}
        >
          Like
        </Button>
      </Stack>
    </div>
  );
}
