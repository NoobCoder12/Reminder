import "./ShowReminders.css"
import { useEffect, useState, useRef } from "react"
import { useNavigate } from "react-router-dom";

function ShowReminders () {
    const navigate = useNavigate();
    const [reminders, setReminders] = useState([]);
    const [message, setMessage] = useState("");
    const [openMenuId, setOpenMenuId] = useState(null);

    useEffect (() => {
        document.addEventListener('mousedown', closeMenuOutside)

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

    return () => {
            document.removeEventListener('mousedown', closeMenuOutside); // Removes event listener before next page rendering
        }

    }, [openMenuId]);

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to delete this reminder?")) {
            return ;
        }

        try{
            const res = await fetch(`http://localhost:8000/reminders/${id}`, {
                method: "DELETE"
            });

            if (!res.ok) throw new Error("Deleting failed");
            
            setReminders(prev => prev.filter(r => r.id !== id));  // 'prev' is a safeguard to ensure the latest state is used
            alert("Reminder deleted successfully")

        } catch(err) {
            setMessage(err.message)
        }
    }

    const closeMenuOutside = (e) => {
        if(openMenuId && !e.target.closest(".dropdown") && !e.target.closest(".actions button")) { 
            setOpenMenuId(null)
        }
    }

   return (
    <div className="reminders">

        {message && <p>{message}</p>}

        {reminders.map((r, i) => (
            <div className="reminder" key={r.id} style = {{ opacity: 0, animation: `entry 0.8s ease-out ${i}s forwards`}}>
                <div className="header">
                    <h2>{r.title}</h2>
                    <div className="actions">
                        <button onClick={() => setOpenMenuId(openMenuId === r.id ? null : r.id)}>...</button>   {/*if false r.id will be assigned to openMenuId*/}
                    {openMenuId  === r.id && (
                        <ul className="dropdown">
                            <li onClick={() => navigate(`/reminders/${r.id}/edit`)}>Edit</li>
                            <li onClick={() => handleDelete(r.id)}>Delete</li>
                        </ul>
                        )}
                    </div>
                </div>
                <p>{r.description}</p>
                <p>{String(openMenuId)}</p>
                <p>Must be done until: {r.due_to}</p>s
            </div>
        ))}
    </div>
   )
};

export default ShowReminders