import { Routes, Route, NavLink } from 'react-router-dom'
import Home from './home'
import Upload from './upload'
import Results from './Results'

function App() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Updated Navigation Bar using Bootstrap classes */}
      <nav className="navbar navbar-expand-lg navbar-dark" style={{ backgroundColor: '#1b263b' }}>
        <div className="container-fluid">
          <NavLink className="navbar-brand" to="/">Traffic Analyzer</NavLink>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse justify-content-center" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <NavLink className="nav-link" to="/">Home</NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/upload">Upload</NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/results">Results</NavLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Main content area */}
      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
