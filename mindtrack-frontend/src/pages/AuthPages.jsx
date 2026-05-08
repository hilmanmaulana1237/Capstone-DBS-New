import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { BackgroundBeams } from "../components/ui/BackgroundBeams";
import { Eye, EyeOff, Activity } from "lucide-react";
import { apiClient } from "../utils/apiClient";

const GlassCard = ({ children, title, subtitle }) => (
  <div className="min-h-screen flex items-center justify-center relative bg-slate-50 overflow-hidden px-4 pt-16">
    <div className="absolute inset-0 z-0 pointer-events-none">
      <BackgroundBeams />
    </div>
    <div className="absolute top-0 w-full h-full overflow-hidden z-0 pointer-events-none opacity-40">
       <div className="absolute top-[10%] -right-[10%] w-[500px] h-[500px] rounded-full bg-teal-100 blur-3xl"></div>
       <div className="absolute -bottom-[20%] -left-[10%] w-[400px] h-[400px] rounded-full bg-emerald-100 blur-3xl"></div>
    </div>

    <motion.div 
      initial={{ opacity: 0, scale: 0.95, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-panel p-8 sm:p-10 w-full max-w-md z-10 relative bg-white/90 shadow-xl border border-slate-100 rounded-2xl"
    >
      <div className="text-center mb-8 flex flex-col items-center">
        <div className="w-12 h-12 bg-teal-50 rounded-xl flex items-center justify-center text-teal-600 mb-4 shadow-inner">
          <Activity size={24} strokeWidth={2.5} />
        </div>
        <h2 className="text-2xl font-black text-slate-800 tracking-tight">
          {title}
        </h2>
        <p className="text-slate-500 text-sm mt-1">{subtitle}</p>
      </div>
      {children}
    </motion.div>
  </div>
);

export function LoginPage({ setToken, setUsername }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPwd, setShowPwd] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true); setError('');
    try {
      const { data } = await apiClient.post('/api/auth/login', { email, password });
      
      localStorage.setItem('token', data.token);
      localStorage.setItem('username', data.username);
      setToken(data.token);
      setUsername(data.username);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || err.message || "Gagal masuk.");
    }
    setLoading(false);
  };

  return (
    <GlassCard title="MindTrack Portal" subtitle="Silakan masuk untuk akses dasbor rekam medis.">
      {error && <motion.p initial={{opacity:0}} animate={{opacity:1}} className="text-red-600 bg-red-50 p-3 rounded-xl text-sm mb-4 border border-red-200 text-center font-medium">{error}</motion.p>}
      
      <form onSubmit={handleLogin} className="space-y-4">
        <div>
          <label className="text-slate-600 font-semibold text-xs mb-1.5 block uppercase tracking-wide">Alamat Email</label>
          <input type="email" value={email} onChange={e=>setEmail(e.target.value)} required placeholder="nama@instansi.com" className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 input-glow transition-all shadow-sm" />
        </div>
        <div className="relative">
          <label className="text-slate-600 font-semibold text-xs mb-1.5 block uppercase tracking-wide">Kata Sandi</label>
          <div className="relative">
            <input type={showPwd ? "text" : "password"} value={password} onChange={e=>setPassword(e.target.value)} required placeholder="••••••••" className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 input-glow transition-all shadow-sm pr-12" />
            <button type="button" onClick={() => setShowPwd(!showPwd)} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-teal-600 transition-colors">
               {showPwd ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
        </div>
        <button type="submit" disabled={loading} className="w-full bg-teal-600 hover:bg-teal-500 text-white font-bold py-3.5 rounded-xl mt-6 shadow-md hover:shadow-lg transition-all flex justify-center items-center gap-2">
          {loading ? <span className="animate-spin">⏳</span> : null}
          {loading ? 'Mengautentikasi...' : 'Masuk Jaringan Klinis'}
        </button>
      </form>
      <div className="mt-8 pt-6 border-t border-slate-100 text-center">
        <p className="text-slate-500 text-sm">
          Faskes Baru? <Link to="/register" className="text-teal-600 hover:text-teal-700 font-bold ml-1">Klaim Akses Akun</Link>
        </p>
      </div>
    </GlassCard>
  );
}

export function RegisterPage() {
  const [formData, setFormData] = useState({ username:'', email: '', password: '' });
  const [showPwd, setShowPwd] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    if(formData.password.length < 6) return setError("Kata sandi minimal 6 karakter demi privasi rekam medis.");
    
    setLoading(true); setError(''); setSuccess('');
    try {
      const { data } = await apiClient.post('/api/auth/register', formData);
      
      setSuccess(data.message);
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.error || err.message || "Gagal mendaftar.");
    }
    setLoading(false);
  };

  return (
    <GlassCard title="Pendaftaran Sistem" subtitle="Bergabung ke jaringan analitik B2B MindTrack.">
      {error && <motion.p initial={{opacity:0}} animate={{opacity:1}} className="text-red-600 bg-red-50 p-3 rounded-xl text-sm mb-4 border border-red-200 text-center font-medium">{error}</motion.p>}
      {success && <motion.p initial={{opacity:0}} animate={{opacity:1}} className="text-emerald-700 bg-emerald-50 p-3 rounded-xl text-sm mb-4 border border-emerald-200 text-center font-medium">{success}</motion.p>}
      
      <form onSubmit={handleRegister} className="space-y-4">
        <div>
          <label className="text-slate-600 font-semibold text-xs mb-1.5 block uppercase tracking-wide">ID Faskes / Username</label>
          <input type="text" onChange={e=>setFormData({...formData, username: e.target.value})} required placeholder="RumahSakitAbc" className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 input-glow transition-all shadow-sm" />
        </div>
        <div>
          <label className="text-slate-600 font-semibold text-xs mb-1.5 block uppercase tracking-wide">Email Resmi</label>
          <input type="email" onChange={e=>setFormData({...formData, email: e.target.value})} required placeholder="admin@instansi.com" className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 input-glow transition-all shadow-sm" />
        </div>
        <div className="relative">
          <label className="text-slate-600 font-semibold text-xs mb-1.5 block uppercase tracking-wide">Kata Sandi Kuat</label>
          <div className="relative">
             <input type={showPwd ? "text" : "password"} onChange={e=>setFormData({...formData, password: e.target.value})} required placeholder="Minimal 6 Kunci" className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 input-glow transition-all shadow-sm pr-12" />
             <button type="button" onClick={() => setShowPwd(!showPwd)} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-teal-600 transition-colors">
                {showPwd ? <EyeOff size={18} /> : <Eye size={18} />}
             </button>
          </div>
        </div>
        <button type="submit" disabled={loading} className="w-full bg-teal-600 hover:bg-teal-500 text-white font-bold py-3.5 rounded-xl mt-6 shadow-md hover:shadow-lg transition-all flex justify-center items-center gap-2">
          {loading ? <span className="animate-spin">⏳</span> : null}
          {loading ? 'Memvalidasi Identitas...' : 'Otorisasi Pendaftaran'}
        </button>
      </form>
      <div className="mt-8 pt-6 border-t border-slate-100 text-center">
        <p className="text-slate-500 text-sm">
          Faskes Terdaftar? <Link to="/login" className="text-emerald-600 hover:text-emerald-700 font-bold ml-1">Masuk Sini</Link>
        </p>
      </div>
    </GlassCard>
  );
}
