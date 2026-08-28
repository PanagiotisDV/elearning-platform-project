import { Link } from 'react-router-dom'
import { FaBookOpen, FaGraduationCap, FaChartLine, FaCertificate } from 'react-icons/fa'

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-primary-600">
                🎓 E-Learning platform, Μια νέα εμπειρία στην εκπαίδευση
              </span>
            </div>
            <div className="flex items-center gap-4">
              <Link to="/login" className="btn-primary text-sm">
                Σύνδεση
              </Link>
              <Link to="/register" className="btn-secondary text-sm">
                Εγγραφή
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* ===== HERO SECTION ΜΕ BACKGROUND IMAGE ===== */}
      <div 
        className="relative py-40 px-4 sm:px-6 lg:px-8"
        style={{
          backgroundImage: `url('/main-bg-page.png')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
        }}
      >
        {/* ===== OVERLAY ΓΙΑ OPACITY ===== */}
        <div 
          className="absolute inset-0 bg-white"
          style={{ opacity: 0.4 }}
        ></div>

        {/* ===== ΠΕΡΙΕΧΟΜΕΝΟ ===== */}
        <div className="relative z-10 max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-primary-900 mb-6 flex items-center justify-center gap-3">
              <FaBookOpen className="text-primary-300" />
              Διψάς για μάθηση;{' '}
              <span className="text-primary-900">Ξέρουμε τον τρόπο!!!</span>
            </h1>
            <p className="text-2xl text-extrabold text-primary-800 max-w-2xl mx-auto mb-8">
              Ανακάλυψε χιλιάδες μαθήματα από έμπειρους εκπαιδευτές.
              Ξεκίνα να μαθαίνεις σήμερα και εξέλιξε την καριέρα σου.
            </p>
            <div className="flex gap-4 justify-center">
              <Link to="/register" className="btn-primary text-lg px-8 py-3">
                Ξεκίνα Δωρεάν
              </Link>
              <Link to="/login" className="btn-secondary text-lg px-8 py-3">
                Σύνδεση
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* ===== FEATURES - ΚΑΤΩ ΑΠΟ ΤΗΝ ΕΙΚΟΝΑ ===== */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="card bg-white shadow-md hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4 flex justify-center">
              <FaGraduationCap className="text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-center mb-2">Μαθήματα από Ειδικούς</h3>
            <p className="text-gray-600 text-center">Μάθε από επαγγελματίες του κλάδου με πραγματική εμπειρία</p>
          </div>
          <div className="card bg-white shadow-md hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4 flex justify-center">
              <FaChartLine className="text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-center mb-2">Παρακολούθηση Προόδου</h3>
            <p className="text-gray-600 text-center">Παρακολούθησε τη μαθησιακή σου πορεία και τα επιτεύγματά σου</p>
          </div>
          <div className="card bg-white shadow-md hover:shadow-lg transition-shadow">
            <div className="text-4xl mb-4 flex justify-center">
              <FaCertificate className="text-yellow-600" />
            </div>
            <h3 className="text-xl font-semibold text-center mb-2">Πιστοποιητικά</h3>
            <p className="text-gray-600 text-center">Απόκτησε πιστοποιητικά για να αναδείξεις τις δεξιότητές σου</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home