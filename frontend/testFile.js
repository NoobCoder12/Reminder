try {
        const res = await fetch("http://localhost:8000/reminders");

        if (!res.ok) throw new Error("Error fetching reminders");

        const data = await res.json();

        console.log(data)

        } catch(err) {
            console.error(err);
            setMessage("Error fetching data");
        };