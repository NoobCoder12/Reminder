import './Create.css';
import { useState} from "react";


function Create () {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [dueTo, setDueTo] = useState("");
    const [message, setMessage] = useState("");



    const handleCreate = async () => {
        try {
            
            function formatDate (dueTo) {
                if (!dueTo) {
                    return ""
                }
                const [date, time] = dueTo.split("T")
                const [year, month, day] = date.split("-")

                return `${day}-${month}-${year} ${time}`
            };

            const res = await fetch("http://localhost:8000/create", {
                method: "POST",
                headers: { "Content-Type" : "application/json"},
                body: JSON.stringify({
                    title,
                    description,
                    due_to: formatDate(dueTo)
                }),
            });

            if (!res.ok) throw new Error("Failed to create reminder"); //Stops function and created new Error object

            const data = await res.json()

            setMessage(`Reminder created: ${data.title}`);  //With no error data would have 'title' attr
        } catch (err) {
            console.error("Fetch error: ", err)
            setMessage("Error creating reminder");
            }
        }

    return (
        <div className='create'>
            <h1>Create Reminder</h1>

            <input type='text' placeholder='Title' value={title} onChange={(e) => setTitle(e.target.value)}/>   {/*'value' is a value of hook value*/}

            <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)}/>  {/*Event is automatically passed as function argument by default*/}

            <input type="datetime-local" placeholder='Due to' value={dueTo} onChange={(e) => setDueTo(e.target.value)}/>

            <button onClick={handleCreate}>Create</button>

            {message && <p>{message}</p>}
        </div>
    );
}

export default Create
