import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis } from "recharts";
import toast, { Toaster } from "react-hot-toast";
import { BackgroundBeams } from "../components/ui/BackgroundBeams";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

export function Dashboard({ token }) {
  const [formData, setFormData] = useState({ gender: '0', age: '', sleep_duration: '', physical_activity: '', heart_rate: '', daily_steps: '', stress_level: '5' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('assessment');

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_URL}/api/assessments`, { headers: { 'Authorization': `Bearer ${token}` } });
      const data = await res.json();
      setHistory(data);
    } catch (err) { console.error(err); }
  };

  useEffect(() => {
    fetchHistory();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); setResult(null);
    try {
      const response = await fetch(`${API_URL}/api/assessments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Gagal mendapatkan hasil dari Server.");
      setResult(data);
      fetchHistory(); // refresh history immediately
      toast.success("AI Engine Diagnosis Selesai!");
    } catch (error) {
      toast.error(error.message);
    }
    setLoading(false);
  };

  const getBadgeColor = (str) => {
    if (!str) return 'from-slate-200 to-slate-300';
    if (str.includes('Normal') || str.includes('Aman')) return 'from-teal-400 to-emerald-500 shadow-[0_5px_15px_rgba(16,185,129,0.3)] text-white';
    if (str.includes('Insomnia')) return 'from-amber-400 to-orange-500 shadow-[0_5px_15px_rgba(245,158,11,0.3)] text-white';
    return 'from-rose-500 to-red-600 shadow-[0_5px_15px_rgba(225,29,72,0.3)] text-white';
  };

  const generateAdvice = (data, pred) => {
    let advice = [];
    if (Number(data.sleep_duration) < 6) advice.push(`Tidur defisit (${data.sleep_duration} jam). Rekomendasi: Terapi sleep hygiene & minimalisir paparan layar biru 60 menit pralelap.`);
    if (Number(data.heart_rate) > 80) advice.push(`Takikardia ringan (${data.heart_rate} BPM). Observasi pemicu stres kronis kardiologis.`);
    if (Number(data.physical_activity) < 30) advice.push(`Sedentary terdeteksi. Anjuran: 15 menit aktivitas kardiovaskuler moderat harian.`);
    if (pred.includes("Apnea")) advice.push("Probabilitas Sleep Apnea klinis persisten. Saran: Rujukkan ke fasilitas polisomnografi (Sleep Lab).");
    if (pred.includes("Insomnia")) advice.push("Pola Insomniak terpantau. Batasi asupan adenosin-blocker (kafein) pasca jam 14:00.");
    if (advice.length === 0) advice.push("Seluruh metrik vital berada dalam rentang ideal klinis. Status pemeliharaan dianjurkan.");
    return advice.join(' ');
  };

  const calculateScore = (data) => {
    let score = 100;
    if (Number(data.sleep_duration) < 6) score -= 25;
    else if (Number(data.sleep_duration) < 7) score -= 10;
    if (Number(data.heart_rate) > 80) score -= 15;
    if (Number(data.physical_activity) < 30) score -= 15;
    if (Number(data.daily_steps) < 5000) score -= 15;
    return Math.max(0, score);
  };

  const inputClass = "w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 input-glow transition-all shadow-sm focus:bg-white";

  return (
    <div className="min-h-screen bg-slate-50 pt-24 px-4 sm:px-8 relative overflow-hidden font-sans">
      <div className="absolute inset-0 z-0 pointer-events-none">
        <BackgroundBeams />
      </div>
      <div className="absolute top-0 w-full h-full overflow-hidden z-0 pointer-events-none opacity-40">
         <div className="absolute -top-[10%] -right-[5%] w-[600px] h-[600px] rounded-full bg-teal-100 blur-3xl"></div>
      </div>

      <Toaster position="top-center" toastOptions={{ style: { background: '#ffffff', color: '#1e293b', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' } }} />

      <motion.div 
        initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
        className="max-w-6xl mx-auto relative z-10"
      >
        <div className="flex border-b border-slate-200 mb-8 overflow-x-auto">
          <button onClick={() => setActiveTab('assessment')} className={`pb-4 px-6 text-sm md:text-base font-bold transition-colors whitespace-nowrap ${activeTab === 'assessment' ? 'text-teal-600 border-b-2 border-teal-500' : 'text-slate-400 hover:text-slate-600'}`}>
            Formulir Asesmen Klinis
          </button>
          <button onClick={() => setActiveTab('history')} className={`pb-4 px-6 text-sm md:text-base font-bold transition-colors whitespace-nowrap ${activeTab === 'history' ? 'text-teal-600 border-b-2 border-teal-500' : 'text-slate-400 hover:text-slate-600'}`}>
            Pusat Rekam Medis
          </button>
        </div>

        <AnimatePresence mode="wait">
          {activeTab === 'assessment' ? (
            <motion.div key="assessment" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }}>
              <div className="grid md:grid-cols-12 gap-8">
                {/* FORM BOX (Lebih Lebar 7 Kolom) */}
                <div className="md:col-span-7 glass-panel p-8 bg-white/80 border border-slate-100">
                  <h3 className="text-xl font-black mb-6 text-slate-800 border-b border-slate-100 pb-4 flex items-center gap-2">
                    <span className="text-teal-500">📋</span> Input Vitals Pasien
                  </h3>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-2 gap-5">
                       <div>
                        <label className="text-xs font-bold text-slate-500 mb-1.5 block uppercase tracking-wide">Jenis Kelamin</label>
                        <select name="gender" value={formData.gender} onChange={handleChange} className={inputClass} title="Metrik gender diperlukan untuk kalibrasi base heart rate.">
                          <option value="0">Pria</option><option value="1">Wanita</option>
                        </select>
                      </div>
                      <div>
                        <label className="text-xs font-bold text-slate-500 mb-1.5 block uppercase tracking-wide">Usia (Tahun)</label>
                        <input type="number" name="age" onChange={handleChange} required placeholder="Contoh: 28" className={inputClass} />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-5">
                      <div>
                        <label className="text-xs font-bold text-slate-500 mb-1.5 block uppercase tracking-wide">Durasi Tidur (Jam)</label>
                        <input type="number" step="0.1" name="sleep_duration" onChange={handleChange} required placeholder="Total durasi siklus lelap" className={inputClass} />
                      </div>
                      <div>
                        <label className="text-xs font-bold text-slate-500 mb-1.5 block uppercase tracking-wide">Kardio / Fisik (Mnt)</label>
                        <input type="number" name="physical_activity" onChange={handleChange} required placeholder="Gerakan aktif harian" className={inputClass} />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-5">
                      <div>
                        <label className="text-xs font-bold text-slate-500 mb-1.5 block uppercase tracking-wide">Resting BPM (Detak/Mnt)</label>
                        <input type="number" name="heart_rate" onChange={handleChange} required placeholder="Standar saat duduk rileks" className={inputClass} />
                      </div>
                      <div>
                        <label className="text-xs font-bold text-slate-500 mb-1.5 block uppercase tracking-wide">Pedometrik (Langkah)</label>
                        <input type="number" name="daily_steps" onChange={handleChange} required placeholder="Target global: 8000+" className={inputClass} />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 gap-4 pt-4 border-t border-slate-100">
                      <div>
                        <div className="flex justify-between items-end mb-2">
                           <label className="text-xs font-bold text-slate-500 block uppercase tracking-wide">Tingkat Beban Stres Psikologis</label>
                           <span className="text-[10px] font-bold text-teal-600 bg-teal-50 px-2 py-1 rounded">Skala: {formData.stress_level}/10</span>
                        </div>
                        <input type="range" min="1" max="10" name="stress_level" value={formData.stress_level} onChange={handleChange} className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-500" />
                        <div className="flex justify-between text-[10px] font-bold text-slate-400 mt-2">
                           <span>😌 Rileks Optimal (1)</span>
                           <span>🔥 Burnout Overload (10)</span>
                        </div>
                      </div>
                    </div>
                    <button type="submit" disabled={loading} className="w-full mt-4 bg-gradient-to-r from-teal-600 to-emerald-500 hover:from-teal-500 hover:to-emerald-400 text-white font-bold py-4 rounded-xl shadow-md transition-all flex justify-center items-center gap-2">
                      {loading ? <span className="animate-spin text-xl">⏳</span> : <span className="text-xl">🧬</span>}
                      {loading ? 'Server Neural Net Sedang Menghitung...' : 'Mulai Diagnosis AI End-to-End'}
                    </button>
                  </form>
                </div>

                {/* RESULT BOX (Col 5) */}
                <div className="md:col-span-5 flex flex-col h-full">
                  {!result && (
                    <div className="flex-1 glass-panel border border-dashed border-slate-300 flex flex-col items-center justify-center p-8 text-center bg-white/50 text-slate-500">
                      <div className="w-20 h-20 bg-teal-50 rounded-full flex items-center justify-center mb-4 shadow-inner text-teal-500"><span className="text-3xl">💻</span></div>
                      <h4 className="font-bold text-slate-700 mb-2">Menunggu Data Silang</h4>
                      <p className="text-sm">Silakan masukkan ke-7 vitals demografi pasien di form sebelah kiri untuk melakukan scanning klasifikasi prediksi Deep Learning secara real-time.</p>
                    </div>
                  )}

                  {result && (
                    <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="flex-1 glass-panel bg-white p-6 md:p-8 flex flex-col justify-start items-center text-center shadow-lg border-slate-100">
                      <div className="flex justify-between w-full mb-6 pb-4 border-b border-slate-100">
                        <span className="text-slate-400 uppercase tracking-widest text-[10px] font-black">Indeks Kebugaran</span>
                        <span className="text-teal-600 font-black text-sm">{calculateScore(formData)} / 100</span>
                      </div>
                      
                      <div className="mb-2">
                         <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Hasil Diagnosis AI</span>
                      </div>
                      <div className={`px-6 py-4 rounded-2xl bg-gradient-to-br w-full mb-6 ${getBadgeColor(result.predicted_disorder)}`}>
                          <span className="text-2xl md:text-3xl font-black drop-shadow-md">
                            {result.predicted_disorder}
                          </span>
                      </div>

                      {/* PROBABILITY BARS */}
                      {result.probabilities && (
                        <div className="w-full bg-slate-50 p-5 rounded-2xl border border-slate-100 shadow-inner mb-6">
                          <h5 className="text-[10px] font-black text-slate-400 mb-4 pb-2 border-b border-slate-200 uppercase tracking-widest">Detail Probabilitas Softmax Layer</h5>
                          <div className="space-y-4">
                            {Object.entries(result.probabilities).map(([key, val]) => (
                               <div key={key}>
                                 <div className="flex justify-between text-xs mb-1.5">
                                   <span className="text-slate-600 font-bold">{key.replace('_', ' ')}</span>
                                   <span className="text-slate-500 font-mono font-semibold">{val}%</span>
                                 </div>
                                 <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                                   <motion.div initial={{ width: 0 }} animate={{ width: `${val}%` }} transition={{ duration: 1.2, ease: "easeOut" }} className={`h-full rounded-full ${key==='Normal'?'bg-emerald-500':key==='Insomnia'?'bg-amber-500':'bg-rose-500'}`} />
                                 </div>
                               </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* LIFESTYLE RADAR */}
                      <div className="w-full h-56 bg-white rounded-2xl border border-slate-100 p-2 shadow-sm relative mb-6">
                        <h5 className="absolute top-2 left-4 text-[10px] uppercase font-bold text-slate-400 z-10">Radar Metrik Ideal</h5>
                        <ResponsiveContainer width="100%" height="100%">
                          <RadarChart cx="50%" cy="50%" outerRadius="65%" data={[
                            { metric: "Tidur (8j)", score: Math.min((formData.sleep_duration / 8) * 100, 100) },
                            { metric: "Fisik (60m)", score: Math.min((formData.physical_activity / 60) * 100, 100) },
                            { metric: "Langkah (8k)", score: Math.min((formData.daily_steps / 8000) * 100, 100) },
                            { metric: "Jantung Bugar", score: Math.max(0, 100 - Math.max(0, (formData.heart_rate - 65))) },
                            { metric: "Bebas Stres", score: Math.max(0, 100 - (formData.stress_level * 10)) }
                          ]}>
                            <PolarGrid stroke="#e2e8f0" />
                            <PolarAngleAxis dataKey="metric" tick={{ fill: '#64748b', fontSize: 10, fontWeight: 'bold' }} />
                            <Radar dataKey="score" stroke="#0d9488" fill="#14b8a6" fillOpacity={0.3} />
                          </RadarChart>
                        </ResponsiveContainer>
                      </div>

                      <div className="text-left w-full bg-teal-50 p-5 rounded-2xl border border-teal-100 shadow-sm">
                        <h5 className="text-xs font-black text-teal-800 mb-2 flex items-center gap-1"><span>🩺</span> Resep & Rekomendasi Terapi</h5>
                        <p className="text-xs text-teal-700 font-medium leading-relaxed">
                          {generateAdvice(formData, result.predicted_disorder)}
                        </p>
                      </div>

                      <div className="mt-6 w-full flex justify-between items-center border-t border-slate-100 pt-4">
                        <div className="text-left">
                           <p className="text-[10px] text-slate-400 uppercase font-bold tracking-widest">Risk Factor</p>
                           <p className={`text-sm tracking-tight ${result.risk_level === 'HIGH' ? 'text-rose-600 font-black' : 'text-emerald-600 font-black'}`}>{result.risk_level}</p>
                        </div>
                        <div className="text-right">
                           <p className="text-[10px] text-slate-400 uppercase font-bold tracking-widest">Model</p>
                           <p className="text-xs font-bold text-slate-600">TF Deep Learning L1</p>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div key="history" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-8">
              
              {/* SUMMARY CARD */}
              {history.length > 0 && (
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
                   <div className="glass-panel p-6 flex flex-col justify-center bg-white border border-slate-100 shadow-sm">
                     <span className="text-xs text-slate-400 uppercase font-black tracking-widest mb-1">Total Asesmen Masuk</span>
                     <span className="text-3xl font-black text-slate-700">{history.length} <span className="text-sm font-medium text-slate-400 tracking-normal">kasus</span></span>
                   </div>
                   <div className="glass-panel p-6 flex flex-col justify-center bg-white border border-slate-100 shadow-sm">
                     <span className="text-xs text-slate-400 uppercase font-black tracking-widest mb-1">Mayoritas Temuan AI</span>
                     <span className="text-xl font-black text-teal-600">{history[0].predicted_disorder}</span>
                   </div>
                   <button className="glass-panel p-6 flex flex-col justify-center items-center cursor-pointer hover:bg-slate-50 transition-colors border-dashed border-2 border-slate-200 shadow-none bg-transparent group" onClick={() => window.print()}>
                     <span className="text-3xl mb-2 group-hover:scale-110 transition-transform">🖨️</span>
                     <span className="text-xs font-black text-slate-500 uppercase tracking-widest group-hover:text-teal-600">Terbitkan Laporan PDF</span>
                   </button>
                 </div>
              )}

              {/* GAMBARAN TREN (CHART) */}
              {history.length > 0 && (
                <div className="glass-panel p-6 md:p-8 h-[400px] bg-white border-slate-100 shadow-sm">
                  <h3 className="text-slate-800 font-black mb-6 text-sm uppercase tracking-widest">Grafik Historis: Durasi Tidur Siklus Penuh (Jam)</h3>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={[...history].reverse()} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <defs>
                        <linearGradient id="colorSleep" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.4}/>
                          <stop offset="95%" stopColor="#14b8a6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                      <XAxis dataKey="created_at" tickFormatter={(str) => new Date(str).toLocaleDateString('id-ID')} stroke="#94a3b8" fontSize={10} fontWeight="bold" />
                      <YAxis stroke="#94a3b8" fontSize={10} fontWeight="bold" />
                      <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px', color: '#1e293b', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)' }} />
                      <Area type="monotone" dataKey="sleep_duration" stroke="#0d9488" strokeWidth={3} fillOpacity={1} fill="url(#colorSleep)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              )}

              {/* TABEL HISTORI */}
              <div className="glass-panel overflow-hidden bg-white border border-slate-200 shadow-sm">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-slate-50 border-b border-slate-200">
                      <tr>
                        <th className="px-6 py-5 text-slate-500 font-black uppercase tracking-wider text-[10px]">Waktu Eksekusi Diagnosis</th>
                        <th className="px-6 py-5 text-slate-500 font-black uppercase tracking-wider text-[10px]">Output Layer (Penyakit)</th>
                        <th className="px-6 py-5 text-slate-500 font-black uppercase tracking-wider text-[10px]">Skala Stres</th>
                        <th className="px-6 py-5 text-slate-500 font-black uppercase tracking-wider text-[10px]">Tidur (Jam)</th>
                        <th className="px-6 py-5 text-slate-500 font-black uppercase tracking-wider text-[10px]">Fisik (Mnt)</th>
                        <th className="px-6 py-5 text-slate-500 font-black uppercase tracking-wider text-[10px]">Resting HR</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {history.length > 0 ? history.map((row) => (
                        <tr key={row.id} className="hover:bg-slate-50/80 transition-colors">
                          <td className="px-6 py-4 text-xs font-semibold text-slate-600">{new Date(row.created_at).toLocaleString('id-ID')}</td>
                          <td className="px-6 py-4">
                             <span className={`px-3 py-1 text-[10px] font-black rounded-full border whitespace-nowrap uppercase tracking-widest shadow-sm ${row.predicted_disorder.includes('Normal') || row.predicted_disorder.includes('Aman') ? 'bg-emerald-50 text-emerald-600 border-emerald-200' : 'bg-rose-50 text-rose-600 border-rose-200'}`}>
                                {row.predicted_disorder}
                             </span>
                          </td>
                          <td className="px-6 py-4 text-slate-600 font-bold text-xs">{row.stress_level || 5} / 10</td>
                          <td className="px-6 py-4 text-slate-500 text-xs font-semibold">{row.sleep_duration}</td>
                          <td className="px-6 py-4 text-slate-500 text-xs font-semibold">{row.physical_activity}</td>
                          <td className="px-6 py-4 text-slate-500 text-xs font-semibold">{row.heart_rate}</td>
                        </tr>
                      )) : (
                        <tr><td colSpan="6" className="text-center py-16 text-slate-400 font-medium">Buku log medis Anda masih steril/kosong.</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
