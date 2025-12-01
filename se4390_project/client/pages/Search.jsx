import React, { useState } from "react";

function Search() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const fetchSearch = async () => {
    setError("");
    setResult(null);
    try {
      const res = await fetch(
        `http://127.0.0.1:8080/api/search?query=${query}`
      );
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError("Failed to fetch search results.");
    }
  };

  return (
    <div>
      <h2>Search</h2>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value.toUpperCase())}
        placeholder="Enter ticker (e.g. AAPL)"
      />
      <button onClick={fetchSearch}>Search</button>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}

export default Search;
