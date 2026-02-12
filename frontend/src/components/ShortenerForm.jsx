import { useState } from 'react';
import axios from 'axios';
import { FaCopy, FaCheck } from 'react-icons/fa';

const ShortenerForm = () => {
	const [longUrl, setLongUrl] = useState('');
	const [shortUrl, setShortUrl] = useState('');
	const [loading, setLoading] = useState(false);
	const [copied, setCopied] = useState(false);
	const [error, setError] = useState('');

	// We get the backend URL from the .env file
	const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

	const handleSubmit = async (e) => {
		e.preventDefault();
		setLoading(true);
		setError('');
		setShortUrl('');

		try {
			// POST request to the backend
			const response = await axios.post(`${API_URL}/`, {
				long_url: longUrl
			});

			// Construct the final URL to display it
			const fullShortUrl = `${API_URL}/${response.data.short_id}`;
			setShortUrl(fullShortUrl);
		} catch (err) {
			console.error(err);
			setError('Error shortening URL. Please check that it is valid.');
		} finally {
			setLoading(false);
		}
	};

	const handleCopy = () => {
		navigator.clipboard.writeText(shortUrl);
		setCopied(true);
		setTimeout(() => setCopied(false), 2000); // Reset icon after 2s
	};

	return (
		<div className="card">
			<h2>TinyURL Clone</h2>

			<form onSubmit={handleSubmit}>
				<input
					type="url"
					placeholder="Paste your large URL here (https://...)"
					value={longUrl}
					onChange={(e) => setLongUrl(e.target.value)}
					required
					className="input-url"
				/>
				<button type="submit" disabled={loading} className="btn-shorten">
          			{loading ? 'Acortando...' : 'Acortar URL'}
        		</button>
        	</form>

        	{error && <p className="error">{error}</p>}

        	{shortUrl && (
        		<div className="result-container">
        			<p>Here you go!</p>
        			<div className="short-url-box">
        				<a href={shortUrl} target="_blank" rel="noopener noreferrer">
        					{shortUrl}
        				</a>
        				<button onClick={handleCopy} className="btn-copy">
        					{copied ? <FaCheck color="green"/> : <FaCopy />}
        				</button>
        			</div>
        		</div>	
        	)}
        </div>
	);
};

export default ShortenerForm;