import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { LoginPage, RegisterPage } from './pages/AuthPages';
import { Dashboard } from './pages/Dashboard';
import { PrivacyPolicy, TermsOfService, ApiDocs } from './pages/StaticPages';

// ============================================
// Komponen: HALAMAN 404 NOT FOUND (A4 - Light Theme)
// ============================================
function NotFound() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-7xl font-extrabold text-teal-600 mb-4 opacity-50">404</h1>
      <h2 className="text-2xl font-bold text-slate-800 mb-2">Halaman Tidak Ditemukan</h2>
      <p className="text-slate-500 mb-8 max-w-sm">Mohon maaf, rekam medis atau direktori yang Anda cari tidak tersedia di sistem kami.</p>
      <Link to="/" className="px-6 py-3 bg-teal-600 hover:bg-teal-500 text-white rounded-full font-bold shadow-md hover:shadow-lg transition-all">Kembali ke Beranda</Link>
    </div>
  );
}

// ============================================
// KOMPONEN UTAMA ROOT
// ============================================
function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [username, setUsername] = useState(localStorage.getItem('username') || '');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setToken(''); setUsername('');
  };

  return (
    <BrowserRouter>
      {/* NAVBAR FLOATING (A1 - Light Theme) */}
      <nav className="fixed top-0 w-full z-50 bg-white/90 backdrop-blur-md border-b border-slate-200 shadow-sm transition-all duration-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2">
               <span className="text-2xl font-black text-slate-800 tracking-tighter">
                 MindTrack
               </span>
               <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-teal-100 text-teal-700">CLINICAL</span>
            </Link>
            
            <div className="flex items-center gap-4">
              {token ? (
                <>
                  <Link to="/dashboard" className="text-sm font-semibold text-slate-600 hover:text-teal-600 transition-colors">Dashboard AI</Link>
                  <span className="w-px h-4 bg-slate-300 mx-1"></span>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-bold text-slate-800">Hi, {username}</span>
                    <button onClick={handleLogout} className="px-4 py-1.5 text-xs font-bold text-white bg-rose-500 hover:bg-rose-600 rounded-full transition-all shadow-sm">Logout</button>
                  </div>
                </>
              ) : (
                <div className="flex gap-4">
                  <Link to="/login" className="text-sm font-bold text-slate-600 hover:text-teal-600 transition-colors py-2">Sign In</Link>
                  <Link to="/register" className="text-sm font-bold text-white bg-teal-600 hover:bg-teal-500 transition-colors py-2 px-4 rounded-full shadow-md">Register</Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Routes */}
      <Routes>
        <Route path="/" element={!token ? <LandingPage /> : <Navigate to="/dashboard" />} />
        <Route path="/login" element={!token ? <LoginPage setToken={setToken} setUsername={setUsername} /> : <Navigate to="/dashboard" />} />
        <Route path="/register" element={!token ? <RegisterPage /> : <Navigate to="/dashboard" />} />
        
        <Route path="/dashboard" element={token ? <Dashboard token={token} /> : <Navigate to="/login" />} />
        
        {/* Static Pages */}
        <Route path="/privacy" element={<PrivacyPolicy />} />
        <Route path="/terms" element={<TermsOfService />} />
        <Route path="/api-docs" element={<ApiDocs />} />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
