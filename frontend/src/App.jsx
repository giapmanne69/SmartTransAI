import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AuthPage from './features/auth/AuthPage';
import SetupPage from './features/auth/SetupPage';
import DashboardPage from './features/dashboard/DashboardPage';
import WorkspacePage from './features/workspace/WorkspacePage';
import GlossaryPage from './features/glossary/GlossaryPage';
import Layout from './components/Layout';
import { authAPI, settingsAPI } from './services/api';

const App = () => {
  const [user, setUser] = useState(null);
  const [checkingAuth, setCheckingAuth] = useState(true);
  const [isConfigured, setIsConfigured] = useState(false);
  const [checkingConfig, setCheckingConfig] = useState(true);

  const checkConfiguration = async () => {
    try {
      const data = await settingsAPI.getStatus();
      const ready = data.ollama_running && data.model_downloaded && data.openrouter_key_set;
      setIsConfigured(ready);
    } catch (err) {
      console.error('Không thể kiểm tra cấu hình:', err);
    } finally {
      setCheckingConfig(false);
    }
  };

  const checkAuth = async () => {
    if (authAPI.isAuthenticated()) {
      try {
        const userData = await authAPI.getMe();
        setUser(userData);
      } catch (err) {
        console.error('Invalid token, logging out:', err);
        authAPI.logout();
        setUser(null);
      }
    }
    setCheckingAuth(false);
  };

  useEffect(() => {
    checkConfiguration();
    checkAuth();
  }, []);

  const handleLogout = () => {
    authAPI.logout();
    setUser(null);
  };

  if (checkingConfig || checkingAuth) {
    return (
      <div style={{ display: 'flex', height: '100vh', width: '100vw', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--bg-main)', color: 'var(--text-secondary)' }}>
        Đang khởi động SmartTrans AI...
      </div>
    );
  }

  if (!isConfigured) {
    return <SetupPage onSetupComplete={() => setIsConfigured(true)} />;
  }

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route 
          path="/login" 
          element={user ? <Navigate to="/" replace /> : <AuthPage onAuthSuccess={setUser} />} 
        />
        
        {/* Protected Routes */}
        <Route
          path="/"
          element={
            user ? (
              <Layout user={user} onLogout={handleLogout}>
                <DashboardPage />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        <Route
          path="/workspace/:id"
          element={
            user ? (
              <Layout user={user} onLogout={handleLogout}>
                <WorkspacePage />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        <Route
          path="/glossary"
          element={
            user ? (
              <Layout user={user} onLogout={handleLogout}>
                <GlossaryPage />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        {/* Catch-all Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;
