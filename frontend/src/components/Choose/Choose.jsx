import './Choose.css';
import { useNavigate } from "react-router-dom";

function Choose () {

    const navigate = useNavigate();
    
    return (
        <div className='choose'>
            <h1 className='chooseTitle'>What would you like to do?</h1>
            <button className="chooseButtonFirst" onClick={() => navigate("/create")}>Create reminder</button>
            <button className="chooseButtonSecond" onClick={() => navigate("/reminders")}>See my reminders</button>
        </div>
    )
}

export default Choose