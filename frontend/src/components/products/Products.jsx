import React, { useState, useEffect } from 'react';
import './Products.css';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [formData, setFormData] = useState({
    product_name: '',
    description: '',
    unit_type: '',
    unit_quantity: '',
    price_per_unit: '',
    current_stock: '',
    is_available: true
  });

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/v1/products/');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted with data:', formData);
    
    const url = editingProduct 
      ? `http://127.0.0.1:8000/v1/products/${editingProduct.product_id}`
      : 'http://127.0.0.1:8000/v1/products';
    
    const method = editingProduct ? 'PUT' : 'POST';
    console.log('API call:', method, url);
    
    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      console.log('Response status:', response.status);
      
      if (response.ok) {
        console.log('Success! Refreshing products...');
        await fetchProducts();
        closeModal();
      } else {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        alert('Save failed: ' + errorText);
      }
    } catch (error) {
      console.error('Error saving product:', error);
      alert('Network error: ' + error.message);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this product?')) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/v1/products/${id}`, { 
          method: 'DELETE' 
        });
        
        if (response.ok) {
          fetchProducts();
        } else {
          console.error('Delete failed:', await response.text());
        }
      } catch (error) {
        console.error('Error deleting product:', error);
      }
    }
  };

  const openModal = (product = null) => {
    setEditingProduct(product);
    if (product) {
      setFormData({
        product_name: product.product_name || '',
        description: product.description || '',
        unit_type: product.unit_type || '',
        unit_quantity: product.unit_quantity || '',
        price_per_unit: product.price_per_unit || '',
        current_stock: product.current_stock || '',
        is_available: product.is_available ?? true
      });
    } else {
      setFormData({
        product_name: '',
        description: '',
        unit_type: '',
        unit_quantity: '',
        price_per_unit: '',
        current_stock: '',
        is_available: true
      });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingProduct(null);
  };

  return (
    <div className="products-container">
      <div className="products-header">
        <h2>🛍️ Products Management</h2>
        <button className="add-btn" onClick={() => openModal()}>
          + Add Product
        </button>
      </div>

      <div className="products-grid">
        {products.map(product => (
          <div key={product.product_id} className="product-card">
            <div className="product-header">
              <h3>{product.product_name}</h3>
              <span className={`status ${product.is_available ? 'available' : 'unavailable'}`}>
                {product.is_available ? 'Available' : 'Unavailable'}
              </span>
            </div>
            <p className="product-description">{product.description}</p>
            <div className="product-details">
              <div className="detail-item">
                <span className="label">Price:</span>
                <span className="value price">₹{product.price_per_unit}/{product.unit_type}</span>
              </div>
              <div className="detail-item">
                <span className="label">Stock:</span>
                <span className="value">{product.current_stock} {product.unit_type}s</span>
              </div>
              <div className="detail-item">
                <span className="label">Unit Qty:</span>
                <span className="value">{product.unit_quantity}</span>
              </div>
            </div>
            <div className="product-actions">
              <button className="edit-btn" onClick={() => openModal(product)}>
                Edit
              </button>
              <button className="delete-btn" onClick={() => handleDelete(product.product_id)}>
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
              <h3>{editingProduct ? 'Edit Product' : 'Add New Product'}</h3>
              <button className="close-btn" onClick={closeModal}>×</button>
            </div>
            <form onSubmit={handleSubmit} className="product-form">
              <input
                type="text"
                placeholder="Product Name"
                value={formData.product_name}
                onChange={e => setFormData({...formData, product_name: e.target.value})}
                required
              />
              <textarea
                placeholder="Description"
                value={formData.description}
                onChange={e => setFormData({...formData, description: e.target.value})}
                rows="3"
              />
              <input
                type="text"
                placeholder="Unit Type (liter/packet)"
                value={formData.unit_type}
                onChange={e => setFormData({...formData, unit_type: e.target.value})}
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="Unit Quantity"
                value={formData.unit_quantity}
                onChange={e => setFormData({...formData, unit_quantity: e.target.value})}
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="Price per Unit"
                value={formData.price_per_unit}
                onChange={e => setFormData({...formData, price_per_unit: e.target.value})}
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="Current Stock"
                value={formData.current_stock}
                onChange={e => setFormData({...formData, current_stock: e.target.value})}
                required
              />
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={formData.is_available}
                  onChange={e => setFormData({...formData, is_available: e.target.checked})}
                />
                <span>Available Product</span>
              </label>
              <div className="form-actions">
                <button type="button" className="cancel-btn" onClick={closeModal}>
                  Cancel
                </button>
                <button type="submit" className="save-btn">
                  Save Product
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Products;