import logo from './logo.svg';
import './App.css';

async function handleClick()
{
  fetch('http://127.0.0.1:5000/upload', {
    method: 'POST',
    body: JSON.stringify({data: 'formData'}),
    headers: {
     
    }
  }).then(response=>response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Err: ',error));
  return
  try {
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: 'formData',
      headers: {
       
      }
    });
     
    const result = await response.json();
    alert(result.prediction);
  } catch (err) {
    alert("Error uploading video");
  }
}

function App() {
  return (
    <div className="App">
      <button onClick={handleClick}>
        Upload Image
      </button>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
