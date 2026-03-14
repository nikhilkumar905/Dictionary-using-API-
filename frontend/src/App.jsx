import { useEffect, useMemo, useState } from "react";

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "/api").replace(/\/$/, "");

function App() {
  const [word, setWord] = useState("");
  const [result, setResult] = useState("");
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [loading, setLoading] = useState(false);
  const [speaking, setSpeaking] = useState(false);

  const canSpeak = useMemo(() => result.trim().length > 0, [result]);

  const parsedResult = useMemo(() => {
    const lines = result
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);

    const synonymsLine = lines.find((line) => line.startsWith("Synonyms:"));
    const antonymsLine = lines.find((line) => line.startsWith("Antonyms:"));
    const definitionLines = lines.filter(
      (line) => !line.startsWith("Synonyms:") && !line.startsWith("Antonyms:")
    );

    const firstDefinition = definitionLines[0] || "Search a word to see meaning details.";
    const definitionMatch = firstDefinition.match(/^\(([^)]+)\)\s*(.*)$/);

    const partOfSpeech = definitionMatch ? definitionMatch[1] : "Meaning";
    const primaryMeaning = definitionMatch ? definitionMatch[2] : firstDefinition;

    const splitList = (line, prefix) => {
      if (!line) return [];
      const content = line.replace(prefix, "").trim();
      if (!content || content.toLowerCase().startsWith("no ")) return [];
      return content
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean)
        .slice(0, 8);
    };

    return {
      heading: word.trim() ? word.trim().toUpperCase() : "DICTIONARY",
      partOfSpeech,
      primaryMeaning,
      extraMeanings: definitionLines.slice(1, 3),
      synonyms: splitList(synonymsLine, "Synonyms:"),
      antonyms: splitList(antonymsLine, "Antonyms:"),
    };
  }, [result, word]);

  const fetchHistory = async () => {
    const response = await fetch(`${API_BASE}/history`);
    const data = await response.json();
    setHistory(data.history || []);
  };

  useEffect(() => {
    fetchHistory().catch(() => setHistory([]));
  }, []);

  const searchWord = async () => {
    const term = word.trim();
    if (!term) {
      alert("Please enter a word!");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/search?word=${encodeURIComponent(term)}`);
      const data = await response.json();
      if (!response.ok) {
        alert(data.error || "Search failed.");
        return;
      }
      setResult(data.result || "Word not found in the dictionary.");
      await fetchHistory();
    } catch {
      alert("Could not connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = async () => {
    const confirmDelete = window.confirm("Are you sure you want to delete the search history?");
    if (!confirmDelete) {
      return;
    }

    try {
      await fetch(`${API_BASE}/history`, { method: "DELETE" });
      setHistory([]);
      alert("Search history cleared successfully!");
    } catch {
      alert("Failed to clear history.");
    }
  };

  const speakMeaning = () => {
    if (!canSpeak) {
      alert("Please search a word first before using text-to-speech.");
      return;
    }

    if (!window.speechSynthesis) {
      alert("Text-to-speech is not supported in this browser.");
      return;
    }

    if (speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(result);
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    setSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const voiceInput = () => {
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Recognition) {
      alert("Voice input is not supported in this browser.");
      return;
    }

    const recognition = new Recognition();
    recognition.lang = "en-US";
    recognition.onresult = async (event) => {
      const spokenText = event.results[0][0].transcript;
      setWord(spokenText);
      try {
        const response = await fetch(`${API_BASE}/search?word=${encodeURIComponent(spokenText)}`);
        const data = await response.json();
        setResult(data.result || "Word not found in the dictionary.");
        await fetchHistory();
      } catch {
        alert("Could not connect to backend.");
      }
    };
    recognition.onerror = () => alert("Could not understand the audio.");
    recognition.start();
  };

  return (
    <main className="page">
      <div className="monitor">
        <div className="monitor-bezel">
          <section className="workspace">
            <aside className="sidebar">
          <div className="brand">
            <span className="brand-icon">◈</span>
            <div>
              <h1>Dict नरी</h1>
              <p>Stylish dictionary search</p>
            </div>
          </div>

          <div className="sidebar-block">
            <span className="sidebar-label">Recent Searches</span>
            <ul className="recent-list">
              {history.slice(0, 6).map((item, index) => (
                <li key={`${item}-recent-${index}`}>{item}</li>
              ))}
              {history.length === 0 && <li className="empty-recent">No recent words</li>}
            </ul>
          </div>

          <button className="sidebar-history-btn" onClick={() => setShowHistory((current) => !current)}>
            {showHistory ? "Hide History" : "Show History"}
          </button>
        </aside>

        <section className="dashboard">
          <div className="search-shell">
            <input
              value={word}
              onChange={(event) => setWord(event.target.value)}
              placeholder="Search a word..."
              onKeyDown={(event) => {
                if (event.key === "Enter") searchWord();
              }}
            />
            <button className="search-btn" onClick={searchWord} disabled={loading}>
              {loading ? "..." : "Search"}
            </button>
          </div>

          <div className="content-grid">
            <article className="history-card">
              <div className="panel-head">
                <h2>History</h2>
                <button className="mini-btn danger" onClick={clearHistory}>Clear History</button>
              </div>

              {showHistory ? (
                history.length === 0 ? (
                  <p className="history-empty">No history found.</p>
                ) : (
                  <ul className="history-list">
                    {history.map((item, index) => (
                      <li key={`${item}-${index}`}>{item}</li>
                    ))}
                  </ul>
                )
              ) : (
                <p className="history-empty">Click “Show History” from the left panel.</p>
              )}
            </article>

            <article className="detail-card">
              <div className="panel-head">
                <div>
                  <h2 className="word-title">{parsedResult.heading}</h2>
                  <p className="part-of-speech">{parsedResult.partOfSpeech}</p>
                </div>
                <div className="detail-actions">
                  <button className="mini-btn" onClick={speakMeaning}>{speaking ? "Stop" : "Speak"}</button>
                  <button className="mini-btn" onClick={voiceInput}>Voice</button>
                </div>
              </div>

              <section className="meaning-block">
                <h3>Definition</h3>
                <p>{parsedResult.primaryMeaning}</p>
                {parsedResult.extraMeanings.map((line, index) => (
                  <p key={`extra-${index}`} className="muted-line">{line}</p>
                ))}
              </section>

              <section className="chips-block">
                <h3>Usage & Synonyms</h3>
                <div className="chips-wrap">
                  {parsedResult.synonyms.length > 0 ? (
                    parsedResult.synonyms.map((item, index) => (
                      <span key={`syn-${item}-${index}`} className="chip">{item}</span>
                    ))
                  ) : (
                    <span className="chip muted">No synonyms</span>
                  )}
                </div>
              </section>

              <section className="chips-block">
                <h3>Antonyms</h3>
                <div className="chips-wrap">
                  {parsedResult.antonyms.length > 0 ? (
                    parsedResult.antonyms.map((item, index) => (
                      <span key={`ant-${item}-${index}`} className="chip alt">{item}</span>
                    ))
                  ) : (
                    <span className="chip muted">No antonyms</span>
                  )}
                </div>
              </section>

              <textarea className="result-area" readOnly value={result} placeholder="Search result will appear here..." />
            </article>
          </div>
            </section>
          </section>
        </div>
        <div className="monitor-stand" />
        <div className="monitor-base" />
      </div>
    </main>
  );
}

export default App;
