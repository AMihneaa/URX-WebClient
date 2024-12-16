import React from 'react';

const data = {
    position: [0.600525622392412, -0.23278915712382445, -0.3322044984512897, -0.04176787055215222, -3.138968824031173, -0.010858511312736064],
  };
  
sendPositionData = async (data) => {
    try {
        console.log(data.position);  
        const response = await fetch('http://127.0.0.1:8000/robot/movePosition/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        const responseData = await response.json();
        console.log(responseData);
    } catch (error) {
        console.error('Error:', error);``
    }
  }
const MoveRobot = () => {
    // Your component logic goes here

    return (
        <div>
            <button onClick={() => sendPositionData(data)}>Move Robot</button>
        </div>
    );
};

export default MoveRobot;