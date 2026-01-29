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
        due_to:"",
        email:"",
        alert_type:""
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

    function formatDateForFrontend(fetchedDate) {
        if (!fetchedDate) return "";

        if (fetchedDate.includes("T")) {
            return fetchedDate; // if formatted already returns with no changes
        }

        const [dateInfo, time] = fetchedDate.split(" ");
        const [day, month, year] = dateInfo.split('-');


        return `${year}-${month}-${day}T${time}`
    }

    function formatDateForBackend(inputDate) {
        if (!inputDate) return "";


        if (!inputDate.includes("T")) {
            return inputDate        // With no changes date is returned as-is
        }
        
        const localDate = new Date(inputDate);


        const year = localDate.getUTCFullYear();
        const month = String(localDate.getUTCMonth() + 1).padStart(2, "0"); // Transforming into 2 character number with 0 at the begining
        const day = String(localDate.getUTCDate()).padStart(2, "0");
        const hours = String(localDate.getUTCHours()).padStart(2, "0"); // Gets valid hour in UTC format for backend
        const minutes = String(localDate.getUTCMinutes()).padStart(2, "0");

        return `${day}-${month}-${year} ${hours}:${minutes}`
    }

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
                body: JSON.stringify({
                    ...reminder, // Without spread operator object might be deleted
                    due_to: formatDateForBackend(reminder.due_to)
                })
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

                <input type='email' name="email" placeholder='Email' value={reminder.email} onChange={handleChange}/> 

                <input type="datetime-local" name="due_to" value={formatDateForFrontend(reminder.due_to)} onChange={handleChange}/>

                <select name="alert_type" value={reminder.alert_type} onChange={handleChange}>
                    <option value="minutes">15 minutes</option>
                    <option value="hours">1 hour</option>
                    <option value="days">1 day</option>
                </select>

                <button type="submit">Save</button>
            </form>
        </div>
    );
}

export default GetReminder;
