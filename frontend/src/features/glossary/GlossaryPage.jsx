import React, { useState, useEffect } from 'react';
import { glossaryAPI, parseError } from '../../services/api';

const GlossaryPage = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Form state
  const [sourceTerm, setSourceTerm] = useState('');
  const [targetTerm, setTargetTerm] = useState('');
  const [notes, setNotes] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = React.useRef(null);
  
  const fetchGlossary = async () => {
    setLoading(true);
    try {
      const data = await glossaryAPI.getAll();
      setItems(data);
    } catch (err) {
      setError('Không thể kết nối lấy từ điển.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGlossary();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const res = await glossaryAPI.uploadFile(file);
      setSuccess(`Đã nạp thành công ${res.imported_count} thuật ngữ từ tệp tin!`);
      // Re-fetch glossary
      const data = await glossaryAPI.getAll();
      setItems(data);
    } catch (err) {
      setError(parseError(err, 'Lỗi tải lên tệp tin từ điển.'));
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!sourceTerm || !targetTerm) {
      setError('Vui lòng nhập đầy đủ thuật ngữ gốc và bản dịch.');
      return;
    }

    try {
      if (editingId) {
        // Update item
        const updated = await glossaryAPI.update(editingId, {
          source_term: sourceTerm,
          target_term: targetTerm,
          notes: notes
        });
        setItems((prev) => prev.map((item) => (item.id === editingId ? updated : item)));
        setSuccess('Cập nhật thuật ngữ thành công!');
        setEditingId(null);
      } else {
        // Create item
        const newItem = await glossaryAPI.create(sourceTerm, targetTerm, notes);
        setItems((prev) => [newItem, ...prev]);
        setSuccess('Thêm thuật ngữ chuyên ngành thành công!');
      }
      
      // Reset form
      setSourceTerm('');
      setTargetTerm('');
      setNotes('');
    } catch (err) {
      setError(parseError(err, 'Có lỗi xảy ra khi lưu thuật ngữ.'));
    }
  };

  const handleEdit = (item) => {
    setEditingId(item.id);
    setSourceTerm(item.source_term);
    setTargetTerm(item.target_term);
    setNotes(item.notes || '');
    setError('');
    setSuccess('');
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Bạn có chắc chắn muốn xóa thuật ngữ này khỏi từ điển?')) return;
    setError('');
    setSuccess('');
    try {
      await glossaryAPI.delete(id);
      setItems((prev) => prev.filter((item) => item.id !== id));
      setSuccess('Xóa thuật ngữ thành công!');
      if (editingId === id) {
        setEditingId(null);
        setSourceTerm('');
        setTargetTerm('');
        setNotes('');
      }
    } catch (err) {
      setError('Lỗi không thể xóa thuật ngữ.');
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setSourceTerm('');
    setTargetTerm('');
    setNotes('');
  };

  return (
    <div style={{ padding: '24px 32px', display: 'flex', gap: '32px', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Form Card (Add/Edit) */}
      <div className="card" style={{ width: '380px', height: 'fit-content', flexShrink: 0 }}>
        <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '20px', color: editingId ? 'var(--accent-cyan)' : 'var(--text-primary)' }}>
          {editingId ? '✍️ Sửa thuật ngữ chuyên ngành' : '➕ Thêm thuật ngữ chuyên ngành'}
        </h3>

        {error && <div className="alert-banner alert-error" style={{ fontSize: '13px', padding: '8px 12px' }}>{error}</div>}
        {success && <div className="alert-banner alert-success" style={{ fontSize: '13px', padding: '8px 12px' }}>{success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="label">Thuật ngữ gốc (Tiếng Anh)</label>
            <input
              type="text"
              className="input"
              value={sourceTerm}
              onChange={(e) => setSourceTerm(e.target.value)}
              placeholder="Ví dụ: Machine Learning"
              required
            />
          </div>

          <div className="form-group">
            <label className="label">Bản dịch chuẩn (Tiếng Việt)</label>
            <input
              type="text"
              className="input"
              value={targetTerm}
              onChange={(e) => setTargetTerm(e.target.value)}
              placeholder="Ví dụ: Học máy"
              required
            />
          </div>

          <div className="form-group">
            <label className="label">Ghi chú ngữ cảnh (Tùy chọn)</label>
            <textarea
              className="input"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Giải thích cách dùng hoặc ngữ cảnh ứng dụng..."
              style={{ minHeight: '80px', resize: 'vertical' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
            <button type="submit" className="btn btn-primary" style={{ flexGrow: 1 }}>
              {editingId ? 'Cập nhật' : 'Thêm từ'}
            </button>
            {editingId && (
              <button type="button" className="btn btn-secondary" onClick={handleCancelEdit}>
                Hủy
              </button>
            )}
          </div>
        </form>

        <div style={{ marginTop: '24px', paddingTop: '20px', borderTop: '1px solid var(--border-color)' }}>
          <h4 style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '12px' }}>Nhập hàng loạt từ tệp tin</h4>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            style={{ display: 'none' }}
            accept=".json,.md,.txt"
          />
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => fileInputRef.current?.click()}
            style={{ width: '100%', fontSize: '13px' }}
            disabled={uploading}
          >
            📂 {uploading ? 'Đang nạp...' : 'Tải lên File (.json, .md, .txt)'}
          </button>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '8px', textAlign: 'center', lineHeight: '1.4' }}>
            Chấp nhận định dạng JSON (danh sách hoặc key-value), bảng Markdown hoặc danh sách bullet.
          </p>
        </div>
      </div>

      {/* Glossary List */}
      <div style={{ flexGrow: 1 }}>
        <div className="card" style={{ height: '100%', minHeight: '400px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '20px' }}>
            Bảng tra cứu từ điển Glossary
          </h3>

          {loading ? (
            <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '40px' }}>Đang tải từ điển chuyên ngành...</p>
          ) : items.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', textAlign: 'center', marginTop: '40px', fontStyle: 'italic' }}>
              Chưa có thuật ngữ nào được nạp. Hãy điền vào form bên trái để xây dựng từ điển chuyên ngành!
            </p>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                    <th style={{ padding: '12px 8px', fontWeight: '500' }}>Thuật ngữ gốc</th>
                    <th style={{ padding: '12px 8px', fontWeight: '500' }}>Bản dịch chuẩn</th>
                    <th style={{ padding: '12px 8px', fontWeight: '500' }}>Ghi chú ngữ cảnh</th>
                    <th style={{ padding: '12px 8px', fontWeight: '500', textAlign: 'right' }}>Hành động</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item) => (
                    <tr
                      key={item.id}
                      style={{
                        borderBottom: '1px solid var(--border-color)',
                        transition: 'background-color 0.15s ease',
                      }}
                      onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'hsla(217, 32%, 80%, 0.02)')}
                      onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                    >
                      <td style={{ padding: '14px 8px', fontWeight: '600', color: 'var(--accent-cyan)' }}>
                        {item.source_term}
                      </td>
                      <td style={{ padding: '14px 8px', color: 'var(--text-primary)' }}>
                        {item.target_term}
                      </td>
                      <td style={{ padding: '14px 8px', color: 'var(--text-secondary)', fontSize: '13px', maxWidth: '240px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {item.notes || '—'}
                      </td>
                      <td style={{ padding: '14px 8px', textAlign: 'right' }}>
                        <button
                          className="btn btn-secondary"
                          onClick={() => handleEdit(item)}
                          style={{ padding: '4px 8px', fontSize: '12px', marginRight: '8px' }}
                        >
                          ✏️ Sửa
                        </button>
                        <button
                          className="btn btn-danger"
                          onClick={() => handleDelete(item.id)}
                          style={{ padding: '4px 8px', fontSize: '12px' }}
                        >
                          🗑️ Xóa
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GlossaryPage;
