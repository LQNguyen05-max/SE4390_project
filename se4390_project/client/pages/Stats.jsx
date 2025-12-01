import React, { useState } from "react";

function Stats() {
  const [ticker, setTicker] = useState("");
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  const fetchStats = async () => {
    setError("");
    setStats(null);
    if (!ticker) {
      setError("Please enter a ticker symbol...");
      return;
    }
    try {
      const res = await fetch(`http://127.0.0.1:8080/api/stats/${ticker}`);
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setStats(data);
      }
    } catch (err) {
      setError("Failed to fetch stats.");
    }
  };

  return (
    <div>
      <h2>Stock Stats</h2>
      <input
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase())}
        placeholder="Enter ticker (e.g. AAPL)"
      />
      <button onClick={fetchStats}>Get Stats</button>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {stats && <pre>{JSON.stringify(stats, null, 2)}</pre>}
    </div>
  );
}

export default Stats;
