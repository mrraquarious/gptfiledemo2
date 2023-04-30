import React from 'react';
import FileUploader from './FileUploader';
import Chatbox from './Chatbox';
import './App.css';

function App() {
  return (
    <div style={{ display: 'flex' }}>
      <FileUploader />
      <Chatbox />
    </div>
  );
}

export default App;
