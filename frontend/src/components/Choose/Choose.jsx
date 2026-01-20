import './Choose.css';
import { useNavigate } from "react-router-dom";

function Choose () {

    const navigate = useNavigate();
    
    return (
        <div className='choose'>
            <h1>What would you like to do?</h1>
            <button onClick={() => navigate("/create")}>Create reminder</button>
            <button onClick={() => navigate("/reminders")}>See my reminders</button>
        </div>
    )
}

export default Choose