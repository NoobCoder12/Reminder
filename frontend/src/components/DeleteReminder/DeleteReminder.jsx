import { useState } from "react";
import { useParams } from "react-router-dom";

function DeleteReminder () {
    const { id } = useParams();
    const reminderID = parseInt(id);

    const [ reminder, setReminder ] = useState({
        title: "",
        description: "",
        due_to:""
    });

    const [ loading, setLoading ] = useState(true);
    const [ error, setError ] = useState("");

    useEffect (() => {
        const fetchReminder = async () => {
            try{
                const res = await fetch(`http://localhost:8000/reminders/${reminderID}`);

                if (!res.ok) throw new Error("Fetching failed");

                const data = await res.json()

                setReminder(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchReminder();
    }, [id]);


    const deleteReminder = async () => {
        try {
            const res = await fetch(`http://localhost:8000/reminders/${reminderID}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(reminder)
            });

            if (!res.ok) throw new Error("Reminder was not deleted")

            alert("Reminder deleted successfully");

            Navigate("/reminders")
        } catch(err) {
            setError(err.message)
        }
    };

    if (loading) return <p>Loading...</p>
    if (error) return <p>{error}</p>

    
}