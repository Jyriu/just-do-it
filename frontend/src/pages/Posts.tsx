import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Post } from '../types';

const Posts = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await api.get('/posts');
        setPosts(response.data.posts);
      } catch (err: any) {
        setError(err.response?.data?.message || 'Une erreur est survenue');
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-xl">Chargement...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Posts récents</h2>
        <Link
          to="/create-post"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Nouveau post
        </Link>
      </div>

      <div className="space-y-6">
        {posts.map((post) => (
          <div key={post.id} className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
            <Link to={`/posts/${post.id}`} className="block">
              <h3 className="text-xl font-semibold mb-2 text-gray-900 hover:text-blue-600 transition-colors">
                {post.title}
              </h3>
              <p className="text-gray-600 mb-4 line-clamp-2">{post.content}</p>
              <div className="flex justify-between items-center text-sm text-gray-500">
                <div className="flex items-center space-x-4">
                  <span>Par {post.author.username}</span>
                  <span>•</span>
                  <span>{new Date(post.createdAt).toLocaleDateString()}</span>
                </div>
                <div className="flex items-center space-x-4">
                  <span>{post.views_count} vues</span>
                  <span>{post.likes_count} likes</span>
                  <span>{post.replies.total} réponses</span>
                </div>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Posts;