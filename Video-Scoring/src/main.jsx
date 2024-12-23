import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App.jsx';
import Dashboard from './components/Dashboard.jsx';
import HomePage from './components/Home.jsx';
import { SharedProvider } from './sharedContext.jsx';

const router = createBrowserRouter([
  {
    path: "",
    element: <HomePage />
  },
  {
    path: "/dashboard",
    element: <Dashboard />
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SharedProvider>
      <RouterProvider router={router} />
    </SharedProvider>
  </StrictMode>
);
