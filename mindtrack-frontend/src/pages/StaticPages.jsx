import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Shield, FileText, Code2, ArrowLeft, ArrowRight } from "lucide-react";

const PageHeader = ({ title, icon: Icon, subtitle }) => (
  <div className="bg-teal-900 text-white pt-32 pb-20 px-6 relative overflow-hidden">
    <div className="absolute inset-0 opacity-10" style={{ backgroundImage: "radial-gradient(#ffffff 1px, transparent 1px)", backgroundSize: "24px 24px" }}></div>
    <div className="max-w-4xl mx-auto relative z-10 flex flex-col items-center text-center">
      <div className="w-16 h-16 bg-teal-800 rounded-2xl flex items-center justify-center mb-6 shadow-inner border border-teal-700">
        <Icon size={32} className="text-teal-300" />
      </div>
      <h1 className="text-4xl md:text-5xl font-black mb-4 tracking-tight drop-shadow-md">{title}</h1>
      <p className="text-teal-200 text-lg max-w-2xl">{subtitle}</p>
    </div>
  </div>
);

const ContentSection = ({ title, children }) => (
  <div className="mb-12">
    <h2 className="text-2xl font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">{title}</h2>
    <div className="text-slate-600 space-y-4 leading-relaxed font-medium">
      {children}
    </div>
  </div>
);

export function PrivacyPolicy() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="min-h-screen bg-slate-50 font-sans">
      <PageHeader 
        title="Kebijakan Privasi End-to-End" 
        subtitle="Komitmen Transparansi MindTrack terhadap Pengelolaan Data Rekam Medis Faskes." 
        icon={Shield} 
      />
      <div className="max-w-4xl mx-auto px-6 py-16 bg-white shadow-xl shadow-slate-200/40 -mt-10 relative z-20 rounded-3xl border border-slate-100 mb-20">
        <ContentSection title="1. Pendahuluan">
          <p>MindTrack ("Sistem", "Platform", atau "Kami") berdedikasi sepenuhnya untuk melindungi informasi pribadi dan rekam medis yang dikirimkan oleh Fasilitas Kesehatan ("Faskes") maupun Pasien melalui arsitektur microservices kami.</p>
        </ContentSection>
        <ContentSection title="2. Standar Enkripsi & Pemrosesan">
          <p>Semua probabilitas kalkulasi (Inferensi AI) dilakukan secara tertutup melalui <strong>FastAPI Backend Router</strong>. Data demografi seperti Usia, Durasi Tidur, dan Detak Jantung tidak pernah dijual, disebarluaskan, atau disalurkan ke model pelatih generatif publik.</p>
          <p>Penyimpanan <em>local storage</em> token otorisasi pasien mematuhi standar enkripsi JWT dengan secret-key siklus terikat.</p>
        </ContentSection>
        <ContentSection title="3. Penghapusan Jejak Analitik">
          <p>Rumah Sakit atau Administrator memiliki wewenang penuh (Role-Based Access Control) untuk menghapus riwayat pasien dari <em>ledger</em> sistem. Pembersihan ini bersifat permanen tanpa residu di database SQL kami.</p>
        </ContentSection>
        <div className="mt-12 pt-8 border-t border-slate-100 flex justify-center">
          <Link to="/" className="flex items-center gap-2 text-teal-600 font-bold hover:text-teal-800 transition-colors">
            <ArrowLeft size={18}/> Kembali ke Beranda Utama
          </Link>
        </div>
      </div>
    </motion.div>
  );
}

export function TermsOfService() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="min-h-screen bg-slate-50 font-sans">
      <PageHeader 
        title="Syarat Ketentuan Institusi" 
        subtitle="Regulasi Penggunaan Layanan Prediktif MindTrack bagi Fasilitas Kesehatan." 
        icon={FileText} 
      />
      <div className="max-w-4xl mx-auto px-6 py-16 bg-white shadow-xl shadow-slate-200/40 -mt-10 relative z-20 rounded-3xl border border-slate-100 mb-20">
        <ContentSection title="1. Batasan Tanggung Jawab Medis (Disclaimer)">
          <div className="bg-rose-50 border-l-4 border-rose-500 p-4 rounded-r-lg mb-4 text-rose-800">
            <strong>Peringatan Klinis:</strong> MindTrack adalah perangkat lunak prediktif <em>Deep Learning</em> (Keras/TensorFlow) yang berfungsi sebagai Sistem Pendukung Pengambilan Keputusan (Decision Support System). **Sistem BUKANLAH pengganti diagnosis patologis formal dari Dokter/Psikiater bersertifikasi.**
          </div>
          <p>Segala luaran "Probabilitas Insomnia" maupun "Sleep Apnea" harus divalidasi silang melalui observasi medis langsung (misal: Polisomnografi pasien).</p>
        </ContentSection>
        <ContentSection title="2. Lisensi Penggunaan B2B">
          <p>Pengguna Enterprise (Rumah Sakit, Klinik, HRD Korporat) diberikan lisensi SaaS <em>Revocable</em> selama uji coba tahap kompetisi <strong>Coding Camp 2026 X DBS Foundation</strong>. Setiap upaya untuk melakukan rekayasa balik (reverse-engineering) pada Model H5 kami adalah pelanggaran hukum.</p>
        </ContentSection>
        <div className="mt-12 pt-8 border-t border-slate-100 flex justify-center">
          <Link to="/" className="flex items-center gap-2 text-teal-600 font-bold hover:text-teal-800 transition-colors">
            <ArrowLeft size={18}/> Kembali ke Beranda Utama
          </Link>
        </div>
      </div>
    </motion.div>
  );
}

export function ApiDocs() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="min-h-screen bg-slate-50 font-sans">
      <PageHeader 
        title="Dokumentasi API Inference" 
        subtitle="Panduan Integrasi Endpoint Neural-Network FastAPI ke Sistem Faskes Anda." 
        icon={Code2} 
      />
      <div className="max-w-4xl mx-auto px-6 py-16 bg-white shadow-xl shadow-slate-200/40 -mt-10 relative z-20 rounded-3xl border border-slate-100 mb-20">
        <ContentSection title="Base URL & Otorisasi">
          <div className="bg-slate-900 text-slate-300 p-4 rounded-xl font-mono text-sm mb-4">
            Production: <span className="text-teal-400">https://api.mindtrack-ai.com/v1</span><br/>
            Authorization: <span className="text-emerald-400">Bearer &lt;JWT_TOKEN&gt;</span>
          </div>
          <p>Pastikan Anda mendaftarkan <em>Client-ID</em> untuk Faskes Anda guna mendapatkan JWT.</p>
        </ContentSection>
        
        <ContentSection title="POST /api/assessments">
          <p className="mb-4">Endpoint utama untuk melakukan klasifikasi Vitals pasien terhadap arsitektur Keras layer kami.</p>
          <h4 className="font-bold text-slate-700 text-sm uppercase tracking-widest mb-2">Request Payload (JSON)</h4>
          <pre className="bg-slate-900 text-emerald-400 p-4 rounded-xl font-mono text-xs overflow-x-auto mb-6">
{`{
  "gender": "0",              // 0: Pria, 1: Wanita
  "age": 28,                  // Integer
  "sleep_duration": 6.5,      // Float (Jam)
  "physical_activity": 45,    // Integer (Menit)
  "heart_rate": 72,           // Integer (BPM)
  "daily_steps": 6000,        // Integer
  "stress_level": 6           // Integer (1-10)
}`}
          </pre>
          
          <h4 className="font-bold text-slate-700 text-sm uppercase tracking-widest mb-2">Response Output (JSON)</h4>
          <pre className="bg-slate-900 text-cyan-400 p-4 rounded-xl font-mono text-xs overflow-x-auto">
{`{
  "predicted_disorder": "Insomnia (Stadium Awal)",
  "probabilities": {
    "Normal": 12.4,
    "Sleep_Apnea": 4.1,
    "Insomnia": 83.5
  },
  "risk_level": "HIGH",
  "created_at": "2026-04-01T...Z"
}`}
          </pre>
        </ContentSection>
        <div className="mt-12 pt-8 border-t border-slate-100 flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2 text-slate-500 font-bold hover:text-slate-800 transition-colors">
            <ArrowLeft size={18}/> Beranda
          </Link>
          <a href="#" className="flex items-center gap-2 px-6 py-3 bg-teal-600 text-white rounded-full font-bold shadow-md hover:bg-teal-500 transition-all">
            Unduh Postman Collection <ArrowRight size={18}/>
          </a>
        </div>
      </div>
    </motion.div>
  );
}
