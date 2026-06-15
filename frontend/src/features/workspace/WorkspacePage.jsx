import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { documentAPI, glossaryAPI } from '../../services/api';

const WorkspacePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [document, setDocument] = useState(null);
  const [glossary, setGlossary] = useState([]);
  const [selectedChunk, setSelectedChunk] = useState(null);
  const [translatedText, setTranslatedText] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  const fetchDocumentDetail = async (silent = false) => {
    if (!silent) setLoading(true);
    try {
      const data = await documentAPI.getDetail(id);
      setDocument(data);
      // If there are chunks and none selected yet, select first chunk
      if (data.chunks && data.chunks.length > 0 && !selectedChunk) {
        const first = data.chunks[0];
        setSelectedChunk(first);
        setTranslatedText(first.translated_text || first.original_text);
      } else if (selectedChunk) {
        // Refresh selected chunk data
        const updated = data.chunks.find((c) => c.id === selectedChunk.id);
        if (updated) setSelectedChunk(updated);
      }
    } catch (err) {
      setError('Lỗi kết nối hoặc không tìm thấy tài liệu.');
      console.error(err);
    } finally {
      if (!silent) setLoading(false);
    }
  };

  const fetchGlossary = async () => {
    try {
      const data = await glossaryAPI.getAll();
      setGlossary(data);
    } catch (err) {
      console.error('Lỗi lấy từ điển:', err);
    }
  };

  useEffect(() => {
    fetchDocumentDetail();
    fetchGlossary();
  }, [id]);

  // Polling details when document is processing translation
  useEffect(() => {
    if (!document || document.status !== 'processing') return;

    const interval = setInterval(() => {
      fetchDocumentDetail(true);
    }, 3000);

    return () => clearInterval(interval);
  }, [document]);

  const handleSelectChunk = (chunk) => {
    setSelectedChunk(chunk);
    setTranslatedText(chunk.translated_text || chunk.original_text);
  };

  const handleSaveTranslation = async () => {
    if (!selectedChunk) return;
    setSaving(true);
    try {
      const updated = await documentAPI.updateChunk(selectedChunk.id, translatedText);
      // Update local document chunks
      setDocument((prev) => {
        const newChunks = prev.chunks.map((c) => (c.id === selectedChunk.id ? updated : c));
        return { ...prev, chunks: newChunks };
      });
      setSelectedChunk(updated);
      
      const newChunks = document.chunks.map((c) => (c.id === selectedChunk.id ? updated : c));
      const allCorrected = newChunks.every((c) => c.corrected_by_user);
      
      if (allCorrected) {
        // Automatically trigger document export/download
        const url = documentAPI.exportUrl(id);
        window.open(url, '_blank');
      } else {
        // Show short feedback or auto select next chunk
        const currentIndex = document.chunks.findIndex((c) => c.id === selectedChunk.id);
        if (currentIndex !== -1 && currentIndex < document.chunks.length - 1) {
          const next = document.chunks[currentIndex + 1];
          setSelectedChunk(next);
          setTranslatedText(next.translated_text || next.original_text);
        }
      }
    } catch (err) {
      setError('Lỗi không thể lưu bản dịch.');
    } finally {
      setSaving(false);
    }
  };

  const handleExport = () => {
    // Open export URL directly to download file
    const url = documentAPI.exportUrl(id);
    window.open(url, '_blank');
  };

  const handleTranslateAll = async () => {
    try {
      await documentAPI.translate(id);
      setDocument((prev) => ({ ...prev, status: 'processing' }));
    } catch (err) {
      setError('Lỗi kích hoạt tiến trình dịch thuật.');
    }
  };

  const handleStopTranslateAll = async () => {
    try {
      await documentAPI.stopTranslation(id);
      setDocument((prev) => ({ ...prev, status: 'uploaded' }));
      await fetchDocumentDetail(true);
    } catch (err) {
      setError('Lỗi không thể dừng tiến trình dịch thuật.');
    }
  };

  // Find glossary matches for selected chunk
  const getGlossaryMatches = () => {
    if (!selectedChunk || glossary.length === 0) return [];
    const textLower = selectedChunk.original_text.toLowerCase();
    return glossary.filter((item) => {
      const term = item.source_term.toLowerCase();
      return textLower.includes(term);
    });
  };

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        Đang tải không gian dịch thuật...
      </div>
    );
  }

  if (error || !document) {
    return (
      <div style={{ padding: '40px' }}>
        <div className="alert-banner alert-error">{error || 'Không tìm thấy tài liệu.'}</div>
        <button className="btn btn-secondary" onClick={() => navigate('/')}>Quay lại Dashboard</button>
      </div>
    );
  }

  const glossaryMatches = getGlossaryMatches();

  return (
    <div className="workspace-container">
      {/* Toolbar */}
      <div className="workspace-toolbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button className="btn btn-secondary" onClick={() => navigate('/')} style={{ padding: '6px 12px', fontSize: '13px' }}>
            ⬅️ Quay lại
          </button>
          <span style={{ fontWeight: '600', maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {document.name}
          </span>
          <span className={`badge badge-${document.status}`} style={{ fontSize: '9px' }}>
            {document.status === 'uploaded' ? 'Đã tải lên' : document.status === 'processing' ? 'Đang dịch...' : 'Đã dịch'}
          </span>
        </div>
        
        <div style={{ display: 'flex', gap: '12px' }}>
          {document.status !== 'translated' && document.status !== 'processing' && (
            <button className="btn btn-primary" onClick={handleTranslateAll} style={{ padding: '6px 14px', fontSize: '13px' }}>
              🤖 Dịch toàn bộ bằng AI
            </button>
          )}
          {document.status === 'processing' && (
            <button className="btn btn-danger" onClick={handleStopTranslateAll} style={{ padding: '6px 14px', fontSize: '13px' }}>
              🛑 Dừng dịch AI
            </button>
          )}
          
          <button className="btn btn-secondary" onClick={handleExport} disabled={document.chunks.every(c => !c.translated_text)} style={{ padding: '6px 14px', fontSize: '13px' }}>
            📤 Xuất file dịch (.txt)
          </button>
        </div>
      </div>

      {/* Main Workspace Panels */}
      <div className="workspace-panels">
        {/* Left Panel: English source */}
        <div className="panel-source">
          <h4 style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Bản gốc (Tiếng Anh)</h4>
          {document.chunks.map((chunk) => (
            <div
              key={chunk.id}
              className={`segment-row ${selectedChunk?.id === chunk.id ? 'active' : ''}`}
              onClick={() => handleSelectChunk(chunk)}
            >
              <div className="segment-meta">
                <span>Câu #{chunk.position_index + 1}</span>
                <span className={`badge badge-${chunk.status}`} style={{ fontSize: '8px', padding: '2px 6px' }}>
                  {chunk.status === 'done' ? 'đã dịch' : chunk.status === 'translating' ? 'đang dịch' : 'chờ dịch'}
                </span>
              </div>
              <div className="segment-content">{chunk.original_text}</div>
            </div>
          ))}
        </div>

        {/* Right Panel: Vietnamese translation */}
        <div className="panel-target">
          <h4 style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Bản dịch (Tiếng Việt)</h4>
          {document.chunks.map((chunk) => (
            <div
              key={chunk.id}
              className={`segment-row ${selectedChunk?.id === chunk.id ? 'active' : ''}`}
              onClick={() => handleSelectChunk(chunk)}
            >
              <div className="segment-meta">
                <span>Câu #{chunk.position_index + 1}</span>
                {chunk.corrected_by_user && <span style={{ fontSize: '10px', color: 'var(--accent-cyan)' }}>✍️ Đã hiệu chỉnh</span>}
              </div>
              <div className="segment-content" style={{ fontStyle: chunk.translated_text ? 'normal' : 'italic', color: chunk.translated_text ? 'var(--text-primary)' : 'var(--text-muted)' }}>
                {chunk.translated_text || chunk.original_text}
              </div>
            </div>
          ))}
        </div>

        {/* Right Drawer: Active Edit segment */}
        {selectedChunk && (
          <div className="workspace-side-drawer">
            <div className="drawer-header">
              <span>Chi tiết câu #{selectedChunk.position_index + 1}</span>
              <span className={`badge badge-${selectedChunk.status}`} style={{ fontSize: '9px' }}>
                {selectedChunk.status}
              </span>
            </div>

            <div className="drawer-content">
              {/* Source Sentence */}
              <div>
                <h5 style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Câu gốc:</h5>
                <p style={{ fontSize: '14px', background: 'hsl(223, 47%, 9%)', padding: '10px 14px', borderRadius: '6px', border: '1px solid var(--border-color)', lineHeight: '1.5' }}>
                  {selectedChunk.original_text}
                </p>
              </div>

              {/* Glossary Matches (RAG) */}
              <div>
                <h5 style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Thuật ngữ phù hợp (RAG):</h5>
                {glossaryMatches.length === 0 ? (
                  <p style={{ fontSize: '12px', color: 'var(--text-muted)', fontStyle: 'italic' }}>Không có thuật ngữ nào khớp.</p>
                ) : (
                  <div className="glossary-matches">
                    {glossaryMatches.map((item) => (
                      <div key={item.id} className="glossary-match-item">
                        <div className="glossary-match-term">
                          <span style={{ color: 'var(--accent-cyan)' }}>{item.source_term}</span>
                          <span>➡️</span>
                          <span style={{ color: 'var(--text-primary)' }}>{item.target_term}</span>
                        </div>
                        {item.notes && <p className="glossary-match-notes">{item.notes}</p>}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* AI Translation Suggestion (LangGraph Translator + Style Agent) */}
              {selectedChunk.translated_text && (
                <div className="ai-suggestion-box">
                  <div className="ai-header">
                    <span>🤖 Bản dịch của AI Agent</span>
                  </div>
                  <p style={{ fontSize: '13.5px', color: 'var(--text-primary)', marginBottom: '10px', lineHeight: '1.5' }}>
                    {selectedChunk.translated_text}
                  </p>
                  <button
                    className="btn btn-secondary"
                    onClick={() => setTranslatedText(selectedChunk.translated_text)}
                    style={{ padding: '4px 10px', fontSize: '11px' }}
                  >
                    📝 Khôi phục bản dịch AI
                  </button>
                </div>
              )}

              {/* AI Reviewer critique */}
              {selectedChunk.reviewer_feedback && (
                <div style={{ background: 'hsla(217, 10%, 45%, 0.15)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '12px 16px' }}>
                  <div style={{ fontWeight: '600', fontSize: '12px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                    <span>📝 Đánh giá của Reviewer Agent:</span>
                  </div>
                  <p style={{ fontSize: '12.5px', color: 'var(--text-secondary)', fontStyle: 'italic', lineHeight: '1.4' }}>
                    {selectedChunk.reviewer_feedback}
                  </p>
                </div>
              )}

              {/* Translation Editor */}
              <div className="form-group" style={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                <label className="label">Biên tập bản dịch:</label>
                <textarea
                  className="input"
                  value={translatedText}
                  onChange={(e) => setTranslatedText(e.target.value)}
                  style={{ flexGrow: 1, minHeight: '120px', resize: 'none', lineHeight: '1.5', padding: '12px' }}
                  placeholder="Nhập bản dịch tiếng Việt tại đây..."
                />
              </div>

              {/* Actions */}
              <button
                className="btn btn-primary"
                onClick={handleSaveTranslation}
                disabled={saving}
                style={{ width: '100%' }}
              >
                {saving
                  ? 'Đang lưu...'
                  : (document.chunks.every(c => c.corrected_by_user)
                      ? 'Lưu văn bản'
                      : 'Lưu & Chuyển câu kế tiếp')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkspacePage;
