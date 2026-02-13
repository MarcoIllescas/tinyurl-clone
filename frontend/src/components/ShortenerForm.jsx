import { useState } from 'react';
import axios from 'axios';
import { FaCopy, FaCheck, FaLink, FaSearch, FaExternalLinkAlt } from 'react-icons/fa';

const ShortenerForm = () => {
  //State to control the mode: 'shorten' or 'resolve'
  const [mode, setMode] = useState('shorten');

  // Single state for the input (works for long URL or short ID)
  const [inputValue, setInputValue] = useState('');
  
  // Income statements 
  const [resultShortUrl, setResultShortUrl] = useState('');
  const [resultLongUrl, setResultLongUrl] = useState('');

  // UI states
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  // Function to switch mode and clear states
  const toggleMode = (newMode) => {
    setMode(newMode);
    setInputValue('');
    setResultShortUrl('');
    setResultLongUrl('');
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResultShortUrl('');
    setResultLongUrl('');

    try {
      if (mode === 'shorten') {
        const response = await axios.post(`${API_URL}/`, {
          long_url: inputValue
        });
        const fullShortUrl = `${API_URL}/${response.data.short_id}`;
        setResultShortUrl(fullShortUrl);

      } else {
        const shortIdToResolve = inputValue.trim().split('/').pop();

        const response = await axios.post(`${API_URL}/resolve`, {
          short_id: shortIdToResolve
        });
        setResultLongUrl(response.data.long_url);
      }
      
    } catch (err) {
      console.error(err);
      if (err.response && err.response.status === 404) {
        setError('URL not found in DB.');
      } else if (mode === 'shorten') {
         setError('Error. Make sure the URL is valid.');
      } else {
         setError('Error verifying. Check the ID or the connection.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(resultShortUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="main-card">
      {/* --- NAVIGATION TABS --- */}
      <div className="tabs">
        <button 
          className={`tab-btn ${mode === 'shorten' ? 'active' : ''}`}
          onClick={() => toggleMode('shorten')}
        >
          <FaLink className="tab-icon"/> Shorten URL
        </button>
        <button 
          className={`tab-btn ${mode === 'resolve' ? 'active' : ''}`}
          onClick={() => toggleMode('resolve')}
        >
          <FaSearch className="tab-icon"/> Check Destination
        </button>
      </div>

      <div className="card-content">
        <h2 className="form-title">
          {mode === 'shorten' ? 'Create short link' : 'Check where a link goes'}
        </h2>
        
        <form onSubmit={handleSubmit} className="action-form">
          <div className="input-group">
            <input
              type={mode === 'shorten' ? 'url' : 'text'}
              placeholder={mode === 'shorten' ? 'Paste your long URL here (https://...)' : 'Paste the short link or ID here'}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              required
              className="main-input"
            />
          </div>
          <button type="submit" disabled={loading || !inputValue.trim()} className="main-btn">
            {loading ? 'Processing...' : (mode === 'shorten' ? 'Shorten' : 'Verify')}
          </button>
        </form>

        {error && <div className="error-msg">{error}</div>}

        {/* --- RESULT: SHORTEN MODE --- */}
        {resultShortUrl && mode === 'shorten' && (
          <div className="result-box success-box animate-pop">
            <p className="result-label">Your short link is ready!</p>
            <div className="copy-container">
              <a href={resultShortUrl} target="_blank" rel="noopener noreferrer" className="short-link">
                {resultShortUrl}
              </a>
              <button onClick={handleCopy} className="copy-btn" title="Copy to clipboard">
                {copied ? <FaCheck color="#28a745"/> : <FaCopy />}
              </button>
            </div>
          </div>
        )}

        {/* --- RESULT: VERIFY MODE --- */}
        {resultLongUrl && mode === 'resolve' && (
          <div className="result-box info-box animate-pop">
            <p className="result-label">This short link redirects to:</p>
            <div className="long-url-container">
              <a href={resultLongUrl} target="_blank" rel="noopener noreferrer" className="long-link">
                {resultLongUrl} <FaExternalLinkAlt className="link-icon-small"/>
              </a>
            </div>
            <p className="security-note">Verified: It is safe to open this link.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ShortenerForm;
