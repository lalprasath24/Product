// Login.jsx

import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import './Login.css';

const Login = () => {
  const [phone, setPhone] = useState('');
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [responseData, setResponseData] = useState(null);
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};

    if (!phone) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^\+?\d{10,15}$/.test(phone)) {
      newErrors.phone = 'Enter a valid phone number (with country code)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (validateForm()) {
      setIsSubmitting(true);
      setResponseData(null);

      try {
        const response = await fetch('http://localhost:8000/v1/send-otp/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ phone_number: phone }),
        });

        const data = await response.json();
        console.log('API Response:', data);
        setResponseData(data);
        if (response.ok) {
          // ✅ redirect to otp verify page & pass phone number
          navigate("/otp-verify", { state: { phone_number: phone } });
        } else {
          alert(data.message || "Failed to send OTP");
        }
        
      } catch (error) {
        console.error('Error:', error);
        setResponseData({ error: 'Something went wrong. Please try again.' });
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h2>Login with Phone</h2>
          <p>Enter your phone number to receive an OTP</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="phone">Phone Number</label>
            <input
              type="text"
              id="phone"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className={errors.phone ? 'error' : ''}
              placeholder="+8765678765"
            />
            {errors.phone && <span className="error-message">{errors.phone}</span>}
          </div>

          <button
            type="submit"
            className={`login-button ${isSubmitting ? 'submitting' : ''}`}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Sending OTP...' : 'Send OTP'}
          </button>
        </form>

        {responseData && (
          <div className="api-response">
            <h4>API Response:</h4>
            <pre>{JSON.stringify(responseData, null, 2)}</pre>
          </div>
        )}

        <div className="login-footer">
          <p>Don't have an account? <a href="#signup">Sign up</a></p>
        </div>
      </div>
    </div>
  );
};

export default Login;
