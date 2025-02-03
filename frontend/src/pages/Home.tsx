import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">
          Welcome to Just do IT
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          A collaborative forum for IT enthusiasts to share knowledge and help each other
        </p>
        <div className="space-x-4">
          <Link
            to="/register"
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 inline-block"
          >
            Get Started
          </Link>
          <Link
            to="/posts"
            className="bg-gray-100 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-200 inline-block"
          >
            Browse Posts
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <div className="text-center p-6 bg-white rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Share Knowledge</h3>
          <p className="text-gray-600">
            Create posts to share your experiences and insights with the community
          </p>
        </div>
        <div className="text-center p-6 bg-white rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Get Help</h3>
          <p className="text-gray-600">
            Ask questions and get help from experienced developers
          </p>
        </div>
        <div className="text-center p-6 bg-white rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Grow Together</h3>
          <p className="text-gray-600">
            Join discussions and help others while improving your skills
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home; 