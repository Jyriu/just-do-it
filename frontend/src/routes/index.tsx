import { createBrowserRouter, RouteObject } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Posts from '../pages/Posts';
import CreatePost from '../pages/CreatePost';

const routes: RouteObject[] = [
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: 'login',
        element: <Login />,
      },
      {
        path: 'register',
        element: <Register />,
      },
      {
        path: 'posts',
        element: <Posts />,
      },
      {
        path: 'create-post',
        element: <CreatePost />,
      },
    ],
  },
];

export const router = createBrowserRouter(routes); 