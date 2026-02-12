import ShortenerForm from './components/ShortenerForm';
import './App.css';

function App() {
	return (
		<div className="app-container">
			<header>
				<h1>TinyURL Clone</h1>
				<p>Cloud Computing Practice</p>
			</header>
			<main>
				<ShortenerForm />
			</main>
		</div>
	);
}

export default App;