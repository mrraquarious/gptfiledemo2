import React from 'react';

function FileUploader() {
  const handleChange = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    console.log(result);
  };

  return (
    <div>
      <h1>Upload your file</h1>
      <input type="file" onChange={handleChange} />
    </div>
  );
}

export default FileUploader;
