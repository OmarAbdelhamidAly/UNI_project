<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smart Access and Medical System for Hospitals</title>
</head>
<body>
  <h1>Smart Access and Medical System for Hospitals</h1>
  <p>This project implements a <strong>Smart Access Control and Medical Consultation System</strong> for hospital environments. With seamless integration of face recognition for secure access and an AI-driven medical module for cancer diagnosis, the system provides both security and medical support through an intelligent, user-friendly interface.</p>

  <hr>

  <h2>Features</h2>
  
  <h3>1. Smart Access Control System</h3>
  <p>Enhanced security with advanced face recognition authentication:</p>
  <ul>
    <li><strong>Face-Based Registration & Authentication:</strong> Utilizes face recognition for user registration and login, ensuring secure access control.</li>
    <li><strong>Secure Database Integration:</strong> Employs SQLite for storing user profiles and facial data securely.</li>
    <li><strong>Session Management:</strong> Provides session-based access with secure redirects to designated hospital modules.</li>
  </ul>

  <h3>2. AI-Powered Medical Consultation System</h3>
  <p>The medical consultation module assists in cancer diagnosis with AI capabilities specialized in:</p>
  <ul>
    <li>Lung Cancer</li>
    <li>Brain Cancer</li>
    <li>Chest Cancer</li>
    <li>Colon Cancer</li>
    <li>Bone Marrow Cancer</li>
  </ul>
  <p>Key features include:</p>
  <ul>
    <li><strong>Customizable AI Medical Expert:</strong> Built using LangChain and fine-tuned LLMs, trained on the latest cancer research papers.</li>
    <li><strong>Research-Based Answering System:</strong> Uses FAISS for efficient storage and retrieval of indexed research embeddings, ensuring accurate and up-to-date responses.</li>
    <li><strong>Intuitive Chat Interface:</strong> Patients can interact directly with the AI medical expert, receiving real-time answers for diagnosis and treatment information.</li>
  </ul>

  <hr>

  <h2>Technical Stack</h2>
  <ul>
    <li><strong>Backend:</strong> Flask for server-side logic and routing, SQLite for persistent storage.</li>
    <li><strong>Face Recognition:</strong> OpenCV and DeepFace libraries for accurate image-based user authentication.</li>
    <li><strong>AI Medical Assistant:</strong> LangChain with Llama models for language-based medical support.</li>
    <li><strong>Storage and Retrieval:</strong> FAISS for efficient similarity search on cancer research data.</li>
  </ul>

  <h2>Installation and Setup</h2>
  
  <h3>1. Clone the Repository</h3>
  <pre><code>git clone https://github.com/yourusername/smart-access-medical-system.git
cd smart-access-medical-system
</code></pre>

  <h3>2. Install Dependencies</h3>
  <pre><code>pip install -r requirements.txt</code></pre>

  <h3>3. Configure Environment Variables</h3>
  <p>Create a <code>.env</code> file with necessary API keys and database configurations:</p>
  <ul>
    <li><code>GROQ_API_KEY</code>: API key for Groq service if used in cancer research retrieval.</li>
  </ul>

  <h3>4. Initialize the Database</h3>
  <pre><code>python init_db.py</code></pre>

  <h3>5. Run the Application</h3>
  <pre><code>flask run</code></pre>
  <p>The app will start on <code>http://localhost:5000</code> by default.</p>

  <hr>

  <h2>Docker Setup</h2>
  <p>To deploy using Docker, follow these steps:</p>

  <h3>1. Pull Docker Image</h3>
  <p>Download the pre-built Docker image from DockerHub:</p>
  <pre><code>docker pull omarabdelhamid/goofy_darwin:latest</code></pre>

  <h3>2. Run the Docker Container</h3>
  <p>Start the container with the following command:</p>
  <pre><code>docker run -p 5000:5000 omarabdelhamid/goofy_darwin:latest</code></pre>

  <p>This will launch the app on port 5000, making it accessible at <code>http://localhost:5000</code>.</p>

  <hr>

  <h2>Usage</h2>
  
  <h3>Sign-Up Process</h3>
  <ul>
    <li>Users upload a face image for registration.</li>
    <li>The image is processed and saved securely in the database.</li>
  </ul>

  <h3>Sign-In and Access</h3>
  <ul>
    <li>Users authenticate via face recognition, gaining access to their dashboard upon successful login.</li>
    <li>The dashboard provides options for various medical consultation modules.</li>
  </ul>

  <h3>Medical Consultation</h3>
  <ul>
    <li>Patients can enter queries related to cancer symptoms, diagnosis, or treatment.</li>
    <li>The AI assistant uses LLMs and FAISS to retrieve relevant and research-backed responses.</li>
  </ul>

  <hr>

  <h2>Project Structure</h2>
  <ul>
    <li><code>FaceRecognitionModel.py</code>: Handles routes for registration, authentication, and face recognition functions.</li>
    <li><code>models.py</code>: SQLAlchemy models for storing user and medical record data.</li>
    <li><code>app.py</code>: Main app controller, manages routing for access control and medical consultation.</li>
    <li><code>chatapp.py</code>: Contains the AI-driven medical assistant logic for cancer consultation.</li>
    <li><code>config.py</code>: Configurations and environment settings.</li>
  </ul>

  <hr>

  <h2>Contributing</h2>
  <p>We welcome contributions to improve the system further. To contribute:</p>
  <ol>
    <li>Fork the repository.</li>
    <li>Create a feature branch (<code>git checkout -b feature-branch</code>).</li>
    <li>Commit your changes (<code>git commit -m "Added new feature"</code>).</li>
    <li>Push to the branch (<code>git push origin feature-branch</code>).</li>
    <li>Open a Pull Request.</li>
  </ol>

  <h2>License</h2>
  <p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.</p>

  <hr>

  <h2>Contact</h2>
  <p>For questions or suggestions, please reach out via the GitHub repository or email us at <a href="mailto:support@example.com">support@example.com</a>.</p>

</body>
</html>
