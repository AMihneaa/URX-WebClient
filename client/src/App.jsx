import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Title from './component/Title.component'
import MoveRobot from './component/MoveRobot.component'

function App() {

  return (
    <>
      <Title text="Hello from Vite!" />
      <Title text="text 2!" />
      <MoveRobot />
    </>
  )
}

export default App
