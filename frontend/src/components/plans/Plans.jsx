import React, { useState, useEffect } from 'react';
import './Plans.css';

const Plans = () => {
  const [plans, setPlans] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);
  const [formData, setFormData] = useState({
    plan_name: '',
    description: '',
    duration_days: '',
    price: '',
    is_active: true
  });

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/v1/subscriptionPlan');
      const data = await response.json();
      setPlans(data);
    } catch (error) {
      console.error('Error fetching plans:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = editingPlan 
      ? `http://127.0.0.1:8000/v1/subscriptionPlan/${editingPlan.plan_id}`
      : 'http://127.0.0.1:8000/v1/subscriptionPlan';
    
    const method = editingPlan ? 'PUT' : 'POST';
    
    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        fetchPlans();
        closeModal();
      } else {
        alert('Save failed');
      }
    } catch (error) {
      console.error('Error saving plan:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this plan?')) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/v1/subscriptionPlan/${id}`, { 
          method: 'DELETE' 
        });
        
        if (response.ok) {
          fetchPlans();
        }
      } catch (error) {
        console.error('Error deleting plan:', error);
      }
    }
  };

  const openModal = (plan = null) => {
    setEditingPlan(plan);
    setFormData(plan ? {
      plan_name: plan.plan_name,
      description: plan.description,
      duration_days: plan.duration_days,
      price: plan.price,
      is_active: plan.is_active
    } : {
      plan_name: '',
      description: '',
      duration_days: '',
      price: '',
      is_active: true
    });
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingPlan(null);
  };

  return (
    <div className="plans-container">
      <div className="plans-header">
        <h2>📋 Subscription Plans</h2>
        <button className="add-btn" onClick={() => openModal()}>
          + Add Plan
        </button>
      </div>

      <div className="plans-grid">
        {plans.map(plan => (
          <div key={plan.plan_id} className="plan-card">
            <div className="plan-header">
              <h3>{plan.plan_name}</h3>
              <span className={`status ${plan.is_active ? 'active' : 'inactive'}`}>
                {plan.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <p className="plan-description">{plan.description}</p>
            <div className="plan-details">
              <div className="detail-item">
                <span className="label">Duration:</span>
                <span className="value">{plan.duration_days} days</span>
              </div>
              <div className="detail-item">
                <span className="label">Price:</span>
                <span className="value price">₹{plan.price}</span>
              </div>
            </div>
            <div className="plan-actions">
              <button className="edit-btn" onClick={() => openModal(plan)}>
                Edit
              </button>
              <button className="delete-btn" onClick={() => handleDelete(plan.plan_id)}>
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingPlan ? 'Edit Plan' : 'Add New Plan'}</h3>
              <button className="close-btn" onClick={closeModal}>×</button>
            </div>
            <form onSubmit={handleSubmit} className="plan-form">
              <input
                type="text"
                placeholder="Plan Name"
                value={formData.plan_name}
                onChange={e => setFormData({...formData, plan_name: e.target.value})}
                required
              />
              <textarea
                placeholder="Description"
                value={formData.description}
                onChange={e => setFormData({...formData, description: e.target.value})}
                rows="3"
              />
              <input
                type="number"
                placeholder="Duration (days)"
                value={formData.duration_days}
                onChange={e => setFormData({...formData, duration_days: e.target.value})}
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="Price"
                value={formData.price}
                onChange={e => setFormData({...formData, price: e.target.value})}
                required
              />
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={formData.is_active}
                  onChange={e => setFormData({...formData, is_active: e.target.checked})}
                />
                <span>Active Plan</span>
              </label>
              <div className="form-actions">
                <button type="button" className="cancel-btn" onClick={closeModal}>
                  Cancel
                </button>
                <button type="submit" className="save-btn">
                  Save Plan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Plans;