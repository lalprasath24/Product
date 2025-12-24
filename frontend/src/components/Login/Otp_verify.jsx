import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./OtpVerify.css"; // ✅ add css file

const Otp_verify = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const phone_number = location.state?.phone_number || "";

  const [otp, setOtp] = useState("");
  const [responseData, setResponseData] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleVerify = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch("http://localhost:8000/v1/verify-otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone_number, otp }),
      });

      const data = await response.json();
      setResponseData(data);

      if (response.ok) {
        sessionStorage.setItem("access", data.tokens.access);
        sessionStorage.setItem("refresh", data.tokens.refresh);
        navigate("/dashboard");
      } else {
        alert(data.message || "Invalid OTP");
      }
    } catch (error) {
      console.error('Error:', error);  
      setResponseData({ error: "Something went wrong." });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="otp-container">
      <div className="otp-card">
        <h2>Verify OTP</h2>
        <p className="subtitle">We sent an OTP to <strong>{phone_number}</strong></p>

        <form onSubmit={handleVerify} className="otp-form">
          <input
            type="text"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            placeholder="Enter 6-digit OTP"
            maxLength={6}
            className="otp-input"
            required
          />
          <button
            type="submit"
            className={`otp-button ${isSubmitting ? "loading" : ""}`}
            disabled={isSubmitting}
          >
            {isSubmitting ? "Verifying..." : "Verify OTP"}
          </button>
        </form>

        {responseData && (
          <div className="api-response">
            <h4>Server Response</h4>
            <pre>{JSON.stringify(responseData, null, 2)}</pre>
          </div>
        )}

        <p className="resend-text">
          Didn’t receive the code? <a href="#">Resend OTP</a>
        </p>
      </div>
    </div>
  );
};

export default Otp_verify;
