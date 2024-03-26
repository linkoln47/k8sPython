
import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    (async () => {
      const response = await fetch(
        "http://localhost:5000/"
      );
      const parsed = await response.json();
      setData(parsed);
    })();
  }, []);

  return (
    <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            <pre>{JSON.stringify(data)}</pre> 
          </p> 
          <a className="App-link" href="https://reactjs.org" target="_blank" rel="noopener noreferrer" > Learn React </a> 
        </header> 
    </div>
  );
}

export default App