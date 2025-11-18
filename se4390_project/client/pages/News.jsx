import React from "react";
import { useParams } from "react-router-dom";

// Content is Dynamic HTML

function News() {
  const { ticker } = useParams();
  return <div>News for: {ticker} </div>;
}

export default News;
