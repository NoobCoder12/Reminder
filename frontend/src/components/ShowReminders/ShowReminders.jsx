import "./ShowReminders.css"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom";

function ShowReminders () {
    const navigate = useNavigate();
    const [reminders, setReminders] = useState([]);
    const [message, setMessage] = useState("");
    const [openMenuId, setOpenMenuId] = useState(null);

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
                <div className="header">
                    <h2>{r.title}</h2>
                    <div className="actions">
                        <button onClick={() => setOpenMenuId(openMenuId === r.id ? null : r.id)}>...</button>   {/*if false r.id will be assigned to openMenuId*/}
                    {openMenuId  === r.id && (
                        <ul className="dropdown">
                            <li onClick={() => navigate(`/reminders/${r.id}/edit`)}>Edit</li>
                            <li>Delete</li>
                        </ul>
                        )}
                    </div>
                </div>
                <p>{r.description}</p>
                <p>{String(openMenuId)}</p>
                <p>Must be done until: {r.due_to}</p>
            </div>
        ))}
    </div>
   )
};

export default ShowReminders