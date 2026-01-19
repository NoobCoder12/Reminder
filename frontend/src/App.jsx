import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Welcome from "./Welcome"

function App () {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />}/>
      </Routes>
    </Router>
  )
  };

export default App;

