import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, parseError } from '../../services/api';

const AuthPage = ({ onAuthSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    if (!username || !password) {
      setError('Vui lòng điền đầy đủ tên đăng nhập và mật khẩu.');
      setLoading(false);
      return;
    }

    if (!isLogin) {
      if (username.length < 3) {
        setError('Tên đăng nhập phải có ít nhất 3 ký tự.');
        setLoading(false);
        return;
      }
      if (username.length > 50) {
        setError('Tên đăng nhập không được vượt quá 50 ký tự.');
        setLoading(false);
        return;
      }
      if (password.length < 6) {
        setError('Mật khẩu phải có ít nhất 6 ký tự.');
        setLoading(false);
        return;
      }
      if (password !== confirmPassword) {
        setError('Mật khẩu nhập lại không khớp.');
        setLoading(false);
        return;
      }
    }

    try {
      if (isLogin) {
        // Log in
        await authAPI.login(username, password);
        setSuccess('Đăng nhập thành công! Đang chuyển hướng...');
        const user = await authAPI.getMe();
        setTimeout(() => {
          onAuthSuccess(user);
          navigate('/');
        }, 800);
      } else {
        // Register
        await authAPI.register(username, password);
        setSuccess('Đăng ký tài khoản thành công! Vui lòng đăng nhập.');
        setIsLogin(true);
        setPassword('');
        setConfirmPassword('');
      }
    } catch (err) {
      setError(parseError(err, 'Có lỗi xảy ra. Vui lòng thử lại.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-title">Smart Trans AI</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
            {isLogin ? 'Hệ thống dịch thuật Agentic AI' : 'Tạo tài khoản dịch thuật mới'}
          </p>
        </div>

        {error && <div className="alert-banner alert-error">{error}</div>}
        {success && <div className="alert-banner alert-success">{success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="label">Tên đăng nhập</label>
            <input
              type="text"
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Nhập tên đăng nhập"
              required
            />
          </div>

          <div className="form-group">
            <label className="label">Mật khẩu</label>
            <input
              type="password"
              className="input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Nhập mật khẩu"
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label className="label">Xác nhận mật khẩu</label>
              <input
                type="password"
                className="input"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Nhập lại mật khẩu"
                required
              />
            </div>
          )}

          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '10px' }} disabled={loading}>
            {loading ? 'Đang xử lý...' : isLogin ? 'Đăng Nhập' : 'Đăng Ký'}
          </button>
        </form>

        <div style={{ marginTop: '24px', textAlign: 'center', fontSize: '13px' }}>
          <span style={{ color: 'var(--text-secondary)' }}>
            {isLogin ? 'Chưa có tài khoản?' : 'Đã có tài khoản?'}
          </span>{' '}
          <button
            onClick={() => {
              setIsLogin(!isLogin);
              setError('');
              setSuccess('');
            }}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--accent-cyan)',
              cursor: 'pointer',
              fontWeight: '600',
              fontFamily: 'var(--font-sans)',
            }}
          >
            {isLogin ? 'Đăng ký ngay' : 'Đăng nhập ngay'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
