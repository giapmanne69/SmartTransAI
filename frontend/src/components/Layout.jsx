import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';

const Layout = ({ children, user, onLogout }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  const menuItems = [
    { path: '/', label: 'Tài liệu', icon: '📄' },
    { path: '/glossary', label: 'Từ điển chuyên ngành', icon: '📚' }
  ];

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span>🌀 SmartTrans AI</span>
        </div>
        
        <nav style={{ flexGrow: 1 }}>
          <ul className="sidebar-menu">
            {menuItems.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <li key={item.path} className={`sidebar-item ${isActive ? 'active' : ''}`}>
                  <Link to={item.path}>
                    <span style={{ fontSize: '18px' }}>{item.icon}</span>
                    <span>{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* User Info & Logout */}
        <div style={{ marginTop: 'auto', paddingTop: '20px', borderTop: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--accent-cyan), var(--accent-purple))', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: 'var(--bg-main)' }}>
              {user?.username?.substring(0, 2).toUpperCase() || 'US'}
            </div>
            <div style={{ overflow: 'hidden' }}>
              <p style={{ fontSize: '14px', fontWeight: '600', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{user?.username}</p>
              <p style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>User Account</p>
            </div>
          </div>
          <button className="btn btn-secondary" onClick={handleLogout} style={{ width: '100%', padding: '8px 12px', fontSize: '13px' }}>
            🚪 Đăng xuất
          </button>
        </div>
      </aside>

      {/* Main Panel */}
      <main className="main-content">
        {/* Header */}
        <header className="header">
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: '600' }}>
              {location.pathname === '/' ? 'Dashboard' : location.pathname.startsWith('/workspace') ? 'Không gian dịch thuật song ngữ' : 'Quản lý thuật ngữ chuyên ngành'}
            </h2>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px', color: 'var(--text-secondary)' }}>
            <span>Học viện Công nghệ Bưu chính Viễn thông</span>
          </div>
        </header>

        {/* Inner Content */}
        <div style={{ flexGrow: 1, overflowY: 'auto' }}>
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
