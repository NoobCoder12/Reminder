import './Create.css';
import { useState} from "react";
import { useNavigate } from 'react-router-dom';


function Create () {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [dueTo, setDueTo] = useState("");
    const [message, setMessage] = useState("");
    const [email, setEmail] = useState("");
    const [alertType, setAlertType] = useState("minutes");
    const navigate = useNavigate();



    const handleCreate = async (e) => {
        e.preventDefault()
        try {

            const res = await fetch("http://localhost:8000/create", {
                method: "POST",
                headers: { "Content-Type" : "application/json"},
                body: JSON.stringify({
                    title,
                    description,
                    due_to: formatDateToUTC(dueTo),
                    email,
                    alert_type: alertType,
                }),
            });

            if (!res.ok) throw new Error("Failed to create reminder"); //Stops function and created new Error object

            const data = await res.json()

            setMessage(`Reminder created: ${data.title}`);  //With no error data would have 'title' attr

            alert("Reminder created succesfully");
            navigate("/reminders");
            
        } catch (err) {
            console.error("Fetch error: ", err)
            setMessage("Error creating reminder");
            }
        }

    function formatDateToUTC(dueTo) {
                if (!dueTo) {
                    return ""
                }
                
                
                const localDate = new Date(dueTo);


                const year = localDate.getUTCFullYear();
                const month = String(localDate.getUTCMonth() + 1).padStart(2, "0"); // Transforming into 2 character number with 0 at the begining
                const day = String(localDate.getUTCDate()).padStart(2, "0");
                const hours = String(localDate.getUTCHours()).padStart(2, "0");
                const minutes = String(localDate.getUTCMinutes()).padStart(2, "0");

                return `${day}-${month}-${year} ${hours}:${minutes}`
            };

    return (
        <div className='create'>
            <h1>Create Reminder</h1>

            <form className="createForm" onSubmit={handleCreate}>

                <input type='text' placeholder='Title' value={title} onChange={(e) => setTitle(e.target.value)}/>   {/*'value' is a value of hook value*/}

                <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)}/>  {/*Event is automatically passed as function argument by default*/}

                <input type='email' placeholder='Email' value={email} onChange={(e) => setEmail(e.target.value)}/> 
                
                <input type="datetime-local" placeholder='Due to' value={dueTo} onChange={(e) => setDueTo(e.target.value)}/>

                <select value={alertType} onChange={(e) => setAlertType(e.target.value)}>
                    <option value="minutes">15 minutes</option>
                    <option value="hours">1 hour</option>
                    <option value="days">1 day</option>
                </select>

                <button type='submit'>Create</button>

            </form>

            {message && <p>{message}</p>}
        </div>
    );
}

export default Create
