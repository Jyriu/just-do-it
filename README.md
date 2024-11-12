# Just do IT: A Collaborative Forum for IT Enthusiasts

Welcome to **Just do IT**, a collaborative forum project aimed at the IT community. This project is currently under development and aims to create a platform where users can share posts, ask for help, exchange advice, and participate in discussions related to various IT topics.

## Current Features
Here is a list of features that have already been implemented or are under development:

- **User Registration and Login**: Each user can create an account, log in, and receive a JWT token for authentication.
- **Post Creation**: Users can create posts to ask for help, share advice, or start discussions on specific topics.
- **Reply to Posts**: Users can reply to posts and engage in discussions.
- **Post Pagination**: Posts are displayed with a pagination system for better navigation.
- **Like System (in progress)**: Users will be able to like posts and replies to indicate their relevance and popularity.
- **Statistics and Gamification**: A points and leaderboard system is planned to encourage engagement and quality contributions.

## Technologies Used
- **Backend**: Flask (Python) with SQLAlchemy for database management.
- **Database**: PostgreSQL, using **Flask-Migrate** to manage schema migrations.
- **Authentication**: JWT (JSON Web Tokens) to handle user authentication and security.
- **Frontend**: In preparation, the project will likely use **React** for a dynamic user interface.

## Installation and Setup
If you wish to contribute or test this project locally, here’s how you can set it up on your machine.

### Prerequisites
- **Python 3.8+**
- **PostgreSQL** (configured with a database named `just_do_it_db`)
- **Node.js** (if the frontend is under development)

### Installation
1. Clone the project:
   ```sh
   git clone https://github.com/your-username/just-do-it.git
   cd just-do-it/backend
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate # On MacOS/Linux
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file at the root of the backend project with the sensitive information (e.g., database connection string):
   ```env
   DATABASE_URL=postgresql://username:password@localhost/just_do_it_db
   JWT_SECRET_KEY=your-secret-key
   ```

5. Initialize the database:
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. Run the application:
   ```sh
   python app.py
   ```
   The application should be accessible at `http://127.0.0.1:5000`.

## Contribution
For now, this is a personal project aimed at learning and practice, but if the MVP is deployed and users are interested, contributions will be welcome! Here’s how you can contribute:

- **Report Bugs**: Open an issue on GitHub.
- **Suggest New Features**: Discuss an idea or make a suggestion by opening an issue.
- **Submit a Pull Request**: For new features or bug fixes.

Please read the `CONTRIBUTING.md` file (in preparation) before submitting contributions.

## Future Plans
Here are some of the features planned for future development:
- **Notification System**: To notify users of replies or likes.
- **Full Gamification**: Leaderboard, levels, and badges to enhance the forum experience.
- **Dynamic Front-End**: Likely using **React** for the user interface.

## Author
This project is developed by [your name]. For any questions, feel free to contact me on [your email or GitHub].

## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.

