import { ReactNode } from 'react'
import Navbar from './Navbar'

interface LayoutProps {
  children: ReactNode
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div>
      <h1>⚙️ DevOps Toolkit</h1>
      <Navbar />
      <main>{children}</main>
    </div>
  )
}

export default Layout
