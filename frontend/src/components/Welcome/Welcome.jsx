import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import './Welcome.css'

function Welcome () {

    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    
      useEffect (() => {
        fetch("http://localhost:8000/")
          .then((res) => res.json())
          .then((data) => setMessage(data.message))
          .catch((err) => console.error(err))
      }, []);


    return (
        <div className='welcome'>
            <h1>Welcome to Reminder</h1>
            <p className="welcomeInfo">This app will not let you forget anything!</p>
            <button onClick={() => navigate("/choose")}>LET'S START</button>
            {/* <p className="appInfo">Message from backend: {message}</p> */}
        </div>
    )
}

export default Welcome