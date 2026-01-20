import "./ShowReminders.css"
import { useEffect, useState } from "react"

function ShowReminders () {

    const [reminders, setReminders] = useState([])
    const [message, setMessage] = useState("");

    useEffect (() => {
        const fetchReminders = async () => { 
        try {
            const res = await fetch("http://localhost:8000/reminders");

            if (!res.ok) throw new Error("Error fetching reminders");

            const data = await res.json();
            setReminders(data);

        } catch(err) {
            console.error(err);
            setMessage("Error fetching data");
        };
    };
    
    fetchReminders()
    }, []);

   return (
    <div className="reminders">

        {message && <p>{message}</p>}

        {reminders.map((r) =>(
            <div className="reminder" key={r.id}>
                <h3>{r.title}</h3>
                <p>{r.description}</p>
                <small>{r.due_to}</small>
            </div>
        ))}
    </div>
   )
};

export default ShowReminders