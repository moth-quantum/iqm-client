import { useState, useEffect } from 'react';
import Fuse from 'fuse.js';
import { Search, X } from 'lucide-react';
import AppSwitcher from './AppSwitcher';
import docs from "../search.json";

interface Doc {
  title: string;
  package: string;
  description: string;
  url: string;
}


function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Doc[]>(docs);

  const fuse = new Fuse(docs, {
    keys: ['title', 'description', 'package'],
    threshold: 0.4
  });

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Check for CMD+K (Mac) or CTRL+K (Windows/Linux)
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsModalOpen(true);
      }
      // Close modal on ESC
      if (e.key === 'Escape') {
        setIsModalOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    if (searchQuery) {
      const results = fuse.search(searchQuery);
      setSearchResults(results.map(result => result.item));
    } else {
      setSearchResults(docs);
    }
  }, [searchQuery]);

  const handleSearchClick = () => {
    setIsModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-[#ebece4] p-8">
      <div className="max-w-4xl mx-auto">

        <AppSwitcher />

        <div
          onClick={handleSearchClick}
          className="mt-6 flex items-center gap-2 p-3 bg-white border border-gray-200 rounded-lg cursor-pointer hover:border-gray-300 transition-colors"
        >
          <Search className="w-5 h-5 text-gray-400" />
          <span className="text-gray-500">Search all documentation... (Press ⌘K)</span>
        </div>

        {/* Modal */}
        {isModalOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center pt-[15vh] z-50">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[70vh] overflow-hidden">
              <div className="p-4 border-b border-gray-100 flex items-center gap-3">
                <Search className="w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  autoFocus
                  placeholder="Search documentation..."
                  className="flex-1 outline-none text-gray-900"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="p-1 hover:bg-gray-100 rounded-md transition-colors"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>

              <div className="overflow-y-auto max-h-[calc(70vh-4rem)]">
                {searchResults.map((doc, index) => (
                  <a
                    key={index}
                    href={doc.url}
                    className="block p-4 hover:bg-gray-50 transition-colors"
                  >
                    <h3 className="font-medium text-gray-900">{doc.title}</h3>
                    <span className="text-sm text-gray-500 block mt-1">
                      {doc.package}
                    </span>
                    <p className="text-sm text-gray-600 mt-1">
                      {doc.description}
                    </p>
                  </a>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
          <a href="/docs/iqm-pulse" className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-lg font-semibold text-gray-900">IQM Pulse</h2>
            <p className="mt-2 text-sm text-gray-600">Interface and implementations for control pulses.</p>
          </a>

          <a href="/docs/iqm-pulla" className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-lg font-semibold text-gray-900">IQM Pulla</h2>
            <p className="mt-2 text-sm text-gray-600">Pulse-level access library for compiling quantum circuits.</p>
          </a>

          <a href="https://iqm-finland.github.io/qiskit-on-iqm/" className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-lg font-semibold text-gray-900">Qiskit on IQM</h2>
            <p className="mt-2 text-sm text-gray-600">Qiskit adapter for IQM’s quantum computers.</p>
          </a>

          <a href="https://iqm-finland.github.io/cirq-on-iqm/" className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-lg font-semibold text-gray-900">Cirq on IQM</h2>
            <p className="mt-2 text-sm text-gray-600">Cirq adapter for IQM’s quantum computers.</p>
          </a>

          <a href="https://iqm-finland.github.io/iqm-benchmarks/" className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-lg font-semibold text-gray-900">IQM Benchmarks</h2>
            <p className="mt-2 text-sm text-gray-600">Quantum Characterization, Verification, and Validation (QCVV) tools for quantum computing.</p>
          </a>

          <a href="https://iqm-finland.github.io/iqm-client/" className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-lg font-semibold text-gray-900">IQM Client</h2>
            <p className="mt-2 text-sm text-gray-600">Python client for remote access to quantum computers for circuit-level access.</p>
          </a>

          <a href="/docs/iqm-station-control-client" className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-lg font-semibold text-gray-900">IQM Station Control Client</h2>
            <p className="mt-2 text-sm text-gray-600">Python client for remote access to quantum computers for pulse-level access.</p>
          </a>

          <a href="/docs/iqm-exa-common" className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-lg font-semibold text-gray-900">IQM EXA Common</h2>
            <p className="mt-2 text-sm text-gray-600">Abstract interfaces, helpers, utility classes, etc.</p>
          </a>
        </div>

        <footer className="mt-8 text-center text-sm text-gray-500">
          Copyright IQM Quantum Computers 2021-2025.
        </footer>
      </div>
    </div>
  );
}

export default App;