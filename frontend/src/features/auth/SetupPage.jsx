import React, { useState, useEffect } from 'react';
import { settingsAPI, parseError } from '../../services/api';

const SetupPage = ({ onSetupComplete }) => {
  const [currentStep, setCurrentStep] = useState(1);
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
      setError(parseError(err, 'Lỗi không thể kích hoạt tải mô hình.'));
    }
  };

  const isAllReady = status.ollama_running && status.model_downloaded && status.openrouter_key_set;

  const nextStep = () => {
    if (currentStep < 4) setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const renderStepIndicators = () => {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '24px', gap: '8px' }}>
        {[1, 2, 3, 4].map(step => (
          <div 
            key={step} 
            style={{ 
              width: '40px', 
              height: '4px', 
              borderRadius: '2px', 
              background: step <= currentStep ? 'var(--accent-cyan)' : 'var(--border-color)',
              transition: 'background 0.3s ease'
            }} 
          />
        ))}
      </div>
    );
  };

  return (
    <div className="auth-page">
      <div className="auth-card" style={{ maxWidth: '550px' }}>
        <div className="auth-header" style={{ marginBottom: '16px' }}>
          <h1 className="auth-title">Cấu hình SmartTrans AI</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13.5px', marginTop: '4px' }}>
            Bước {currentStep} trên 4: Thiết lập môi trường
          </p>
        </div>

        {renderStepIndicators()}

        {error && <div className="alert-banner alert-error">{error}</div>}
        {success && <div className="alert-banner alert-success">{success}</div>}

        <div style={{ minHeight: '260px', marginBottom: '24px' }}>
          {currentStep === 1 && (
            <div className="step-content animate-fade-in">
              <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>Cài đặt phần mềm Ollama</h2>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '16px', lineHeight: '1.5' }}>
                SmartTrans AI sử dụng các mô hình AI chạy cục bộ trên máy tính của bạn thông qua <strong>Ollama</strong> để đảm bảo tốc độ và bảo mật dữ liệu.
              </p>
              <div style={{ background: 'hsla(217, 32%, 80%, 0.03)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <ol style={{ fontSize: '13.5px', color: 'var(--text-main)', paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <li>Truy cập trang web <a href="https://ollama.com" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-cyan)', fontWeight: '500' }}>ollama.com</a></li>
                  <li>Tải xuống và cài đặt phần mềm phù hợp với hệ điều hành của bạn.</li>
                  <li>Mở ứng dụng Ollama sau khi cài đặt thành công.</li>
                </ol>
              </div>
              <div style={{ marginTop: '20px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '14px', fontWeight: '500' }}>Trạng thái kết nối:</span>
                <span className={`badge ${status.ollama_running ? 'badge-done' : 'badge-failed'}`}>
                  {status.ollama_running ? '✅ Đã kết nối thành công' : '❌ Chưa kết nối được (Đang tìm kiếm...)'}
                </span>
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="step-content animate-fade-in">
              <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>Tải mô hình Llama-3-8B-Instruct</h2>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '16px', lineHeight: '1.5' }}>
                Đây là mô hình ngôn ngữ lớn (LLM) sẽ chạy trực tiếp trên máy của bạn để thực hiện các tác vụ dịch thuật một cách thông minh. Quá trình tải có thể mất vài phút tùy tốc độ mạng.
              </p>
              
              <div style={{ background: 'hsla(217, 32%, 80%, 0.03)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                  <span style={{ fontSize: '14px', fontWeight: '500' }}>Trạng thái:</span>
                  <span className={`badge ${status.model_downloaded ? 'badge-done' : downloading ? 'badge-translating' : 'badge-pending'}`}>
                    {status.model_downloaded ? '✅ Đã tải mô hình' : downloading ? '⏳ Đang tải...' : '⚠️ Chưa có mô hình'}
                  </span>
                </div>

                {!status.model_downloaded && !downloading && (
                  <div>
                    {status.ollama_running ? (
                      <button className="btn btn-primary" onClick={handlePullModel} style={{ width: '100%', padding: '10px 16px', fontSize: '14px' }}>
                        📥 Bấm vào đây để tải mô hình Llama-3 (~4.7GB)
                      </button>
                    ) : (
                      <div className="alert-banner alert-error" style={{ fontSize: '13px' }}>
                        Vui lòng đảm bảo Ollama đang chạy (từ Bước 1) trước khi tải mô hình.
                      </div>
                    )}
                  </div>
                )}

                {downloading && status.pull_status && (
                  <div style={{ marginTop: '14px', padding: '12px', background: 'var(--bg-lighter)', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', color: 'var(--text-main)', marginBottom: '8px' }}>
                      <span style={{ fontWeight: '500' }}>{status.pull_status.message}</span>
                      <span style={{ fontWeight: 'bold', color: 'var(--accent-cyan)' }}>{status.pull_status.progress}%</span>
                    </div>
                    <div style={{ width: '100%', height: '8px', background: 'hsl(223, 47%, 9%)', borderRadius: '4px', overflow: 'hidden' }}>
                      <div style={{ width: `${status.pull_status.progress}%`, height: '100%', background: 'linear-gradient(90deg, var(--accent-cyan), var(--accent-purple))', transition: 'width 0.3s ease' }} />
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="step-content animate-fade-in">
              <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>Cấu hình OpenRouter API Key</h2>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '16px', lineHeight: '1.5' }}>
                Ứng dụng cần sử dụng các mô hình đám mây tiên tiến (như GPT-4o, Claude-3.5) để làm nhiệm vụ đánh giá (Reviewer) chất lượng bản dịch. Chúng tôi sử dụng OpenRouter làm cổng kết nối.
              </p>
              
              <div style={{ background: 'hsla(217, 32%, 80%, 0.03)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <ol style={{ fontSize: '13.5px', color: 'var(--text-main)', paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '20px' }}>
                  <li>Truy cập <a href="https://openrouter.ai/keys" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-cyan)', fontWeight: '500' }}>openrouter.ai/keys</a> và đăng nhập/đăng ký.</li>
                  <li>Tạo một API Key mới (Create Key) và sao chép mã đó.</li>
                  <li>Dán mã API Key vào ô trống bên dưới để lưu.</li>
                </ol>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <span style={{ fontSize: '14px', fontWeight: '500' }}>Trạng thái:</span>
                  <span className={`badge ${status.openrouter_key_set ? 'badge-done' : 'badge-pending'}`}>
                    {status.openrouter_key_set ? '✅ Đã lưu cấu hình' : '⚠️ Chưa cấu hình Key'}
                  </span>
                </div>

                <form onSubmit={handleSaveKey} style={{ display: 'flex', gap: '10px' }}>
                  <input
                    type="password"
                    className="input"
                    value={openrouterKey}
                    onChange={(e) => setOpenrouterKey(e.target.value)}
                    placeholder={status.openrouter_key_set ? '••••••••••••••••••••••••' : 'Nhập sk-or-v1-...'}
                    style={{ flex: 1, padding: '10px 14px', fontSize: '14px' }}
                  />
                  <button type="submit" className="btn btn-secondary" style={{ padding: '10px 16px', fontSize: '14px', whiteSpace: 'nowrap' }} disabled={saving}>
                    {saving ? 'Đang lưu...' : 'Lưu Key'}
                  </button>
                </form>
              </div>
            </div>
          )}

          {currentStep === 4 && (
            <div className="step-content animate-fade-in">
              <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px', textAlign: 'center' }}>Hoàn tất cấu hình</h2>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '24px', lineHeight: '1.5', textAlign: 'center' }}>
                Vui lòng kiểm tra lại trạng thái của các thành phần hệ thống trước khi bắt đầu.
              </p>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '30px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '14px 16px', background: 'hsla(217, 32%, 80%, 0.03)', borderRadius: '8px', border: `1px solid ${status.ollama_running ? 'var(--border-color)' : 'hsla(0, 100%, 65%, 0.3)'}` }}>
                  <span style={{ fontWeight: '500' }}>1. Dịch vụ Ollama</span>
                  <span style={{ color: status.ollama_running ? 'var(--accent-green)' : 'var(--accent-rose)' }}>{status.ollama_running ? 'Sẵn sàng' : 'Chưa bật'}</span>
                </div>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '14px 16px', background: 'hsla(217, 32%, 80%, 0.03)', borderRadius: '8px', border: `1px solid ${status.model_downloaded ? 'var(--border-color)' : 'hsla(0, 100%, 65%, 0.3)'}` }}>
                  <span style={{ fontWeight: '500' }}>2. Mô hình Llama-3</span>
                  <span style={{ color: status.model_downloaded ? 'var(--accent-green)' : 'var(--accent-rose)' }}>{status.model_downloaded ? 'Đã tải xong' : 'Chưa có'}</span>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '14px 16px', background: 'hsla(217, 32%, 80%, 0.03)', borderRadius: '8px', border: `1px solid ${status.openrouter_key_set ? 'var(--border-color)' : 'hsla(0, 100%, 65%, 0.3)'}` }}>
                  <span style={{ fontWeight: '500' }}>3. OpenRouter API</span>
                  <span style={{ color: status.openrouter_key_set ? 'var(--accent-green)' : 'var(--accent-rose)' }}>{status.openrouter_key_set ? 'Đã thiết lập' : 'Chưa có'}</span>
                </div>
              </div>
              
              {!isAllReady && (
                <div className="alert-banner alert-error" style={{ marginBottom: '16px', textAlign: 'center' }}>
                  Có một số thành phần chưa được thiết lập. Bạn có thể quay lại để kiểm tra hoặc tiếp tục nếu biết chắc mình đang làm gì (có thể gặp lỗi khi dùng).
                </div>
              )}
            </div>
          )}
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid var(--border-color)', paddingTop: '20px' }}>
          <button 
            className="btn" 
            style={{ padding: '10px 20px', background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-main)', opacity: currentStep === 1 ? 0.3 : 1, cursor: currentStep === 1 ? 'not-allowed' : 'pointer' }}
            onClick={prevStep}
            disabled={currentStep === 1}
          >
            Quay lại
          </button>

          {currentStep < 4 ? (
            <button 
              className="btn btn-primary" 
              style={{ padding: '10px 24px' }}
              onClick={nextStep}
            >
              Tiếp tục
            </button>
          ) : (
            <button 
              className="btn btn-primary" 
              style={{ padding: '10px 24px', boxShadow: isAllReady ? 'var(--shadow-glow)' : 'none' }}
              onClick={onSetupComplete}
            >
              🚀 Khởi động ứng dụng
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default SetupPage;
