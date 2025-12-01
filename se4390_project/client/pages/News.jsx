import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function News() {
  const { ticker } = useParams();
  const [news, setNews] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ticker) return;
    const fetchNews = async () => {
      setError("");
      setNews([]);
      try {
        const res = await fetch(`http://127.0.0.1:8080/api/news/${ticker}`);
        const data = await res.json();
        if (data.error) {
          setError(data.error);
        } else {
          setNews(data.news || []);
        }
      } catch (err) {
        setError("Failed to fetch news.");
      }
    };
    fetchNews();
  }, [ticker]);

  useEffect(() => {
    console.log("News data for", ticker, ":", news);
  }, [news]);

  return (
    <div>
      <h2>News for: {ticker}</h2>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {news.length === 0 && !error && <div>No news found.</div>}
      <ul>
        {news.map((item, idx) =>
          item && item.title ? (
            <li key={idx}>
              <a href={item.link} target="_blank" rel="noopener noreferrer">
                {item.title}
              </a>
            </li>
          ) : (
            <li key={idx}>No headline</li>
          )
        )}
      </ul>
    </div>
  );
}

export default News;
