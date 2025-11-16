import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import News from "../pages/News";
import Search from "../pages/Search";
import Stats from "../pages/Stats";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/news/:ticker" element={<News />} />
          <Route path="/search" element={<Search />} />
          <Route path="/stats" element={<Stats />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
