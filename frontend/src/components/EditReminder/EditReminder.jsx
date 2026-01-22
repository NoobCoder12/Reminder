import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "./EditReminder.css"

function GetReminder() {
    const { id } = useParams(); // useParams extracts data from link to use it in code
    const reminderID = parseInt(id);

    const navigate = useNavigate();
    const [reminder, setReminder ] = useState({
        title: "",
        description: "",
        due_to:""
    }); // Could be done simpler but more if blocks would appear

    const [ loading, setLoading ] = useState(true);
    const [ error, setError ] = useState("")

    useEffect(() => {
        const fetchReminder = async () => {
            try {
                const res = await fetch(`http://localhost:8000/reminders/${reminderID}`)

                if (!res.ok) throw new Error("Error fetching data");

                const data = await res.json();

                setReminder(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchReminder();
    }, [id]); // Will be executed when ID changes

    const handleChange = (e) => {       // React automatically shares event as parameter for event function
        const { name, value } = e.target;  // Gets name and value from input
        setReminder((prev) => ({ ...prev, [name]: value }));  //Sets value of Reminder, prev is an old object, ...prev copies remaining data from it
    };

    const handleSave = async (e) => {
        e.preventDefault();  // Page won't refresh after submitting

        try {
            const res = await fetch(`http://localhost:8000/reminders/${reminderID}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(reminder)
            });

            if (!res.ok) throw new Error("Update failed");

            alert("Reminder updated!");

            navigate("/reminders");
        } catch(err) {
            setError(err.message)
        }
    };

    if (loading) return <p>Loading...</p>
    if (error) return <p>{error}</p>

    return (
        <div className="editDiv">
            <h1>Edit reminder</h1>
            <form className="editForm" onSubmit={handleSave}>
                <input type="text" name="title" value={reminder.title} onChange={handleChange} placeholder="Title"/>

                <textarea name="description" value={reminder.description} onChange={handleChange} placeholder="Description"/>

                <input type="date" name="due_to" value={reminder.due_to} onChange={handleChange}/>

                <button type="submit">Save</button>
            </form>
        </div>
    );
}

export default GetReminder;
