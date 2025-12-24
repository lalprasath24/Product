import React, { useEffect, useState } from 'react';
import './Customers.css';

const Customers = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchType, setSearchType] = useState('name');

  useEffect(() => {
    fetch("http://127.0.0.1:8000/v1/customers/")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch customers");
        return res.json();
      })
      .then((data) => {
        setCustomers(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this customer?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/v1/customers/${id}/`, {
        method: "DELETE",
      });
      if (res.ok) {
        setCustomers(customers.filter((c) => c.customer_id !== id));
      } else {
        alert("Failed to delete customer");
      }
    } catch (error) {
      alert("Error deleting customer: " + error);
    }
  };

  const handleUpdate = (id) => {
    alert(`Update feature coming soon for customer ${id}`);
  };

  const filteredCustomers = customers.filter(customer => {
    if (!searchTerm) return true;
    
    if (searchType === 'id') {
      return customer.customer_id?.toString() === searchTerm;
    } else if (searchType === 'name') {
      const fullName = `${customer.first_name || ''} ${customer.last_name || ''}`.toLowerCase();
      return fullName.includes(searchTerm.toLowerCase());
    }
    return true;
  });

  const getStatusBadge = (status) => {
    const colors = {
      'active': { bg: '#dcfce7', text: '#166534' },
      'inactive': { bg: '#fee2e2', text: '#991b1b' },
      'pending': { bg: '#fef3c7', text: '#92400e' }
    };
    const color = colors[status?.toLowerCase()] || { bg: '#f3f4f6', text: '#374151' };
    return { backgroundColor: color.bg, color: color.text };
  };

  const getTypeBadge = (type) => {
    const colors = {
      'premium': { bg: '#ede9fe', text: '#6b21a8' },
      'regular': { bg: '#dbeafe', text: '#1e40af' },
      'vip': { bg: '#fef3c7', text: '#92400e' }
    };
    const color = colors[type?.toLowerCase()] || { bg: '#f3f4f6', text: '#374151' };
    return { backgroundColor: color.bg, color: color.text };
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loader}>
          <div style={styles.spinner}></div>
          <p style={styles.loadingText}>Loading customers...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.container}>
        <div style={styles.errorCard}>
          <div style={styles.errorIcon}>⚠️</div>
          <h3 style={styles.errorTitle}>Error Loading Customers</h3>
          <p style={styles.errorMessage}>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Customers</h1>
          <p style={styles.subtitle}>{filteredCustomers.length} of {customers.length} customers</p>
        </div>
        <div style={styles.searchContainer}>
          <select
            value={searchType}
            onChange={(e) => setSearchType(e.target.value)}
            style={styles.searchSelect}
          >
            <option value="name">Search by Name</option>
            <option value="id">Search by ID</option>
          </select>
          <input
            type="text"
            placeholder={searchType === 'id' ? 'Enter customer ID...' : 'Enter customer name...'}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={styles.searchInput}
            className="search-input"
          />
        </div>
      </div>

      <div style={styles.tableContainer}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.tableHeader}>
              <th style={styles.th}>ID</th>
              <th style={styles.th}>Name</th>
              <th style={styles.th}>Phone</th>
              <th style={styles.th}>Email</th>
              <th style={styles.th}>City</th>
              <th style={styles.th}>Type</th>
              <th style={styles.th}>Status</th>
              <th style={styles.th}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredCustomers.map((customer, index) => (
              <tr key={customer.customer_id} style={index % 2 === 0 ? styles.evenRow : styles.oddRow}>
                <td style={styles.td}>
                  <span style={styles.idBadge}>{customer.customer_id}</span>
                </td>
                <td style={styles.td}>
                  <div style={styles.nameCell}>
                    <div style={styles.avatar}>
                      {customer.first_name?.charAt(0)?.toUpperCase()}
                    </div>
                    <span style={styles.customerName}>
                      {customer.first_name} {customer.last_name || ''}
                    </span>
                  </div>
                </td>
                <td style={styles.td}>{customer.phone}</td>
                <td style={styles.td}>{customer.email || '-'}</td>
                <td style={styles.td}>{customer.city || '-'}</td>
                <td style={styles.td}>
                  <span style={{...styles.badge, ...getTypeBadge(customer.type)}}>
                    {customer.type}
                  </span>
                </td>
                <td style={styles.td}>
                  <span style={{...styles.badge, ...getStatusBadge(customer.status)}}>
                    {customer.status}
                  </span>
                </td>
                <td style={styles.td}>
                  <div style={styles.actionButtons}>
                    <button
                      onClick={() => handleUpdate(customer.customer_id)}
                      style={styles.updateButton}
                      className="update-button"
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => handleDelete(customer.customer_id)}
                      style={styles.deleteButton}
                      className="delete-button"
                    >
                      🗑️
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredCustomers.length === 0 && (
        <div style={styles.emptyState}>
          <div style={styles.emptyIcon}>👥</div>
          <h3 style={styles.emptyTitle}>No customers found</h3>
          <p style={styles.emptyMessage}>
            {searchTerm ? `No customers found for "${searchTerm}"` : 'No customers available'}
          </p>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '24px',
    backgroundColor: '#f8fafc',
    minHeight: '100vh',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '24px',
    flexWrap: 'wrap',
    gap: '16px'
  },
  title: {
    fontSize: '28px',
    fontWeight: '700',
    color: '#1f2937',
    margin: '0'
  },
  subtitle: {
    fontSize: '14px',
    color: '#6b7280',
    margin: '4px 0 0 0'
  },
  searchContainer: {
    display: 'flex',
    gap: '12px',
    alignItems: 'center'
  },
  searchSelect: {
    padding: '10px 12px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '14px',
    backgroundColor: 'white',
    outline: 'none',
    cursor: 'pointer'
  },
  searchInput: {
    padding: '10px 16px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '14px',
    width: '250px',
    outline: 'none',
    transition: 'all 0.2s ease',
    backgroundColor: 'white'
  },
  tableContainer: {
    backgroundColor: 'white',
    borderRadius: '12px',
    overflow: 'hidden',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse'
  },
  tableHeader: {
    backgroundColor: '#f9fafb'
  },
  th: {
    padding: '16px',
    textAlign: 'left',
    fontSize: '14px',
    fontWeight: '600',
    color: '#374151',
    borderBottom: '1px solid #e5e7eb'
  },
  td: {
    padding: '16px',
    fontSize: '14px',
    color: '#374151',
    borderBottom: '1px solid #f3f4f6'
  },
  evenRow: {
    backgroundColor: '#ffffff'
  },
  oddRow: {
    backgroundColor: '#f9fafb'
  },
  nameCell: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px'
  },
  avatar: {
    width: '32px',
    height: '32px',
    borderRadius: '50%',
    backgroundColor: '#3b82f6',
    color: 'white',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '14px',
    fontWeight: '600',
    flexShrink: 0
  },
  customerName: {
    fontWeight: '500',
    color: '#1f2937'
  },
  idBadge: {
    backgroundColor: '#f3f4f6',
    color: '#374151',
    padding: '4px 8px',
    borderRadius: '6px',
    fontSize: '12px',
    fontWeight: '500'
  },
  badge: {
    padding: '4px 12px',
    borderRadius: '16px',
    fontSize: '12px',
    fontWeight: '500',
    textAlign: 'center',
    display: 'inline-block'
  },
  actionButtons: {
    display: 'flex',
    gap: '8px'
  },
  updateButton: {
    padding: '6px 12px',
    backgroundColor: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '12px',
    cursor: 'pointer',
    transition: 'all 0.2s ease'
  },
  deleteButton: {
    padding: '6px 12px',
    backgroundColor: '#ef4444',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '12px',
    cursor: 'pointer',
    transition: 'all 0.2s ease'
  },
  loader: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '400px'
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '4px solid #f3f4f6',
    borderTop: '4px solid #3b82f6',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite'
  },
  loadingText: {
    marginTop: '16px',
    fontSize: '16px',
    color: '#6b7280'
  },
  errorCard: {
    backgroundColor: 'white',
    borderRadius: '16px',
    padding: '48px',
    textAlign: 'center',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    maxWidth: '400px',
    margin: '0 auto'
  },
  errorIcon: {
    fontSize: '48px',
    marginBottom: '16px'
  },
  errorTitle: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: '8px'
  },
  errorMessage: {
    fontSize: '16px',
    color: '#6b7280'
  },
  emptyState: {
    textAlign: 'center',
    padding: '64px 24px',
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    marginTop: '24px'
  },
  emptyIcon: {
    fontSize: '48px',
    marginBottom: '16px'
  },
  emptyTitle: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: '8px'
  },
  emptyMessage: {
    fontSize: '14px',
    color: '#6b7280'
  }
};

export default Customers;