import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App.jsx';
import Dashboard from './components/Dashboard.jsx';
import HomePage from './components/Home.jsx';
import { SharedProvider } from './sharedContext.jsx';
import InputForm from './components/InputForm.jsx';
import { useSharedContext } from './sharedContext.jsx';
import { useParams } from 'react-router-dom';
import Catalogue from './components/Catalogue.jsx';


const router = createBrowserRouter(
  [
  {
    path: "/",
    element: <HomePage />
  },
  {
    path:"/input-form",
    element:<InputForm />
  },
  {
    path: `/dashboard/:id`,
    element: <Dashboard />
  },
  {
    path: `/catalogue`,
    element: <Catalogue />
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SharedProvider>
      <RouterProvider router={router} />
    </SharedProvider>
  </StrictMode>
);
