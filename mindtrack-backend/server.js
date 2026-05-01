import express from 'express';
import cors from 'cors';
import sqlite3 from 'sqlite3';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { rateLimit } from 'express-rate-limit';

const app = express();
app.use(cors());
app.use(express.json());

const JWT_SECRET = 'mindtrack-super-secret-key-2026';

// Middleware keamanan DDoS/Spam Request (Rate Limit) khusus AI Endpoint
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 menit
  limit: 50, // Limit 50 request per window per IP
  message: { error: 'Terlalu banyak request dari perangkat ini. Harap jeda beberapa menit.' }
});

// Menggunakan file persisten mindtrack.db alih-alih memory RAM
const db = new sqlite3.Database('./mindtrack.db', (err) => {
  if (err) {
    console.error('Error opening database: ', err.message);
  } else {
    console.log('Terhubung ke database persisten secara lokal (mindtrack.db).');
    
    // Create users table
    db.run(`CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      email TEXT UNIQUE,
      password_hash TEXT
    )`);

    // Create assessments table with user_id & new fields
    db.run(`CREATE TABLE IF NOT EXISTS assessments (
      id INTEGER PRIMARY KEY AUTOINCREMENT, 
      user_id INTEGER,
      gender INTEGER, 
      age INTEGER, 
      sleep_duration REAL, 
      physical_activity INTEGER, 
      heart_rate INTEGER, 
      daily_steps INTEGER, 
      stress_level INTEGER DEFAULT 5,
      predicted_disorder TEXT,
      probability_breakdown TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(user_id) REFERENCES users(id)
    )`, (err) => {
      // Dynamic evolution: Tambahkan kolom baru tanpa memecah database lama jika sudah eksis
      db.run("ALTER TABLE assessments ADD COLUMN stress_level INTEGER DEFAULT 5", () => {});
      db.run("ALTER TABLE assessments ADD COLUMN probability_breakdown TEXT DEFAULT '{}'", () => {});
    });
  }
});

// Middleware autentikasi
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) return res.status(401).json({ error: 'Akses ditolak. Silakan login terlebih dahulu.' });
  
  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Sesi anda tidak valid atau telah kadaluarsa.' });
    req.user = user;
    next();
  });
};

app.get('/api/health', (req, res) => {
  res.send({ 
    status: 'Operational', 
    service: 'MindTrack Backend',
    version: '2.0.0-capstone',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/stats', (req, res) => {
  db.get('SELECT COUNT(*) as total_users FROM users', [], (err, u) => {
    db.get('SELECT COUNT(*) as total_assessments FROM assessments', [], (err, a) => {
      res.json({
        total_users: u ? u.total_users : 0,
        total_assessments: a ? a.total_assessments : 0,
        ai_engine_status: "Active"
      });
    });
  });
});

// ============================================
// Endpoint 1: Registrasi User Baru
// ============================================
app.post('/api/auth/register', async (req, res) => {
  const { username, email, password } = req.body;
  if (!username || !email || !password) return res.status(400).json({ error: 'Pastikan nama, email, dan masukan sandi diisi.' });

  try {
    const salt = await bcrypt.genSalt(10);
    const password_hash = await bcrypt.hash(password, salt);
    
    db.run(
      'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
      [username, email, password_hash],
      function (err) {
        if (err) {
          if (err.message.includes('UNIQUE constraint failed')) {
            return res.status(400).json({ error: 'Maaf, Email atau Nama tersebut sudah digunakan orang lain.' });
          }
          return res.status(500).json({ error: err.message });
        }
        res.status(201).json({ message: 'Pendaftaran sukses! Silakan login.', userId: this.lastID });
      }
    );
  } catch (error) {
    res.status(500).json({ error: 'Terjadi kegagalan memproses sandi rahasia.' });
  }
});

// ============================================
// Endpoint 2: Login Akun
// ============================================
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  
  db.get('SELECT * FROM users WHERE email = ?', [email], async (err, user) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!user) return res.status(400).json({ error: 'Email yang Anda masukkan salah.' });
    
    const validPassword = await bcrypt.compare(password, user.password_hash);
    if (!validPassword) return res.status(400).json({ error: 'Kata sandi tidak tepat.' });
    
    // Menghasilkan Token rahasia berumur 24 jam
    const token = jwt.sign({ id: user.id, username: user.username }, JWT_SECRET, { expiresIn: '24h' });
    res.json({ token, username: user.username });
  });
});

// ============================================
// Endpoint 3: Jalankan Prediksi AI & Simpan ke Histori
// ============================================
app.post('/api/assessments', authenticateToken, apiLimiter, async (req, res) => {
  const { gender, age, sleep_duration, physical_activity, heart_rate, daily_steps, stress_level } = req.body;
  const user_id = req.user.id;
  
  // Default fallback if stress level omitted from legacy frontend
  const final_stress = stress_level ? parseInt(stress_level) : 5;
  
  try {
    // 1. Meneruskan data sinkronasi ke API Machine Learning (FastAPI Python)
    const aiResponse = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        gender: parseInt(gender), 
        age: parseInt(age), 
        sleep_duration: parseFloat(sleep_duration), 
        physical_activity: parseInt(physical_activity), 
        heart_rate: parseInt(heart_rate), 
        daily_steps: parseInt(daily_steps),
        stress_level: final_stress
      }),
      signal: AbortSignal.timeout(10000) // Timeout setelah 10 detik agar loading tidak stuck
    });
    
    if (!aiResponse.ok) {
        const errText = await aiResponse.text();
        console.error("AI 422 Error Detailed Payload:", errText);
        throw new Error(`AI Validation Error: ${errText}`);
    }
    
    const aiData = await aiResponse.json();
    const predicted_disorder = aiData.predicted_disorder;
    const probability_json = JSON.stringify(aiData.probabilities || {});
    
    // 2. Simpan Histori Assessment ke Database dengan ID Pengguna yang login (Foreign key)
    const query = `INSERT INTO assessments (
      user_id, gender, age, sleep_duration, physical_activity, heart_rate, daily_steps, stress_level, predicted_disorder, probability_breakdown
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;
    
    db.run(
      query,
      [user_id, gender, age, sleep_duration, physical_activity, heart_rate, daily_steps, final_stress, predicted_disorder, probability_json],
      function (err) {
        if (err) return res.status(500).send(err.message);
        res.json({ 
          id: this.lastID, 
          predicted_disorder: predicted_disorder, 
          ai_confidence: aiData.confidence_score, 
          risk_level: aiData.risk_level,
          probabilities: aiData.probabilities,
          model_type: aiData.model_type 
        });
      }
    );
  } catch (error) {
    console.error(error);
    if (error.message.includes('AI Validation Error')) {
        return res.status(400).json({ error: error.message });
    }
    res.status(500).json({ error: 'Gagal menghubungi server AI FastAPI Python. Pastikan python uvicorn menyala.' });
  }
});

// ============================================
// Endpoint 4: Get Riwayat Prediksi Pengguna Saat Ini
// ============================================
app.get('/api/assessments', authenticateToken, (req, res) => {
  const user_id = req.user.id;
  
  db.all('SELECT * FROM assessments WHERE user_id = ? ORDER BY created_at DESC', [user_id], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Backend MindTrack (Versi Aman) menyala di port ${PORT}`);
});
