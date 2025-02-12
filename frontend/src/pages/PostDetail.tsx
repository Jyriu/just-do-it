import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Post } from '../types';
import api from '../services/api';

const PostDetail = () => {
  const { id } = useParams();
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await api.get(`/posts/${id}`);
        setPost(response.data);
      } catch (err: any) {
        setError(err.response?.data?.message || 'Une erreur est survenue');
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [id]);

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

  if (!post) {
    return (
      <div className="text-center py-8">
        <h2 className="text-2xl font-bold">Post non trouvé</h2>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <article className="bg-white p-6 rounded-lg shadow mb-8">
        <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
        <div className="text-gray-600 mb-4">
          Par {post.author.username} • {new Date(post.createdAt).toLocaleDateString()}
        </div>
        <p className="text-gray-800 mb-6 whitespace-pre-wrap">{post.content}</p>
        <div className="flex items-center text-sm text-gray-500">
          <span className="mr-4">{post.views_count} vues</span>
          <span className="mr-4">{post.likes_count} likes</span>
          <span>{post.replies.total} réponses</span>
        </div>
      </article>

      <section className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Réponses</h2>
        {post.replies.items.map((reply) => (
          <div key={reply.id} className="bg-white p-4 rounded-lg shadow mb-4">
            <div className="flex justify-between items-start mb-2">
              <span className="font-medium">{reply.author.username}</span>
              <span className="text-sm text-gray-500">
                {new Date(reply.createdAt).toLocaleDateString()}
              </span>
            </div>
            <p className="text-gray-800">{reply.content}</p>
            <div className="mt-2 text-sm text-gray-500">
              {reply.likes_count} likes
            </div>
          </div>
        ))}
      </section>
    </div>
  );
};

export default PostDetail;