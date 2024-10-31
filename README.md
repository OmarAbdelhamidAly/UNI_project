<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smart Access and Medical System for Hospitals</title>
</head>
<body>
  <h1>Smart Access and Medical System for Hospitals</h1>
  <p>This project provides a <strong>comprehensive smart access control</strong> and <strong>medical consultation system</strong> for hospitals, leveraging face recognition and an AI-powered cancer consultation module. The system enhances security while offering expert medical support focused on cancer diagnosis and treatment.</p>

  <h2>Features</h2>
  <h3>1. Access Control System</h3>
  <p>Our system uses face recognition for user authentication and access control with the following components:</p>
  <ul>
    <li><strong>Face Signup and Sign-in:</strong> Users register and authenticate via face recognition using DeepFace.</li>
    <li><strong>Database Integration:</strong> User data and images are stored securely in SQLite.</li>
    <li><strong>Session Management:</strong> Secure session-based login redirects authenticated users to the hospital dashboard.</li>
  </ul>

  <h3>2. Medical Consultation System</h3>
  <p>The medical module provides AI-driven cancer diagnosis assistance, supporting five cancer types:</p>
  <ul>
    <li>Lung Cancer</li>
    <li>Brain Cancer</li>
    <li>Chest Cancer</li>
    <li>Colon Cancer</li>
    <li>Bone Marrow Cancer</li>
  </ul>
  <p>Features include:</p>
  <ul>
    <li><strong>Customized AI Doctor:</strong> A language model specialized in cancer, trained on research papers for accurate patient responses.</li>
    <li><strong>Embedded Database:</strong> Cancer research embeddings allow for precise and contextually relevant answers.</li>
    <li><strong>Chat Interface:</strong> An intuitive UI for patients to interact with the AI doctor, receive diagnoses, and explore treatment options.</li>
  </ul>

  <h2>Technical Stack</h2>
  <ul>
    <li><strong>Backend:</strong> Flask, SQLite, OpenCV, DeepFace, LangChain, FAISS</li>
    <li><strong>Face Recognition:</strong> OpenCV and DeepFace for authentication</li>
    <li><strong>Machine Learning:</strong> LangChain with Llama-based models for cancer expertise</li>
    <li><strong>Storage:</strong> FAISS for quick access to cancer research data</li>
  </ul>

  <h2>Installation</h2>
  <ol>
    <li><strong>Clone the Repository:</strong></li>
    <pre><code>git clone https://github.com/yourusername/smart-access-medical-system.git
cd smart-access-medical-system
</code></pre>

    <li><strong>Set Up the Environment:</strong></li>
    <pre><code>pip install -r requirements.txt</code></pre>

    <li><strong>Configure Database and Environment Variables:</strong></li>
    <ul>
      <li>Add a <code>.env</code> file with your <code>GROQ_API_KEY</code>.</li>
      <li>Initialize the SQLite database:</li>
    </ul>
    <pre><code>python init_db.py</code></pre>

    <li><strong>Run the Application:</strong></li>
    <pre><code>flask run</code></pre>
  </ol>

  <h2>Using Docker</h2>
  <p>To pull and run the Docker image, use the following commands:</p>
  <pre><code>docker pull omarabdelhamid/goofy_darwin:latest
docker run -p 5000:5000 omarabdelhamid/goofy_darwin:latest
</code></pre>

  <h2>Usage</h2>
  <ul>
    <li><strong>Sign Up:</strong> Upload a base64-encoded image to register your profile.</li>
    <li><strong>Sign In:</strong> Authenticate using facial recognition and access the main dashboard.</li>
    <li><strong>Medical Consultation:</strong> Enter queries regarding cancer diagnosis and treatment through the chat interface.</li>
  </ul>

  <h2>Project Structure</h2>
  <ul>
    <li><code>FaceRecognitionModel.py</code>: Contains routes and functions for user authentication (signup/signin).</li>
    <li><code>models.py</code>: Defines SQLAlchemy models for storing prediction history.</li>
    <li><code>app.py</code>: Main app routes for user and medical assistant access.</li>
    <li><code>chatapp.py</code>: The AI-driven medical assistant's chat interface.</li>
    <li><code>config.py</code>: Configuration settings.</li>
  </ul>

</body>
</html>
