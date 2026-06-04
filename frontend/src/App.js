import React, {useState, useEffect, useRef} from 'react';

function App(){
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);

  useEffect(()=>{
    const ws = new WebSocket('ws://localhost:8000/api/ws/chat');
    ws.onopen = ()=>console.log('ws open');
    ws.onmessage = (evt)=>{
      try{
        const d = JSON.parse(evt.data);
        setMessages(m=>[...m, d]);
      }catch(e){
        console.error(e)
      }
    }
    wsRef.current = ws;
    return ()=>ws.close();
  },[])

  function send(){
    if(!wsRef.current) return;
    wsRef.current.send(JSON.stringify({query, sensor_data: {temperature: 125, vibration: 3.2}}));
    setMessages(m=>[...m, {user: query}]);
    setQuery('');
  }

  return (
    <div style={{background:'#0b0f12', color:'#e6eef6', minHeight:'100vh', padding:20}}>
      <h2>Smart Manufacturing Troubleshooting Assistant</h2>
      <div style={{display:'flex'}}>
        <div style={{flex:1, marginRight:20}}>
          <div style={{height:400, overflow:'auto', background:'#091014', padding:10}}>
            {messages.map((m,i)=> (
              <div key={i} style={{marginBottom:8}}>[{m.status||m.user||'agent'}] {m.final||m.diagnosis||m.sensor_analysis||JSON.stringify(m)}</div>
            ))}
          </div>
          <div style={{marginTop:10}}>
            <input value={query} onChange={e=>setQuery(e.target.value)} style={{width:'80%'}} />
            <button onClick={send}>Send</button>
          </div>
        </div>
        <div style={{width:320}}>
          <div style={{background:'#071017', padding:10}}>Agent Status: <span style={{color:'#7de3a2'}}>Supervisor ready</span></div>
        </div>
      </div>
    </div>
  )
}

export default App;
