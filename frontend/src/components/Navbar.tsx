import { NavLink } from 'react-router-dom'

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul>
        <li>
          <NavLink 
            to="/code-review" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            🔍 Code Review
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/pipeline-tuner" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            🚀 Pipeline Tuner
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/test-genie" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            🧪 Test Genie
          </NavLink>
        </li>
      </ul>
    </nav>
  )
}

export default Navbar
