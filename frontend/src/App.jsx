import './App.css';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import StatsCrudTable from './components/StatsTable';
import Home from './components/Home';
import RegisterForm from './components/AddStatsForm';

function App() {
  return (
    <BrowserRouter>
      {/* NAVBAR */}
      <div className="navbar">
        <Link to='/'>
          Home
        </Link>
        <Link to='/add-stats'>
          Add Stats
        </Link>
        <Link to='/stats-table'>
          Stats Table
        </Link>
      </div>
      {/* ROUTES */}
      <Routes>
        <Route
          index // equivalent to path=""
          element={<Home/>}
        />
        <Route
          path="add-stats"
          element={<RegisterForm/>}
        />
        <Route
          path="stats-table" // path = '/' + 'stats-table'
          element={<StatsCrudTable/>}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
