import React, { useRef, useState } from 'react'

function Upload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [message, setMessage] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Trigger the hidden file input when the custom button is clicked
  const handleChooseFile = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  // Update state when a file is chosen
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0])
    }
  }

  // Upload file to backend
  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first!')
      return
    }

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      setMessage(`Upload successful: ${JSON.stringify(data)}`)
    } catch (error) {
      console.error('Error uploading file:', error)
      setMessage('Error uploading file. Please try again.')
    }
  }

  return (
    <div className="container text-center py-5">
      <h2>Upload Files</h2>

      {/* Hidden file input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />

      {/* Custom "Select File" button using Bootstrap styling */}
      <div className="d-flex gap-2 justify-content-center py-3">
        <button className="btn btn-primary rounded-pill px-3" type="button" onClick={handleChooseFile}>
          Select File
        </button>
        <button className="btn btn-success rounded-pill px-3" type="button" onClick={handleUpload}>
          Upload
        </button>
      </div>

      {/* Display the selected file name if available */}
      {selectedFile && <p>Selected file: {selectedFile.name}</p>}

      {/* Message area */}
      {message && <p className="mt-3">{message}</p>}
    </div>
  )
}

export default Upload
