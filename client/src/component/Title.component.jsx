import React, { useEffect, useState } from 'react';

const Title = ({ text }) => {
    const [backendData, setBackendData] = useState({ message: "Nu s-a primit nimic" });

    const fetchData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/test/'); // Înlocuiți cu URL-ul corect
            const data = await response.json();
            setBackendData(data);
        } catch (error) {
            console.error('Eroare la apelul backend:', error);
        }
    };

    return (
        <div>
            <h1>{text}</h1>
            <p>{backendData.message}</p>
            <button onClick={fetchData}>Încarcă date de la backend</button>
        </div>
    );
};

export default Title;