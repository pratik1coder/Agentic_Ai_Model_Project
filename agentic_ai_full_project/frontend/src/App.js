import React, {useState, useEffect, useRef} from 'react';

export default function App(){
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [company, setCompany] = useState('');
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(()=>{
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if(SpeechRecognition){
      const rec = new SpeechRecognition();
      rec.lang = 'en-US';
      rec.onresult = (e)=>{
        const t = e.results[0][0].transcript;
        setInput(prev => prev ? prev + ' ' + t : t);
      }
      recognitionRef.current = rec;
    }
  },[]);

  const send = async () =>{
    if(!input) return;
    const userMsg = {role:'user', text: input};
    setMessages(prev=>[...prev,userMsg]);
    setInput('');
    try{
      const res = await fetch(
        'https://orange-umbrella-446wg75grw927j76-8000.app.github.dev/api/chat',
        {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({message:input, company: company || undefined})
        }
      );

      const j = await res.json();
      const bot = {role:'assistant', text: j.response || JSON.stringify(j)};
      setMessages(prev=>[...prev, bot]);

      if(window.speechSynthesis){
        const ut = new SpeechSynthesisUtterance(bot.text);
        window.speechSynthesis.speak(ut);
      }

    }catch(e){
      const bot = {role:'assistant', text: '(failed to reach backend)'};
      setMessages(prev=>[...prev, bot]);
    }
  }

  const toggleListen = ()=>{
    if(!recognitionRef.current) return alert('SpeechRecognition not supported in this browser');
    if(!listening){ recognitionRef.current.start(); setListening(true);}
    else { recognitionRef.current.stop(); setListening(false); }
  }

  return (
    <div className="app">
      <header><h1>Company Research Assistant (Agentic)</h1></header>
      <div className="controls">
        <input placeholder="Company (optional)" value={company} onChange={e=>setCompany(e.target.value)} />
        <button onClick={toggleListen}>{listening? 'Stop' : 'Voice'}</button>
      </div>
      <div className="chat">
        {messages.map((m,i)=> (
          <div key={i} className={m.role==='user'? 'bubble user':'bubble bot'}>{m.text}</div>
        ))}
      </div>
      <div className="composer">
        <input value={input} onChange={e=>setInput(e.target.value)} placeholder="Type your message or ask to research a company" />
        <button onClick={send}>Send</button>
      </div>
    </div>
  )
}

