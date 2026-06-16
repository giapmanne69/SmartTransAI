import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { documentAPI, parseError } from '../../services/api';

const DashboardPage = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const fetchDocuments = async (silent = false) => {
    if (!silent) setLoading(true);
    try {
      const data = await documentAPI.getAll();
      setDocuments(data);
    } catch (err) {
      setError('Không thể lấy danh sách tài liệu.');
      console.error(err);
    } finally {
      if (!silent) setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  // Poll for document status updates if any document is processing
  useEffect(() => {
    const hasProcessing = documents.some((doc) => doc.status === 'processing');
    if (!hasProcessing) return;

    const interval = setInterval(() => {
      fetchDocuments(true);
    }, 4000);

    return () => clearInterval(interval);
  }, [documents]);

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Check file extension
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx', 'txt'].includes(ext)) {
      setError('Định dạng tệp không được hỗ trợ. Vui lòng tải lên PDF, DOCX, hoặc TXT.');
      return;
    }

    setUploading(true);
    setError('');
    try {
      await documentAPI.upload(file);
      await fetchDocuments();
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (err) {
      setError(parseError(err, 'Lỗi tải lên tài liệu.'));
    } finally {
      setUploading(false);
    }
  };

  const handleTranslate = async (e, id) => {
    e.stopPropagation();
    try {
      await documentAPI.translate(id);
      // Trigger update state immediately
      setDocuments((prev) =>
        prev.map((doc) => (doc.id === id ? { ...doc, status: 'processing' } : doc))
      );
    } catch (err) {
      setError('Lỗi kích hoạt tiến trình dịch thuật.');
    }
  };

  const handleStopTranslate = async (e, id) => {
    e.stopPropagation();
    setError('');
    try {
      await documentAPI.stopTranslation(id);
      setDocuments((prev) =>
        prev.map((doc) => (doc.id === id ? { ...doc, status: 'uploaded' } : doc))
      );
    } catch (err) {
      setError('Lỗi không thể dừng tiến trình dịch thuật.');
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <div style={{ padding: '24px 32px' }}>
      {error && (
        <div className="alert-banner alert-error" style={{ maxWidth: '800px', margin: '0 auto 20px auto' }}>
          {error}
        </div>
      )}

      {/* Drag & Drop Upload Zone */}
      <div className="upload-zone" onClick={triggerFileInput} style={{ maxWidth: '800px', margin: '0 auto 40px auto' }}>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileUpload}
          style={{ display: 'none' }}
          accept=".pdf,.docx,.txt"
        />
        <div className="upload-icon">📤</div>
        <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '4px' }}>
          {uploading ? 'Đang tải lên và phân tích tài liệu...' : 'Kéo thả hoặc click để tải lên tài liệu'}
        </h3>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
          Hỗ trợ định dạng PDF, Word (DOCX) và Text (TXT)
        </p>
      </div>

      {/* Document List Section */}
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '20px' }}>Tài liệu của bạn</h3>

        {loading ? (
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>Đang tải danh sách tài liệu...</p>
        ) : documents.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
            <p style={{ color: 'var(--text-secondary)' }}>Bạn chưa tải lên tài liệu nào. Hãy sử dụng khu vực phía trên để tải lên.</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '24px' }}>
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="card doc-card"
                onClick={() => navigate(`/workspace/${doc.id}`)}
                style={{ cursor: 'pointer' }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                    <span
                      className={`badge badge-${doc.status}`}
                      style={{ fontSize: '10px' }}
                    >
                      {doc.status === 'uploaded'
                        ? 'Đã tải lên'
                        : doc.status === 'processing'
                        ? 'Đang dịch...'
                        : doc.status === 'translated'
                        ? 'Đã dịch xong'
                        : 'Lỗi dịch'}
                    </span>
                    <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                      {new Date(doc.created_at).toLocaleDateString('vi-VN')}
                    </span>
                  </div>
                  <h4 className="doc-title" title={doc.name}>
                    {doc.name}
                  </h4>
                  <p className="doc-info">
                    Định dạng: {doc.file_type.toUpperCase()}
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '10px', marginTop: '12px' }}>
                  <button
                    className="btn btn-secondary"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/workspace/${doc.id}`);
                    }}
                    style={{ flexGrow: 1, padding: '8px 12px', fontSize: '13px' }}
                  >
                    🔍 Mở Workspace
                  </button>

                  {(doc.status === 'uploaded' || doc.status === 'failed') && (
                    <button
                      className="btn btn-primary"
                      onClick={(e) => handleTranslate(e, doc.id)}
                      style={{ padding: '8px 16px', fontSize: '13px' }}
                    >
                      🤖 Dịch AI
                    </button>
                  )}
                  {doc.status === 'processing' && (
                    <button
                      className="btn btn-danger"
                      onClick={(e) => handleStopTranslate(e, doc.id)}
                      style={{ padding: '8px 16px', fontSize: '13px' }}
                    >
                      🛑 Dừng dịch
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
