import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Welcome from "./components/Welcome/Welcome.jsx"
import Choose from "./components/Choose/Choose.jsx"
import Create from "./components/Create/Create.jsx"
import ShowReminders from "./components/ShowReminders/ShowReminders.jsx"
import EditReminder from "./components/EditReminder/EditReminder.jsx";

function App () {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />}/>
        <Route path="/choose" element={<Choose />}/>
        <Route path="/create" element={<Create />}/>
        <Route path="/reminders" element={<ShowReminders />}/>
        <Route path="/reminders/:id/edit" element={<EditReminder />}/> 
      </Routes>
    </Router>
  )
  };

export default App;

