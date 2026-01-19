import { useState, useEffect } from "react";
import "./App.css";
import Welcome from "./Welcome"

function App () {
  const [message, setMessage] = useState('');

  useEffect (() => {
    fetch("http://localhost:8000/")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => console.error(err))
  }, []);

  return (
    <div>
      <Welcome />
      <p>Message from backend: {message}</p>
    </div>
  )
  };

export default App;

