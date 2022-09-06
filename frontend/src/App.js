import './App.css';
import { useState, useEffect } from 'react';
import Axios from "axios";

const App = () => {

  const [Auth, setAuth] = useState(false);
  const [Tables, setTables] = useState(null);
  const [name, setName] = useState("");
  const [TableId, setTableId] = useState("");
  const [Apps, setApps] = useState(null);
  const [company, setAppCompany] = useState("");
  const [position, setAppPosition] = useState("");
  const [url, setAppUrl] = useState("");

  useEffect(() => {

    Axios.get("http://localhost:5000/api/user", { withCredentials: true })
      .then((response) => {
        console.log(response);
        setAuth(true);
      })
      .catch((response) => {
        console.log(response);
        setAuth(false);
      })
      
    },[]);
    
  const getUserTables = () => {
    Axios.get("http://localhost:5000/api/user/tables", { withCredentials: true }).then(
      (response) => {
        console.log(response);
        setTables(response.data);
      }
    )
  }

  const createUserTable = (e) => {
    e.preventDefault();
    Axios.post("http://localhost:5000/api/user/tables", {name}, { withCredentials: true }).then(
      (response) => {
        console.log(response)
      }
    )
  }

  const deleteUserTable = (e) => {
    e.preventDefault();
    Axios.delete(`http://localhost:5000/api/user/tables/${TableId}`, { withCredentials: true }).then(
      (response) => {
        console.log(response)
      }
    )
  }

  const createApplications = (e) => {
    e.preventDefault();
    const data = {company, position, url};
    console.log(data);
    Axios.post(`http://localhost:5000/api/user/tables/${TableId}/applications`, data, { withCredentials: true}).then(
      (response) => {
        console.log(response);
      }
    )
  }


  const getApplications = (e) => {
    e.preventDefault();
    Axios.get(`http://localhost:5000/api/user/tables/${TableId}/applications`, { withCredentials: true }).then(
      (response) => {
        console.log(response);
        setApps(response.data);
      }
    )
  }
  
  const parseUrl = (e) => {
    e.preventDefault();
    Axios.get(`http://localhost:5000/api/parse`, {params: {url}}, { withCredentials: true }).then(
      (response) => {
        console.log(response);
        if ("position" in response.data)
          setAppPosition(response.data.position[0]);
        if ("company" in response.data)
          setAppCompany(response.data.company[0]);
      }
    )
  }

  return (
    <div className="App">
      {!Auth && <a href="http://localhost:5000/login"><button>Login</button></a>}
      {Auth && <a href="http://localhost:5000/logout"><button>Logout</button></a>}
      <br></br>
      <div>
        <form onSubmit={createUserTable}>
          <label>table_name: </label>
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <button>Create Table</button>
        </form>
      </div>
      <button onClick={getUserTables}> Get tables </button>
      <div><pre>{JSON.stringify(Tables, null, 2) }</pre></div>


      
      <div>
        <form>
          <label>table_id: </label>
          <input
            type="text"
            required
            value={TableId}
            onChange={(e) => setTableId(e.target.value)}
          />
          <button type="button" onClick={deleteUserTable}>Delete Table</button>
          <button type="button" onClick={getApplications}>Get Applications</button>
        </form>
      </div>
      
      <div>
        <form>
          <label>Company: </label>
          <input
            type="text"
            required
            value={company}
            onChange={(e) => setAppCompany(e.target.value)}
          />
          <label>Position: </label>
          <input
            type="text"
            required
            value={position}
            onChange={(e) => setAppPosition(e.target.value)}
          />
          <label>url: </label>
          <input
            type="text"
            value={url}
            onChange={(e) => setAppUrl(e.target.value)}
          />
          <button type="button" onClick={parseUrl}>Parse url</button>
          <button type="button" onClick={createApplications}>Create Application</button>
        </form>
      </div>
      <div><pre>{JSON.stringify(Apps, null, 2) }</pre></div>

      
    </div>
    
  );
}

export default App;
