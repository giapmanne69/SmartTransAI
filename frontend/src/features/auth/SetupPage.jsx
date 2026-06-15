import React, { useState, useEffect } from 'react';
import { settingsAPI } from '../../services/api';

const SetupPage = ({ onSetupComplete }) => {
  const [status, setStatus] = useState({
    ollama_running: false,
    model_downloaded: false,
    openrouter_key_set: false,
    pull_status: { status: 'idle', progress: 0, message: '' }
  });
  
  const [openrouterKey, setOpenrouterKey] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [saving, setSaving] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const fetchStatus = async () => {
    try {
      const data = await settingsAPI.getStatus();
      setStatus(data);
      if (data.pull_status && data.pull_status.status === 'downloading') {
        setDownloading(true);
      } else {
        setDownloading(false);
      }
    } catch (err) {
      console.error('Không thể kết nối đến backend:', err);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleSaveKey = async (e) => {
    e.preventDefault();
    if (!openrouterKey.trim()) {
      setError('Vui lòng nhập API Key.');
      return;
    }
    setSaving(true);
    setError('');
    setSuccess('');
    try {
      await settingsAPI.saveSettings(openrouterKey.trim());
      setSuccess('Đã lưu OpenRouter API Key thành công!');
      fetchStatus();
    } catch (err) {
      setError('Lỗi không thể lưu cấu hình API Key.');
    } finally {
      setSaving(false);
    }
  };

  const handlePullModel = async () => {
    setError('');
    try {
      await settingsAPI.pullModel();
      setDownloading(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Lỗi không thể kích hoạt tải mô hình.');
    }
  };

  const isAllReady = status.ollama_running && status.model_downloaded && status.openrouter_key_set;

  return (
    <div className="auth-page">
      <div className="auth-card" style={{ maxWidth: '500px' }}>
        <div className="auth-header">
          <h1 className="auth-title">Cấu hình SmartTrans AI</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13.5px', marginTop: '4px' }}>
            Thiết lập môi trường cục bộ và kết nối API để bắt đầu
          </p>
        </div>

        {error && <div className="alert-banner alert-error">{error}</div>}
        {success && <div className="alert-banner alert-success">{success}</div>}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', marginBottom: '24px' }}>
          
          {/* Step 1: Ollama Service Status */}
          <div style={{ background: 'hsla(217, 32%, 80%, 0.03)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ fontSize: '14px', fontWeight: '600' }}>1. Dịch vụ Ollama</h3>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  Cần thiết để chạy mô hình Llama-3 cục bộ
                </p>
              </div>
              <span className={`badge ${status.ollama_running ? 'badge-done' : 'badge-failed'}`} style={{ fontSize: '10px' }}>
                {status.ollama_running ? 'Đang chạy' : 'Chưa bật'}
              </span>
            </div>
            {!status.ollama_running && (
              <div style={{ marginTop: '12px', fontSize: '12px', color: 'var(--accent-rose)', lineHeight: '1.4' }}>
                ⚠️ Vui lòng khởi động phần mềm Ollama trên máy tính của bạn. Nếu chưa cài đặt, hãy tải về từ <a href="https://ollama.com" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-cyan)', textDecoration: 'underline' }}>ollama.com</a>.
              </div>
            )}
          </div>

          {/* Step 2: Llama-3-8B-Instruct Model Status */}
          <div style={{ background: 'hsla(217, 32%, 80%, 0.03)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ fontSize: '14px', fontWeight: '600' }}>2. Mô hình Llama-3-8B-Instruct</h3>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  Chạy dịch thuật offline trực tiếp trên máy
                </p>
              </div>
              <span className={`badge ${status.model_downloaded ? 'badge-done' : downloading ? 'badge-translating' : 'badge-pending'}`} style={{ fontSize: '10px' }}>
                {status.model_downloaded ? 'Đã tải' : downloading ? 'Đang tải' : 'Chưa có'}
              </span>
            </div>

            {!status.model_downloaded && status.ollama_running && !downloading && (
              <button className="btn btn-primary" onClick={handlePullModel} style={{ width: '100%', marginTop: '14px', padding: '8px 12px', fontSize: '12px' }}>
                📥 Tải mô hình Llama-3
              </button>
            )}

            {downloading && status.pull_status && (
              <div style={{ marginTop: '14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  <span>{status.pull_status.message}</span>
                  <span>{status.pull_status.progress}%</span>
                </div>
                <div style={{ width: '100%', height: '6px', background: 'hsl(223, 47%, 9%)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ width: `${status.pull_status.progress}%`, height: '100%', background: 'linear-gradient(90deg, var(--accent-cyan), var(--accent-purple))', transition: 'width 0.3s ease' }} />
                </div>
              </div>
            )}
          </div>

          {/* Step 3: OpenRouter API Key Input */}
          <div style={{ background: 'hsla(217, 32%, 80%, 0.03)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div>
                <h3 style={{ fontSize: '14px', fontWeight: '600' }}>3. OpenRouter API Key</h3>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  Dùng cho Node đánh giá/Reviewer
                </p>
              </div>
              <span className={`badge ${status.openrouter_key_set ? 'badge-done' : 'badge-pending'}`} style={{ fontSize: '10px' }}>
                {status.openrouter_key_set ? 'Đã cấu hình' : 'Chưa có'}
              </span>
            </div>
            
            <form onSubmit={handleSaveKey} style={{ display: 'flex', gap: '10px' }}>
              <input
                type="password"
                className="input"
                value={openrouterKey}
                onChange={(e) => setOpenrouterKey(e.target.value)}
                placeholder={status.openrouter_key_set ? '••••••••••••••••••••••••' : 'Nhập sk-or-v1-...'}
                style={{ padding: '8px 12px', fontSize: '12.5px' }}
              />
              <button type="submit" className="btn btn-secondary" style={{ padding: '8px 14px', fontSize: '12.5px', whiteSpace: 'nowrap' }} disabled={saving}>
                {saving ? 'Đang lưu...' : 'Lưu Key'}
              </button>
            </form>
          </div>
        </div>

        {/* Proceed Button */}
        <button
          className="btn btn-primary"
          style={{ width: '100%', padding: '12px', fontSize: '15px', textTransform: 'uppercase', letterSpacing: '0.05em', boxShadow: isAllReady ? 'var(--shadow-glow)' : 'none' }}
          disabled={!isAllReady}
          onClick={onSetupComplete}
        >
          {isAllReady ? '🚀 Tiếp tục vào ứng dụng' : 'Vui lòng hoàn thành cấu hình'}
        </button>
      </div>
    </div>
  );
};

export default SetupPage;
